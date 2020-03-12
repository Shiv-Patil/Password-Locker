#! python3
# Password Locker program to store passwords securely.
import base64
import os
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import json
import pyperclip
import string

with open("passwords.json", 'r') as file:
	'''
	If json file successfully loads and is of type dictionary,
	It will be stored in raw_credentials.
	Else, raw_credentials will be initialized to an empty dictionary.
	'''
	try:
		raw_credentials = json.load(file) if type(json.load(file)) is dict else {}
	except:
		raw_credentials = {}

credentials = {}

def master_password():
	'''
	Function asking for master password
	'''
	password = str(input("Enter Master Password: ".center(40)))
	return password

def generate_password(size=16, char=string.ascii_uppercase+string.ascii_lowercase+string.digits):
	'''
	Function to generate a character password for a credential
	'''
	gen_pass=''.join(random.choice(char) for _ in range(size))
	return gen_pass

def generate_key(masterpassword):
	'''
	Function to generate the decrypting key using master password.
	'''
	salt = b"\xa9\x1ei\xece+\x14\x7f\x003\x91\xc1No\x0e\xd1\xa1]\x1a'm\xfe\n\xf3\x8f2\x93\xeb\x0e\xcb\xf8w\xb1\xe4Kv\xdbZ\xd6\x06&!#/\x06=p9\xc8\xbc\xd3\xdfX\xd9/\xa8P\xd0;gf\xcc\xa2\xe0"
	kdf = PBKDF2HMAC(
	    algorithm=hashes.SHA256(),
	    length=32,
	    salt=salt,
	    iterations=100000,
	    backend=default_backend()
	)
	return base64.urlsafe_b64encode(kdf.derive(masterpassword)) # Can only use kdf once

endsection = lambda: print("-"*100, end='\n\n') # Function to print section ends
clrscr = lambda: os.system('cls') # Function to clear the screen

def encrypt(string):
	'''
	Function to encrypt a string and return it in type bytes
	'''
	string = string.encode()
	string = f.encrypt(string)
	return string

def decrypt(string):
	'''
	Function to decrypt the encrypted string of type bytes and return a string
	'''
	string = f.decrypt(string)
	string = string.decode()
	return string

clrscr()
endsection()
print("Welcome to your password locker!".center(40))

masterpassword = master_password() # This is input in the form of a string
masterpassword = masterpassword.encode() # Convert to type bytes
key = generate_key(masterpassword)
f = Fernet(key)

for keys in raw_credentials:
	try:
		correct = raw_credentials[keys].encode()
		correct = decrypt(correct)
		credentials.update({keys : raw_credentials[keys]})
	except:
		pass

clrscr()
endsection()

while True:
	tobreak = False
	print('Use these codes to navigate:'.rjust(35) + '\n' + '       ac-Add Credential' + '\n' + '       cc-Copy credential password' + '\n' + '       dc-Display credentials' + '\n' + '       ex-Exit')
	short_code = input('Enter a choice: '.rjust(40)).lower().strip()

	if short_code == 'ex':
		break

	elif short_code == 'ac':
		clrscr()
		endsection()
		print('To create a new Credential:'.rjust(40))
		account_name = input('Enter account name - '.rjust(40)).strip()
		if account_name in credentials:
			while True:
				inp = input("That account already exists. Do you want to update it? (y/n): ".center(80)).lower().strip()
				if inp == 'y':
					break
				elif inp == 'n':
					tobreak = True
					break
				else:
					print("\nEnter a correct option.".rjust(40))
			if tobreak:
				clrscr()
				endsection()
				continue
		elif account_name in raw_credentials:
			clrscr()
			print()
			print("That account name is taken by another master password.".center(80))
			endsection()
			continue
		else:
			pass
		while True:
			password_option = input('\n       e-enter password\n       g-generate password: ').lower().strip()
			if password_option == 'e':
				password = input("Enter password - ".rjust(40))
				break
			elif password_option == 'g':
				password = generate_password()
				break
			else:
				print("Invalid Option.".rjust(40))
		clrscr()
		print()
		print(f'New credentials created for: {account_name} using password: {password}'.center(80))
		endsection()
		password = encrypt(password)
		password = password.decode('ascii')
		credentials.update({account_name : password})
		raw_credentials.update({account_name : password})
		with open("passwords.json", 'w') as file:
			json.dump(raw_credentials, file)

	elif short_code == 'cc':
		clrscr()
		endsection()
		account_name = input('Enter your account name - '.rjust(40)).strip()
		if account_name in credentials:
			password_raw = credentials[account_name]
			password_raw = password_raw.encode()
			try:
				password = decrypt(password_raw)
			except:
				clrscr()
				print()
				print("Wrong Master Password entered.".center(80))
				endsection()
				continue
			pyperclip.copy(password)
			clrscr()
			print()
			print(f"Password copied for account {account_name}".center(80))
			endsection()
		else:
			clrscr()
			print()
			print("\n" + "That account does not exist for this masterpassword.".center(80))
			endsection()

	elif short_code == 'dc':
		clrscr()
		endsection()
		print(f"{len(credentials)} account(s) stored for current masterpassword in the passwords file: ".center(80)) if len(credentials) > 0 else print("There are no accounts stored.".center(80))
		for key in credentials:
			print(key.center(40))
		endsection()

	else:
		clrscr()
		print()
		print('Please enter correct option.'.rjust(40))
		endsection()