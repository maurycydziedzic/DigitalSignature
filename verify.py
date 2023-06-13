import sys
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

def print_success(msg: str):
    print("{}[SUCCESS] {}{}".format(OK, msg, END))


def print_error(msg: str):
    print("{}[ERROR] {}{}".format(ERROR, msg, END))
try:
    file = sys.argv[1]
    # file_to_check = sys.argv[2]
except:
    print(border("Usage:\n"
                 "in terminal type: python/py .\\verify.py \"filename_to_check.(extension)\"\n"))
    sys.exit(1)

def verify_signature(document_path, public_key_path):
    try:
        with open(document_path, 'rb') as f:
            signed_doc_data = f.read()

        doc_data = signed_doc_data[:-256]
        signature = signed_doc_data[-256:]

        with open(public_key_path, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        sha256_hash = hashes.Hash(hashes.SHA256())
        sha256_hash.update(doc_data)
        digest = sha256_hash.finalize()
        print(public_key.key_size)
        try:
            public_key.verify(
                signature,
                digest,
                padding.PKCS1v15(),
                hashes.SHA256()
            )

            if(public_key.key_size == 2048):
                print_success("The digital signature is correct.")
        except:
            print_error("The digital signature is incorrect")
    except:
        print_error("The digital signature is incorrect")

file_to_check = f"{file}"
verify_signature(file_to_check, 'public_key.pem')