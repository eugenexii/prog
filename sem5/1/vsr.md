## Исследование модуля Matplotlib, создание документа с помощью Markdown

Matplotlib — библиотека на языке программирования Python для визуализации данных двумерной (2D) графикой (3D графика также поддерживается).

Версия 2.1.1 — последняя стабильная — требует Python версии 2.7 или от 3.4 и выше и версию NumPy от 1.7.1 и выше

Пакет поддерживает многие виды графиков и диаграмм:

* Графики (line plot)

* Диаграммы разброса (scatter plot)

* Столбчатые диаграммы (bar chart) и гистограммы (histogram)

* Круговые диаграммы (pie chart)

* Ствол-лист диаграммы (stem plot)

* Контурные графики (contour plot)

* Поля градиентов (quiver)

* Спектральные диаграммы (spectrogram)

Методы | Описание
------------ | -------------
plt.scatter() | маркер или точечное рисование
plt.plot() | ломаная линия
plt.text() | нанесение текста
plt.bar(), plt.barh(), plt.barbs(), broken_barh() | столбчатая диаграмма
plt.hist(), plt.hist2d(), plt.hlines | гистограмма
plt.pie() | круговая диаграмма
plt.boxplot() | "ящик с усами" (boxwhisker)
plt.errorbar() | оценка погрешности, "усы"
plt.contour() | изолинии;
plt.contourf() | изолинии с послойной окраской
plt.pcolor(), plt.pcolormesh() | псевдоцветное изображение матрицы (2D массива)
plt.imshow() | вставка графики (пиксели + сглаживание)
plt.matshow() | отображение данных в виде квадратов
plt.fill() | заливка многоугольника
plt.fill_between(), plt.fill_betweenx() | заливка между двумя линиями
plt.streamplot() | линии тока
plt.quiver() | векторное поле

### Пример

Следующий пример иллюстрирует построение графика:

```python
from pylab import *
plot(range(1, 20),
     [i * i for i in range(1, 20)], 'ro')
savefig('example.png')
show()
```

![Картинка](https://upload.wikimedia.org/wikipedia/ru/thumb/7/7c/Matplotlib_example_plot.png/400px-Matplotlib_example_plot.png)
