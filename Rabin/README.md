# Rabin cryptosystem

**Криптосистема Рабина** — асимметричная криптографическая система с открытым ключом, основанная на трудности поиска квадратных корней в кольце остатков по модулю составного числа. Разработан Майклом О. Рабином в 1979 г.

[Wiki](https://ru.wikipedia.org/wiki/%D0%9A%D1%80%D0%B8%D0%BF%D1%82%D0%BE%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0_%D0%A0%D0%B0%D0%B1%D0%B8%D0%BD%D0%B0)

Выбираются случайным образом 2 больших простых числа p и q. Причем, должно выполняться условие: `p ≡ q ≡ 3 mod 4`. Пара (p,q) является закрытым ключом системы.

В качестве открытого ключа берется произведение `n = p * q`.

Шифрование исходного сообщения происходит посимвольно с помощью открытого ключа, причем каждый символ должен быть представлен числом `m < n`. Шифротекст генерируется по следующей формуле:
	
	c = m^2 mod n

Собеседнику для расшифровки исходного сообщения необходимо знать закрытый ключ - пару `(p,q)`. Алгоритм расшифровки состоит из нескольких шагов:
	
	- вычисляются числа yp и yq по расширенному алгоритму Евклида из уравнения `yp * p + yq * q = 1`;
	- вычисляются квадратные корни c по модулям p и q:
		mp = c^((p+1)/4) mod p
		mq = c^((q+1)/4) mod q
	- используя китайскую теорему об остатках, находим 4 квадратных корня c по модулю n:
		r1 = (yp * p * mq + yq * q * mp) mod n
		r2 = n - r1
		r3 = (yp * p * mq - yq * q * mp) mod n
		r2 = n - r3
		
	- одно из этих 4-х чисел является истинным текстом.

Расшифровка текста кроме правильного приводит еще к трем ложным результатам. Это является главным неудобством криптосистемы Рабина. 

В данной реализации предполагается, что исходное сообщение представляет из себя текст на английском или русском языке с использованием цифр и специальных символов, коды которых в таблице Unicode находятся в диапазоне от 0 до 1111 (верхнюю границу можно взять больше, вплоть до максимально допустимого аргумента 1114111, но тогда может быть больше вариантов определения символов). Так, исходный текст находится однозначно в большинстве случаев.

Программа показывает, в каком виде передавалось бы зашифрованное сообщение абоненту, а также, как получатель по секретному ключу может восстановить исходное сообщение.


## Пример

	Исходное сообщение: Hello!
	p = 2963 
	q = 911 
	n = 2699293 


| Символ сообщения | Код символа | Шифротекст |        Найденные корни        | Выбранное значение |
|:----------------:|:-----------:|:----------:|:-----------------------------:|:------------------:|
| H | 72 | 5184 | 189560, 2509733, 72, 2699221 | 72 |
| e | 101 | 10201 | 2699192, 101, 2133461, 565832 | 101 |
| l | 108 | 11664 | 108, 2699185, 284340, 2414953 | 108 |
| l | 108 | 11664 | 108, 2699185, 284340, 2414953 | 108 |
| o | 111 | 12321 | 607526, 2091767, 2699182, 111 | 111 |
| ! | 33 | 1089 | 2699260, 33, 1712647, 986646 | 33 |


## Пример запуска:
	
	$ python3 main.py


## Дополнительные файлы:

	- prime_numbers.txt - список первых 500 простых чисел
	
 