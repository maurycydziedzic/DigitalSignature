import sys
from Crypto import Random
from Crypto.PublicKey import RSA
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

OK = '\033[92m'
ERROR = '\033[31m'
END = '\033[0m'


def border(text):
    lines = text.splitlines()
    width = max(len(s) for s in lines)
    res = ['┌' + '─' * width + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)


try:
    file = sys.argv[1]
except:
    print(border("Usage:\n"
                 "in terminal type: python/py .\Digital_Signature \"filename.(extension)\" \"filename_to_check.(extension)\"\n"))
    sys.exit(1)


def print_success(msg: str):
    print("{}[SUCCESS] {}{}".format(OK, msg, END))


def print_error(msg: str):
    print("{}[ERROR] {}{}".format(ERROR, msg, END))


def generate_keys():
    with open("TrueRNG.bin", 'rb') as file:
        # Generate the private key
        private_key = RSA.generate(2048, file.read)

        private_pem = private_key.export_key()
        public_key = private_key.publickey().export_key()

        with open('private_key.pem', 'wb') as private_file:
            private_file.write(private_pem)

        with open('public_key.pem', 'wb') as public_file:
            public_file.write(public_key)


        print("RSA keys generated and saved successfully.")
    return private_key, public_key


def sign_document(document_path, private_key_path, signed_document_path):

    with open(document_path, 'rb') as f:
        doc_data = f.read()


    with open(private_key_path, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None
        )

    sha256_hash = hashes.Hash(hashes.SHA256())
    sha256_hash.update(doc_data)
    digest = sha256_hash.finalize()

    signature = private_key.sign(
        digest,
        padding.PKCS1v15(),
        hashes.SHA256()
    )


    with open(signed_document_path, 'wb') as signed_doc_file:
        signed_doc_file.write(doc_data)
        signed_doc_file.write(signature)
try:
    private_key, public_key = generate_keys()

    file_name = file.split('.')[0]
    extention = file.split('.')[1]
    print(extention)
    sign_document(file, 'private_key.pem', f'{file_name}-signed.{extention}')


except Exception as e:
    print_error(str(e))