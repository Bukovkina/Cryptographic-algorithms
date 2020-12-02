from argparse import ArgumentParser
from math import gcd
from collections import Counter

import numpy as np


def decryption(text):	
	textlen = len(text) # длина исходного текста

	alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
	n = len(alphabet) # длина алфавита

	# Находим длину кодового слова с пом. метода Казиского:
	keylen = kasiski(ciphertext, alphabet)
	print('Found key length:', keylen)
	
	# Применяем частотный анализ для нахождения ключа:
	keyword = frequency_analysis(ciphertext, keylen, alphabet)
	print('Found key word:', keyword)

	# Восстанавливаем исходный текст по ключу
	key = keyword * (textlen // keylen) + keyword[:(textlen % keylen)]
	foundtext = ''
	for m, k in zip(ciphertext, key):
		if m in alphabet:
			ind = (alphabet.index(m) - alphabet.index(k)) % n
			foundtext += alphabet[ind]
		else:
			foundtext += m

	with open('myfoundtext.txt', 'w') as f:
		f.write(foundtext)

	return foundtext


def kasiski(ciphertext, alphabet):
	comb = dict()
	# Для каждой посл-сти из 6-ти (потому что исх. текст длинный) символов записываем их позиции в тексте
	curstr = ''
	for i, c in enumerate(ciphertext):
		if c in alphabet:
			if len(curstr) < 6:
				curstr += c 
			else:
				curstr = curstr[1:] + c
				if curstr in comb:
					comb[curstr].append(i)
				else:
					comb[curstr] = [i]

	# Считаем расстояния между позициями повторяющихся посл-стей символов
	diff = []
	for value in comb.values():
		if len(value) > 1:
			for i in range(1, len(value)):
				diff.append(value[i] - value[i-1])

	# Считаем НОД расстояний
	pastgcd = diff[0]
	for i in range(1, len(diff)):
		curgcd = gcd(pastgcd, diff[i])
		if curgcd != 1:
			pastgcd = curgcd

	# Длина ключа равна полученному НОД
	return pastgcd


def frequency_analysis(ciphertext, keylen, alphabet):
	textlen = len(ciphertext)
	n = len(alphabet)
	# Разбиваем зашифрованный текст на нужное кол-во=keylen групп
	textgroups = [[] for i in range(keylen)]
	for i in range(keylen):
		for j in range(i, textlen, keylen):
			if ciphertext[j] in alphabet:
				textgroups[i].append(ciphertext[j])

	# В каждой группе подсчитываем, сколько раз там встретился каждый символ
	cnt = []
	for i in range(keylen):
		cnt.append(Counter(textgroups[i]).most_common())

	# Записываем вероятности для каждого символа в каждой группе
	frequencies = [{c : 0 for c in alphabet} for i in range(keylen)]
	for i in range(keylen):
		for c in cnt[i]:
			frequencies[i][c[0]] = c[1] / len(textgroups[i]) * 100
			
	# Частотность букв английского алфавита в тексте
	yal = np.array([8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07])
	
	# Применяем частотный анализ: считаем, какой сдвиг
	# наиболее похож на частотность букв англ. алфавита
	sums = [[] for i in range(keylen)]
	for i in range(keylen):
		gr = np.array(list(frequencies[i].values()))
		for _ in range(n):
			sums[i].append(sum((gr - yal) ** 2))
			gr = shift(gr)

	key = ''
	for s in sums:
		smin = np.array(s).argmin()
		key += alphabet[(n - smin) % n]
		
	return key
	

def shift(x):
	e = np.empty_like(x)
	e[0] = x[-1]
	e[1:] = x[:-1]
	return e


def parse_args():
	parser = ArgumentParser()
	parser.add_argument('--file', '-f',
						default='myciphertext.txt',
						help='file with ciphertext you want to decrypt')
	parser.add_argument('--quiet', '-q',
						default=False,
						help='do not display the text on command line',
						action='store_true')
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()
	
	try:
		with open(args.file, 'r') as f:
			ciphertext = f.read()	
	except IOError as e:
		print("File {} do not exists.".format(args.file))
	else: 
		ciphertext = ciphertext.upper()
		foundtext = decryption(text=ciphertext)
		if not args.quiet:
			print('Ciphertext:', ciphertext, sep='\n')
			print('Foundtext: ', foundtext, sep='\n')
