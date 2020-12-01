import argparse

def encryption(text, keyword):
	ciphertext = text
	# Перепишем исходный текст в верхнем регистре: 
	text = text.upper()
	print('Plaintext: ', text, sep='\n')	
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

	return ciphertext


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('--textfile', '-t',
						default='myplaintext.txt',
						help='file with plaintext you want to encrypt')
	parser.add_argument('--key', '-k',
						default='krya',
						help='encryption key')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()
	with open(args.textfile, 'r') as f:
		plaintext = f.readline()	
	
	ciphertext = encryption(text=plaintext, keyword=args.key)

	print('Ciphertext:', ciphertext, sep='\n')
	
	
	