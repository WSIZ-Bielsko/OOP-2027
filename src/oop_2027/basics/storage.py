import json
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Storage:
    messages: dict[int, str]


    def __init__(self):
        self.messages = dict()
        self.crypto_salt_size = 16
        self.crypto_iterations = 600_000

    def _derive_key(self, passphrase: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.crypto_iterations,
        )
        return base64.urlsafe_b64encode(kdf.derive(passphrase.encode("utf-8")))

    def add_message(self, msg_id: int, text: str):
        self.messages[msg_id] = text

    def get_message(self, msg_id: int) -> str | None:
        if msg_id not in self.messages:
            return None
        return self.messages[msg_id]

    def save(self, path: str, passphrase: str) -> None:
        salt = os.urandom(self.crypto_salt_size)
        key = self._derive_key(passphrase, salt)
        plaintext = json.dumps(self.messages).encode("utf-8")
        token = Fernet(key).encrypt(plaintext)
        with open(path, "wb") as f:
            f.write(salt + token)

    def load(self, path: str, passphrase: str) -> None:
        with open(path, "rb") as f:
            blob = f.read()
        salt, token = blob[:self.crypto_salt_size], blob[self.crypto_salt_size:]
        key = self._derive_key(passphrase, salt)
        plaintext = Fernet(key).decrypt(token)
        self.messages = {int(k): v for k, v in json.loads(plaintext).items()}


class StorageRunner:
    def __init__(self, storage: Storage):
        self.storage = storage
        self.filename = 'messages.data'


    def run(self):
        while True:
            command = input("Enter command: ")
            match command:
                case "add":
                    msg_id = int(input("Enter message ID: "))
                    text = input("Enter message text: ")
                    self.storage.add_message(msg_id, text)
                case "get":
                    msg_id = int(input("Enter message ID: "))
                    print(self.storage.get_message(msg_id))
                case "list":
                    for msg_id, text in self.storage.messages.items():
                        print(f"{msg_id}: {text}")
                case "save":
                    print("Saving messages...")
                    passphrase = input("Enter passphrase: ")
                    self.storage.save(self.filename, passphrase)
                case "load":
                    print("Loading messages...")
                    passphrase = input("Enter passphrase: ")
                    self.storage.load(self.filename, passphrase)
                case "exit":
                    return




if __name__ == '__main__':
    # runner
    ...
    storage = Storage()
    runner = StorageRunner(storage)
    runner.run()