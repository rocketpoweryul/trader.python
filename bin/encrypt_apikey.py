"""
encrypt_api_key v0.01 
Copyright 2011 Brian Monkaba
VERSION 0.3 REVISED by genBTC 
"""


from Crypto.Cipher import AES
import hashlib
import json
import time
import random
import os
import getpass

print "\n\nga-bitbot API Key Encryptor v0.2"
print "-" * 30
print "\n\n"

print "Enter the API KEY:"
key = raw_input()

print "\nEnter the API SECRET KEY:"
secret = raw_input()

print "Enter the site:"
site = raw_input()

print "\n\nEnter an encryption password:"
print "(This is the password required to execute trades)"
password = getpass.getpass()                #uses raw_input() but doesnt keep a history

print "\nGenerating the random salt..."
salt = os.urandom(32)                   #requires Python 2.4  = 32 bytes or 256 bits of randomness
"""salt = hashlib.sha512(pre_salt).digest()    #hashing does not add any new randomness """
partialpath=os.path.join(os.path.dirname(__file__) + '../keys/' + site)
f = open(os.path.join(partialpath + '_salt.txt'),'w')
f.write(salt)
f.close()

print "Generating the password hash..."
hash_pass = hashlib.sha256(password + salt).digest()
encryptor = AES.new(hash_pass, AES.MODE_CBC)            #create the AES container
plaintext = json.dumps({"key":key,"secret":secret})

#new way to pad. Uses 32 block size for the cipher 256 bit AES
#chr(32) happens to be spacebar... (padding with spaces)
pad = lambda s: s + (32 - len(s) % 32) * chr(32)        # function to pad the password 
paddedtext = pad(plaintext)

ciphertext = encryptor.encrypt(paddedtext)              #go ahead and encrypt it
print "Length after encryption =",len(ciphertext)

print "Generating the encrypted API KEY file located in: %r" % (partialpath)
f = open(os.path.join(partialpath + '_key.txt'),'w')
print "Writing encryption key to file..."
f.write(ciphertext)
f.close()

print "\n\nAttempting to verify encrypted files..."
f = open(os.path.join(partialpath + '_key.txt'),'r')
filedata = f.read()
f.close()
f = open(os.path.join(partialpath + '_salt.txt'),'r')
filesalt = f.read()
f.close()
typo=True
while typo==True:
    print "\nRe-enter your password to confirm:"
    newpassword = getpass.getpass()                     #Just to check for typos
    if newpassword == password:
        typo=False
    else:
        failed("Incorrect password!!!!")
hash_pass = hashlib.sha256(newpassword + filesalt).digest()
decryptor = AES.new(hash_pass, AES.MODE_CBC)            #create the AES container    

def failed (message):
    os.remove(os.path.join(partialpath + '_key.txt'))
    os.remove(os.path.join(partialpath + '_salt.txt'))
    print "Failed verification due to %r. Please re-run again." % (message)
    
print "File Read Verification Length = ",len(filedata)
if len(filedata)%16 == 0:
    try:
        filekeys = decryptor.decrypt(filedata)          #go ahead and decrypt the file
    except: 
        failed("Failed AES Decyption")
    try:
        data = json.loads(filekeys)                     #convert the string to a dict
    except:
        failed("Failed JSON Decoding")
    else:
        if data['key'] == key and data['secret'] == secret:
            print "\nPASSED Verification!!!!!!!!!!!!"
            print "\nDon't forget your password. This is what is REQUIRED to enable trading."
        else:
            failed("Failed API Key Verification")
else:
    failed("Length was not 160. Make sure Length=160 or some multiple of 16.")