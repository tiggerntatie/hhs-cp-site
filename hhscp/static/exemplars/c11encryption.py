associations = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;'\"/\\<>(){}[]-=_+?!" * 2

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
			print (decode(encrypt(encode(msg),encode(keygen(msg,key)))) + '\n')
		else:
			print (decode(decrypt(encode(msg),encode(keygen(msg,key)))) + '\n')
	else:
		print ("Did not understand command, try again.\n")