from argparse import ArgumentParser

import numpy as np


def mypow(r, a, p):
	res = 1
	for i in range(a):
		res = res * r % p
	return res


def keygen(p, g):
	# Каждый абонент выбирает свое секретное число ci, 1 < ci < p-1:
	c = np.array([np.random.randint(1, p-1) for i in range(3)])

	# По секретным ключам вычисляются открытые ключи di:
	d = [mypow(g, ci, p) for ci in c]

	return c, d
  

def table(c, d):
	# Получаем такую табличку абонентов:
	print('Абонент  Закр.ключ Откр.ключ')
	for i in range(c.size):
		print('  ', i, '      ', c[i], '      ', d[i])
	print()


def encryption(p, g, m, d):
	# Генерируем случайное число k:
	k = np.random.randint(1, p-2)
	print('k =', k)

	# Вычисляем пару (r, e):
	r = mypow(g, k, p)
	e = m * mypow(int(d), k, p) % p

	return r, e


def decryption(r, e, p, c):
	m = e * mypow(r, (p-1-c), p) % p
	return m


if __name__ == '__main__':
	# Выбираем 2 числа p и g:
	p = 113
	g = 31
	c, d = keygen(p, g)
	table(c, d)

	m = 54  # открытый текст, m < p
	B = 1   # номер абонента, которому хотим передать сообщение

	r, e = encryption(p, g, m, d[B])
	print('(r, e) = ', r, e)

	mm = decryption(r, e, p, c[B])
	print('Message = ', mm)
