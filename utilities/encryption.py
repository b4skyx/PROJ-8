# Importing pathlib to get absolute path
from pathlib import Path
# Importing cryptographic libraries
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

cwd = Path(__file__).parents[1]
cwd = str(cwd)


# Core Methods

def generate_rsa_keys(client_id:int, passphrase:str):
    """
    This fucntion generates the RSA keypair.
    The keypair is further encrypted and stored in a file using a passphrase
    """

    keys = RSA.generate(2048)

    encrypted_keys = keys.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC")

    with open(f"{cwd}/keybase/{client_id}_rsa_key.bin", "wb") as f:
        f.write(encrypted_keys)
        f.close()
    return (keys.publickey().export_key(), keys.export_key())

def get_keys_from_encoded(encoded_key, passphrase:str):
    """
    This function decrypts the encoded key using the password
    The encoded key consists of an RSA keypair
    """
    keys = RSA.import_key(encoded_key, passphrase=passphrase)
    return (keys.publickey().export_key(), keys.export_key())

def get_rsa_keys(client_id:int, passphrase:str):
    """
    This fucntion reads the encoded keys from the Filesystem
    Decrypts it and returns a keypair Tuple
    """
    try:
        encoded_key = open(f"{cwd}/keybase/{client_id}_rsa_key.bin", "rb").read()
    except:
        generate_rsa_keys(client_id, passphrase)
        encoded_key = get_rsa_keys(client_id, passphrase)
    key = get_keys_from_encoded(encoded_key, passphrase=passphrase)
    return key

def generate_signature(private_key, data):
    """
    Signs a binary data stream using PKCS1 signature algoritm and a RSA private key
    SHA256 is used for hashing
    """
    hash = SHA256.new(data)
    rsa = RSA.importKey(private_key)
    signer = PKCS1_v1_5.new(rsa)
    signature = signer.sign(hash)
    return signature

def verify_signature(public_key, signature, data):
    """
    Verifies a data stream by calculating its signature using the public key
    Matches it with the signature calculated using a private key
    """
    hash = SHA256.new(data)
    rsa = RSA.importKey(public_key)
    signer = PKCS1_v1_5.new(rsa)
    return True if (signer.verify(hash, signature)) else False


# Document Methods

def get_document(document_id):
    """
    Returns the encrypted document with its ID
    """
    with open(f"{cwd}/documents/{document_id}", "rb") as f:
        data = f.read()
    return data if data else None

def sign_document(client_id, passphrase:str, document_id):
    """
    Signs a document using passphrase
    """
    document = get_document(document_id)
    if not document:
        return
    keys = get_rsa_keys(client_id, passphrase)
    signature = generate_signature(keys[1], document)
    with open(f"{cwd}/signature/{document_id}.sign", "wb") as f:
        f.write(signature)
        f.close()
    return signature

def get_document_signature(document_id):
    """
    Returns the signature of the encrypted document with the given ID
    """
    with open(f"{cwd}/signature/{document_id}.sign", "rb") as f:
        signature = f.read()
    return signature

def verify_document(public_key, signature=False, document_id=None):
    "Verify the documents signature given the public_key and ID"
    if not signature:
        signature = get_document_signature(document_id)
        return verify_document(public_key, signature, document_id)
    document = get_document(document_id)
    if not document:
        return False
    return verify_signature(public_key, signature, document)
