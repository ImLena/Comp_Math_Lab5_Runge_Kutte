import logic


def input_params():
    print('Выберите уравнение:\n'
          '1. y\' + 2y - x^2 = 0\n'
          '2. y\' + 5ln(x) = 0\n'
          '3. y\' + 2xy = 0')
    t = float(input())
    print('Введите начальные условия через пробел (х0 у0)')
    x0, y0 = input().split()
    print('Введите конец отрезка')
    x1 = float(input())
    print('Введите точность')
    h = float(input())
    return float(x0), float(y0), x1, h, t


x0, y0, x1, h, t = input_params()
y, y_vals = logic.Runge_Kutte(x0, y0, x1, h, t)
print(y)
logic.get_graph(x0, x1, y_vals)
