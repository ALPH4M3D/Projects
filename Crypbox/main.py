import re
import getpass
import time
import os
import hashlib
from colorama import init, Fore
import bcrypt
import msvcrt
import RSAcypher
import RSAcertif


def banner():
	os.system('cls' if os.name == 'nt' else 'clear')
	print(Fore.RED + """

 ██████████████████████████   ████████  ███████████████                           
░█░░░███░░░░░███░░░░░░░███   ███░░███  ░░██░░███░░░░░███                          
░   ░███  ░ ░███  █ ░ ░███  ███  ░███   ░███░███    ░███                          
    ░███    ░██████   ░███████   ░███   ░███░██████████                           
    ░███    ░███░░█   ░███░░███  ░███   ░███░███░░░░░░                            
    ░███    ░███ ░   █░███ ░░███ ░███   ░███░███                                  
    █████   ███████████████ ░░███░░████████ █████                                 
   ░░░░░   ░░░░░░░░░░░░░░░   ░░░░ ░░░░░░░░ ░░░░░                                  
                                                                                  
                                                                                  
                                                                                  
   █████████ ███████████ █████ ███████████████ ███████████    ███████  █████ █████
  ███░░░░░██░░███░░░░░██░░███ ░░██░░███░░░░░██░░███░░░░░███ ███░░░░░██░░███ ░░███ 
 ███     ░░░ ░███    ░███░░███ ███ ░███    ░███░███    ░██████     ░░██░░███ ███  
░███         ░██████████  ░░█████  ░██████████ ░██████████░███      ░███░░█████   
░███         ░███░░░░░███  ░░███   ░███░░░░░░  ░███░░░░░██░███      ░███ ███░███  
░░███     ███░███    ░███   ░███   ░███        ░███    ░██░░███     ███ ███ ░░███ 
 ░░█████████ █████   █████  █████  █████       ███████████ ░░░███████░ █████ █████
  ░░░░░░░░░ ░░░░░   ░░░░░  ░░░░░  ░░░░░       ░░░░░░░░░░░    ░░░░░░░  ░░░░░ ░░░░░ 
                                                                                  
                                                             $~Mohamed BEN MANSOUR
                                                             $~Sirine SOUALMIA

	""")

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None
def is_valid_password(password):
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return re.match(password_regex, password) is not None

def check_credentials_exist(email, password):
    if not os.path.exists("Enregistrement.txt"):
        return False  
    with open("Enregistrement.txt", "r") as file:
        for line in file:
            stored_email, stored_password = line.strip().split(":")
            if stored_email == email and stored_password == password:
                return True
    return False

def generate_salt_and_hash(secret):
    salt = bcrypt.gensalt()
    hashed_secret = bcrypt.hashpw(secret.encode('utf-8'), salt)
   
    return salt, hashed_secret

def menu():
	banner()
	print("1- Hash world")
	print("2- RSA encrypt")
	print("3- RSA Certificate")
	print("4- Exit")
	
	def switch(argument):
		match argument:
			case 1:
				wordHashing()
			case 2:
				RSAencrypt()
			case 3:
				RSAcertify()
			case 4:
				print("\nThank you for using our tool ! Have a good one :)")
				exit()
			case default:
				print("Please select a valid option")

	while True:
		#print("Choose option : ", end="", flush=True)
		choice = None
		while choice is None:
			if msvcrt.kbhit():
				choice = int(msvcrt.getch())
		#print(choice)
		switch(choice)
	


# First choice of our menu
def wordHashing():
	banner()
	word = getpass.getpass("Insert word to hash : ")
	banner()
	#print(word)
	print("1- Hash with SHA256")
	print("2- Encrypt the word with a salt")
	print("3- Brute Force the word input")
	print("4- Back to main menu")
	def switch(argument):
		match argument:
			case 1:
				
				print(Fore.GREEN + "Your SHA256 Hash : ",hashlib.sha256(word.encode()).hexdigest())
			case 2:
				salt, hashed_secret = generate_salt_and_hash(word)

				print(Fore.GREEN + "Salt généré :", salt)
				print(Fore.GREEN + "Word Hashed with salt :", hashed_secret.decode('utf-8'))
			
			case 3:
				with open("dict.txt", "r") as file:
					words = file.readlines()
				for wordd in words:
					wordd = wordd.strip()
					hashed_word = hashlib.sha256(wordd.encode()).hexdigest()
				#	print(wordd,hashed_word)

					if hashed_word == hashlib.sha256(word.encode()).hexdigest():
						print(Fore.GREEN + f"Word found: {wordd}")
						break
					else:
						print(Fore.RED + f"Tried the word '{wordd}', but it was wrong.")


			case 4:
				menu()
			case default:
				print("Please select a valid option")

	while True:
		#print("Choose option : ", end="", flush=True)
		choice = None
		while choice is None:
			if msvcrt.kbhit():
				choice = int(msvcrt.getch())
		#print(choice)
		switch(choice)




