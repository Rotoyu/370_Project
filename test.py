from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key)  # This will print a properly formatted key
