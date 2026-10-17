import base64
import json
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

messages = {}


def _get_fernet(passphrase: str, salt: bytes) -> Fernet:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return Fernet(base64.urlsafe_b64encode(kdf.derive(passphrase.encode())))


def save_messages():
    passphrase = input("Enter passphrase to save: ")
    salt = os.urandom(16)
    f_obj = _get_fernet(passphrase, salt)

    data = {
        "salt": base64.b64encode(salt).decode(),
        "msgs": {
            str(k): f_obj.encrypt(v.encode()).decode()
            for k, v in messages.items()
        },
    }
    with open("data.json", "w") as f:
        json.dump(data, f)
    print("Messages saved.")


def load_messages():
    global messages
    if os.path.exists("data.json"):
        passphrase = input("Enter passphrase to load: ")
        with open("data.json", "r") as f:
            data = json.load(f)

        salt = base64.b64decode(data["salt"])
        f_obj = _get_fernet(passphrase, salt)

        try:
            messages = {
                int(k): f_obj.decrypt(v.encode()).decode()
                for k, v in data["msgs"].items()
            }
            print("Messages loaded.")
        except Exception:
            print("Decryption failed. Incorrect passphrase?")
            messages = {}


def add_msg(msg_id: int, text: str):
    messages[msg_id] = text


def get_msg(msg_id: int) -> str:
    return messages.get(msg_id, "Not found")


if __name__ == "__main__":
    load_messages()
    print("--- Message Storage Demo ---")
    while True:
        try:
            inp = input("Enter ID to search, 's' to save, or 'q': ")
            if inp.lower() == "q":
                break
            if inp.lower() == "s":
                save_messages()
                continue
            msg_id = int(inp)
            if msg_id not in messages:
                msg = input("Enter new message: ")
                add_msg(msg_id, msg)
                continue

            print(f"Result: {get_msg(msg_id)}\n")
        except ValueError:
            print("Please enter a valid integer.\n")