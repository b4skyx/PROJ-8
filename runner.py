# Importing pathlib to get absolute path
from pathlib import Path
import utilities.dbTools as dbTools
import utilities.encryption as utilenc
import random

cwd = Path(__file__).parents[0]
cwd = str(cwd)


class ClientAccount:
    def __init__(self, account):
        self.ID = account.get("clientID")
        self.passphrase = account.get("password")
        self.key_tuple = utilenc.get_rsa_keys(self.ID, passphrase=self.passphrase)
        self.public_key = self.key_tuple[0]
        self.private_key = self.key_tuple[1]
        self.documents_owned = account.get("documents_owned", [])

def client_login(count=0):
    email = input("EMAIL:")
    password = input("PASSWORD:")
    account = dbTools.get_client_account(email, password)
    if not account:
        print("Email or Password Incorrect!")
        if count > 2:
            print("You have exceeded the maximum limit. EXITING...")
            return False
        return client_login(count+1)
    return account

class runner():
    def __init__(self):
        account = client_login()
        if not account:
            return
        self.client = ClientAccount(account)

    def list_documents(self):
        print("Documents Owned: ", self.client.documents_owned)

    def add_document(self, document_path):
        document_id = random.randint(1, 1000000)
        with open(document_path, "rb") as r:
            data = r.read()
        with open(f"{cwd}/documents/{document_id}", "wb") as f:
            f.write(data)
        self.client.documents_owned.append(document_id)
        utilenc.sign_document(self.client.ID, self.client.passphrase, document_id)
        dbTools.set_client_data(self.client.ID, {"$set": {"documents_owned": self.client.documents_owned}})
        print("Document Added Successfully!")

    def verify_document(self, document_id):
        if utilenc.verify_document(self.client.public_key, document_id):
            print("PASS")
        else:
            print("FAIL")

    def view_signature(self, document_id):
        print("Signature: ", utilenc.get_document_signature(document_id))

    def view_public_key(self):
        print("Public Key: ")
        print(self.client.public_key)


    def run(self):
        if not self.client:
            return
        while True:
            print("\nEnter your choice:")
            print("0) List Documents")
            print("1) Add Document")
            print("2) Verify Document")
            print("3) View Document Signature")
            print("4) View Public Key")
            print("5) Exit")
            choice = int(input())
            if choice == 5:
                break
            elif choice == 4:
                self.view_public_key()
            elif choice == 3:
                if not self.client.documents_owned:
                    print("No Documents found!")
                    continue
                self.list_documents()
                document_id = input("Enter the document ID: ")
                self.view_signature(document_id)
            elif choice == 2:
                if not self.client.documents_owned:
                    print("No Documents found!")
                    continue
                self.list_documents()
                document_id = input("Enter the document ID: ")
                self.verify_document(document_id)
            elif choice == 1:
                docpath = input("Document to be added: ")
                self.add_document(docpath)
            elif choice == 0:
                self.list_documents()


r = runner()
r.run()
