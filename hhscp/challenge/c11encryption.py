__author__ = 'ericdennison'

import random
from hhscp.codetest import CodeTest
import string
from io import StringIO

class Encryption(CodeTest):

    htmldescription = """
    This is the demo challenge description
    """


    def __init__(self):
        super(Encryption,self).__init__()
        # Create the stimulus input file
        self.testname = "c11encryption"
        assocs = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;'"+chr(34)+"/"+chr(92)+"<>(){}[]-=_+?!") * 2
        encode = lambda s: [assocs.find(c) for c in s]   # convert string to digits
        decode = lambda l: ''.join([assocs[n] for n in l]) # digits to chars to string
        keygen = lambda s, p: p*(len(s)//len(p)) + p[:len(s)%len(p)]    # generate a key of length = message
        encrypt = lambda s, k: [(sc+kc)%len(assocs) for sc,kc in zip(s,k)] # encrypt text, using key
        decrypt = lambda e, k: [(ec-kc)%len(assocs) for ec,kc in zip(e,k)]  # decrypt text, using key
        self.samplestrings = ["How now? A rat? Dead, for a ducat, dead!",
                      "Done to death by slanderous tongue",
                      "Why then tonight let us assay our plot",
                      "Thou art a votary to fond desire",
                      "Some Cupid kills with arrows, some with traps",
                      "Be not afraid of greatness",
                      "Lord, what fools these mortals be",
                      "Our remedies oft in ourselves do lie",
                      "I go, and it is done; the bell invites me"]
        self.samplekeys = ["password", 
                           "123456", 
                           "12345678", 
                           "abc123",
                           "qwerty",
                           "monkey",
                           "letmein",
                           "dragon",
                           "111111",
                           "baseball"]
        
        unrecognizedi = random.randint(0,5)
        s = ''
        for i in range(0,6):
            if i == unrecognizedi:
                s += random.choice('lmnoprs') + '\n'
            else:
                t = random.choice(self.samplestrings)
                p = random.choice(self.samplekeys)
                e = decode(encrypt(encode(t),encode(keygen(t,p))))
                s += 'e\n' + t + '\n' + p + '\nd\n' + e + '\n' + p + '\n'
        s += 'q\n'
        # s += "z\ne\nTwo plus two = Five\nLorem ipsum\nd\n+KF;B(CH=NIZ}m;R\\Dt\nLorem ipsum\nq\n"
        self.infile = StringIO(s)

    def canonicalexample(self):
        return """
associations = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;'\\"/\\<>(){}[]-=_+?!" * 2

encode = lambda s: [associations.find(c) for c in s]   # convert string to digits
decode = lambda l: ''.join([associations[n] for n in l]) # digits to chars to string
keygen = lambda s, p: p*(len(s)//len(p)) + p[:len(s)%len(p)]    # generate a key of length = message
encrypt = lambda s, k: [(sc+kc)%len(associations) for sc,kc in zip(s,k)] # encrypt text, using key
decrypt = lambda e, k: [(ec-kc)%len(associations) for ec,kc in zip(e,k)]  # decrypt text, using key

while True:
    action = input("Enter e to encrypt, d to decrypt, or q to quit: ")
    # Quit
    if action == "q":
        print ("Goodbye!")
        break
    # Encrypt/Decrypt
    elif action in 'ed':
        msg = input("Message: ")
        key = input("Key: ") 
        if action == 'e':
            print (decode(encrypt(encode(msg),encode(keygen(msg,key)))) + '\\n')
        else:
            print (decode(decrypt(encode(msg),encode(keygen(msg,key)))) + '\\n')
    else:
        print ("Did not understand command, try again.\\n")
"""

    def postcheck(self):
        return """
"""


    def passes(self):
        return self.aresimilar()