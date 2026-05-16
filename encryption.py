from cryptography.fernet import Fernet
import json
import os

class Credentials:

    def generate_key(self):
        key = Fernet.generate_key()

        with open('credentials/key.key', 'wb') as key_file:
            key_file.write(key)

    def load_key(self):
        if not os.path.exists('credentials/key.key'):
            self.generate_key()

        with open('credentials/key.key', 'rb') as key_file:
            return key_file.read()

    def store_encrypted_credentials(self, email, password):
        key = self.load_key()
        fernet = Fernet(key)

        user_data = {"email": email, "password": password}

        data = fernet.encrypt(json.dumps(user_data).encode())

        with open("credentials/credentials.enc", "wb") as write_file:
            write_file.write(data)

    def load_decrypted_credentials(self):
        key = self.load_key()
        fernet = Fernet(key)
        try:
            with open('credentials/credentials.enc', 'rb') as load_file:
                encrypted_data = load_file.read()
                decrypted_data = fernet.decrypt(encrypted_data).decode()
                data = json.loads(decrypted_data)
                return data['email'], data['password']
        except FileNotFoundError:
            print("File Not Found")
            return None

        except Exception as e:
            print(f"Error Occurred While Authenticating Credentials : {e}")
            return None


if __name__ == "__main__":
    A = Credentials()
    A.store_encrypted_credentials("zeeshanchudri1234@gmail.com", "aabu jidy xrpc bpip")

