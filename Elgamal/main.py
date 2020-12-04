import random

import numpy as np


def keygen(p, g):
	# Генерируется закрытый ключ x, 1 < x < p-1:
	x = random.randint(2, p-2)
	# По секретному ключу вычисляется открытый ключ y:
	y = pow(g, x, p)
	return x, y


def encryption(p, g, m, y):
	# Генерируем случайное число k, 1 < k < p-1:
	k = random.randint(2, p-2)
	print(f'k = {k}')
	# Вычисляем пару (r, e):
	r = pow(g, k, p)
	e = m * pow(int(y), k, p) % p
	return r, e


def decryption(r, e, p, x):
	m = e * pow(r, (p-1-x), p) % p
	m = ''.join([chr(i) for i in m])
	return m


def gen_pg(m):
	with open('prime_numbers.txt', 'r') as f:
		str_prime = f.read()
		prime_numbers = np.array([int(i) for i in str_prime.split(',')])
	# p - простое число : p > m
	p = int(random.choice(prime_numbers[prime_numbers > m]))
	# g - случайное число : g < p, g - первообразный корень p
	g = random.randint(1, p-1)
	while not is_primitive_root(g, p):
		g = random.randint(1, p-1)
	print(f'p = {p}, g = {g}')
	return p, g


def is_primitive_root(g, p):
	primitive = True
	if pow(g, p-1, p) == 1:
		for i in range(1, p):
			if pow(g, i, p-1) == 1:
				primitive = False
				break
	else:
		primitive = False
	return primitive


if __name__ == '__main__':
	m = input('Your message for encryption: ')
	m = np.array([ord(c) for c in m])
	# Генерируем 2 числа p и g:
	p, g = gen_pg(max(m))
	# Вычисляем закрытый и открытый ключи:
	x, y = keygen(p, g)

	r, e = encryption(p, g, m, y)
	print(f'Ciphertext (r, e) = ({r}, {e})')

	mm = decryption(r, e, p, x)
	print(f'Found message = {mm}')

