# DigitalSignature
Digital signature code in python 
# Warrning I have tested this script only on txt and docx files.
# In this repo you can also download my TrueRNG.bin which I have generated via my TRNG code
Usage of signing machine: in terminal type: python/py .\Digital_Signature \"filename.(extension)"
You will get three new files:
1. private_key.pem
2. public_key.pem
3. filename-signed.(extension)

Than If you want to validate the public key whit your signed file:
Usage of veryfing machine: in terminal type: python/py .\verify.py "filename_to_check.(extension)
you will get putput if the key is compatible or not.
