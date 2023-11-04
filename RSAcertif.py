from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta

# Function to generate RSA key pair and save them to files
def generate_rsa_key_pair(private_key_filename, public_key_filename):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open(private_key_filename, "wb") as private_key_file:
        private_key_file.write(private_key_pem)

    public_key = private_key.public_key()
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(public_key_filename, "wb") as public_key_file:
        public_key_file.write(public_key_pem)

# Function to generate a self-signed certificate
def generate_self_signed_certificate(private_key_filename, cert_filename):
    with open(private_key_filename, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    subject = issuer = x509.Name([
        x509.NameAttribute(x509.NameOID.COMMON_NAME, u'localhost')
    ])

    cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer). \
        public_key(private_key.public_key()).serial_number(x509.random_serial_number()). \
        not_valid_before(datetime.utcnow()). \
        not_valid_after(datetime.utcnow() + timedelta(days=365)). \
        sign(private_key, hashes.SHA256(), default_backend())

    with open(cert_filename, "wb") as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

# Function to encrypt a message with a certificate
def encrypt_message_with_certificate(message, cert_filename):
    with open(cert_filename, "rb") as cert_file:
        cert_data = cert_file.read()
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

    public_key = cert.public_key()

    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return ciphertext

