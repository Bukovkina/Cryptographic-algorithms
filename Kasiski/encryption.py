from argparse import ArgumentParser

def encryption(text, keyword):	
	textlen = len(text) # длина исходного текста

	# Перепишем ключевое слово в верхний регистр:
	keyword = keyword.upper()
	# Перепишем ключ по длине исходного текста:
	key =  keyword * (textlen // len(keyword)) + keyword[:(textlen % len(keyword))]

	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	n = len(alphabet) # длина алфавита

	ciphertext = str()
	# Шифр Виженера:
	for m, k in zip(text, key):
		if m in alphabet:
			ind = (alphabet.index(m) + alphabet.index(k)) % n
			ciphertext += alphabet[ind]
		else:
			ciphertext += m

	with open('myciphertext.txt', 'w') as f:
		f.write(ciphertext)

	return ciphertext


def parse_args():
	parser = ArgumentParser()
	parser.add_argument('--textfile', '-t',
						default='myplaintext.txt',
						help='file with plaintext you want to encrypt')
	parser.add_argument('--key', '-k',
						default='krya',
						help='encryption key')
	parser.add_argument('--quiet', '-q',
						default=False,
						help='display the text on command line or not (False for display)')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()
	
	if args.quiet.lower() == 'true' or args.quiet == '1':
		quiet = True
	elif args.quiet.lower() == 'false' or args.quiet == '0':
		quiet = False
	else:
		quiet = False
	
	try:
		with open(args.textfile, 'r') as f:
			plaintext = f.read()	
	except IOError as e:
		print("File {} do not exists.".format(args.textfile))
	else: 
		plaintext = plaintext.upper()
		ciphertext = encryption(text=plaintext, keyword=args.key)
		if not quiet:
			print('Plaintext: ', plaintext, sep='\n')
			print('Ciphertext:', ciphertext, sep='\n')
