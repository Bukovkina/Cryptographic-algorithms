import numpy as np

def gcdex(p, q):
	if q == 0:
		return p, 1, 0
	else:
		d, x, y = gcdex(q, p % q)
	return d, y, x - y * (p // q)


def keygen():
	with open('prime_numbers.txt', 'r') as f:
		str_prime = f.read()
		prime_numbers = np.array([int(i) for i in str_prime.split(',')])
	x = []
	for i in prime_numbers:
		if i % 4 == 3:
			x.append(i)
	
	p = int(np.random.choice(x))
	while True:
		q = int(np.random.choice(x))
		if q != p:
			break

	n = p * q
	print(f'p = {p}, q = {q}, n = {n}')
	return p, q, n


def encryption(n, M):
	c = M ** 2 % n
	return c


def decryption(p, q, c):
	n = p * q
	d, yp, yq = gcdex(p, q)

	mp = pow(c, (p+1)//4, p)
	mq = pow(c, (q+1)//4, q)

	m = []
	m += [(yp * p * mq + yq * q * mp) % n]
	m += [n - m[0]]
	m += [(yp * p * mq - yq * q * mp) % n]
	m += [n - m[2]]

	return m


if __name__ == '__main__':
	p, q, n = keygen()

	M = 637284109 % n # M < n
	print('M =', M)

	C = encryption(n, M)
	print('C =', C)

	m = decryption(p, q, C)
	print(m)