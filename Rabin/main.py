import numpy as np

def gcdex(p, q):
	if q == 0:
		return p, 1, 0
	else:
		d, x, y = gcdex(q, p % q)
	return d, y, x - y * (p // q)


def keygen(m):
	with open('prime_numbers.txt', 'r') as f:
		str_prime = f.read()
		prime_numbers = np.array([int(i) for i in str_prime.split(',') 
										 if int(i) % 4 == 3])
	p = int(np.random.choice(prime_numbers))
	q = int(np.random.choice(prime_numbers))
	n = p * q
	while q == p or n < m:
		q = int(np.random.choice(prime_numbers))
		n = p * q
	print(f'p = {p}, q = {q}, n = {n}')
	return p, q, n


def encryption(n, m):
	c = [mi ** 2 % n for mi in m]
	return c


def decryption(p, q, c):
	n = p * q
	# Вычисляем yp и yq по алгоритму Евклида:
	_, yp, yq = gcdex(p, q)

	mp = [pow(int(ci), (p+1)//4, p) for ci in c]
	mq = [pow(int(ci), (q+1)//4, q) for ci in c]

	m = np.zeros((4, len(c)))
	m[0] = [(yp * p * mqi + yq * q * mpi) % n for mqi, mpi in zip(mq, mp)]
	m[1] = n - m[0]
	m[2] = [(yp * p * mqi - yq * q * mpi) % n for mqi, mpi in zip(mq, mp)]
	m[3] = n - m[2]
	m = m.T

	answer = ''
	for row in m:
		cur_chars = set([chr(int(i)) for i in row if i < 1111])
		if len(cur_chars) == 1:
			answer += list(cur_chars)[0]
		else:
			answer += '[' + ','.join(cur_chars) + ']'
	return answer


if __name__ == '__main__':
	m = input('Your message for encryption: ')
	m = [ord(c) for c in m]
	print('Message: ', m)
	# Генерируем закрытый ключ (p,q) и открытый ключ n	
	p, q, n = keygen(max(m))

	c = encryption(n, m)
	print(f'Ciphertext = {c}')

	m = decryption(p, q, c)
	print(f'Found message: {m}')
	