print('Задание №1.2')

def arifmet():
  i, sum, k, n = 0, 0, 1, int(input('Введите количество членов арифметической прогрессии: '))
  while i < n:
    sum = sum + k
    k += 1
    i += 1
  print('Сумма членов арифметической прогрессии = ', sum)
arifmet()

print('\nЗадание №1.3')

import math

def treugol():
  a, b, c = int(input('Введите a: ')), int(input('Введите b: ')), int(input('Введите c: '))
  p = (a + b + c) / 2
  s = math.sqrt(p * (p - a) * (p - b) * (p - c))
  print('Площадь треугольника = ', s )
treugol()

print('\nЗадание №1.4')

a=float(input('Введите первое число: '))
b=float(input('Введите второе число: '))

def calc(a,b):
  print('\nСложение равно = ', a+b)
  print('Разность равна = ', a-b)
  print('Деление равно = ', a/b)
  print('Умножение равно = ', a*b)

calc(a,b)