# 2nd choice of our menu
def RSAencrypt():
	ciphertext = None
	msg = None
	signature = None

	banner()
	print("1- Generate key pairs")
	print("2- Encrypt a message with RSA")
	print("3- Decrypt the message")
	print("4- Sign a message")
	print("5- Verify Signed message signature")
	print("6- Back to main menu ")
	
	def switch(argument):
		nonlocal ciphertext
		nonlocal msg
		nonlocal signature

		match argument:
			case 1:
				RSAcypher.generate_rsa_key_pair("my_keys")
				print(Fore.GREEN + "Key pairs generated !")
			case 2:
				message = input("Type message to encrypt : ")
				ciphertext = RSAcypher.encrypt_message(message, "my_keys_public.pem")
				print(Fore.GREEN + "Encrypted Message:", ciphertext)
			case 3:
				decrypted_message = RSAcypher.decrypt_message(ciphertext, "my_keys_private.pem")
				print(Fore.GREEN + "Decrypted Message:", decrypted_message)
			case 4:
				msg = input("Type message to sign : ")
				signature = RSAcypher.sign_message(msg, "my_keys_private.pem")
				print(Fore.GREEN + "Signature:", signature)
			case 5:
				is_signature_valid = RSAcypher.verify_signature(msg, signature, "my_keys_public.pem")
				print(Fore.GREEN + "Is Signature Valid:", is_signature_valid)
			case 6:
				menu()
			case default:
				print("Please select a valid option")
	
	while True:
		choice = None
		while choice is None:
			if msvcrt.kbhit():
				choice = int(msvcrt.getch())
		#print(choice)
		switch(choice)

	




#3rd choice of our menu
def RSAcertify():
	banner()
	print("1- Generate key pairs")
	print("2- Generate Self-Signed Certificate")
	print("3- Encrypt message using certificate")
	print("4- Back to main menu ")
	
	def switch(argument):

		match argument:
			case 1:
				RSAcertif.generate_rsa_key_pair("my_cert_keys_private.pem", "my_cert_keys_public.pem")
				print(Fore.GREEN + "Key pairs generated Successfully !")
			case 2:
				RSAcertif.generate_self_signed_certificate("my_cert_keys_private.pem", "my_certificate.pem")
				print(Fore.GREEN + "Self-Signed certificate generated Successfully !" )
			case 3:
				message = input("Type message to encrypt with the certificate : ")
				ciphertext = RSAcertif.encrypt_message_with_certificate(message, "my_certificate.pem")
				print(Fore.GREEN + "Encrypted Message:", ciphertext)
			case 4:
				menu()
			case default:
				print("Please select a valid option")
	while True:
		choice = None
		while choice is None:
			if msvcrt.kbhit():
				choice = int(msvcrt.getch())
		#print(choice)
		switch(choice)




def pointsfct():
    time.sleep(1)  
    print(Fore.GREEN + ".", end="", flush=True)
    time.sleep(1)  
    print(Fore.GREEN + ".", end="", flush=True)
    time.sleep(1)  



init(autoreset=True)
banner()
email = input("Please insert your email : ")
password = getpass.getpass("Please insert your password : ")

if check_credentials_exist(email, password):
    print(Fore.GREEN + "Email and password already recorded ! Redirecting to the main menu.", end="")
    pointsfct()
    menu()
else:
    if is_valid_email(email) and is_valid_password(password):
        with open("Enregistrement.txt", "a") as file:
            file.write(f"{email}:{password}\n")
        
        print(Fore.GREEN + "Success, you will be redirected to the login page.", end="")
        pointsfct()
        banner()
        menu()
    else:
        print("Error, please check your input")



