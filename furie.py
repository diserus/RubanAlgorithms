import math

from mycomplex import Complex

C = 5

op_count = 0


def reset_op_count():
    global op_count
    op_count = 0


def cmul(a, b):
    global op_count
    op_count += C
    return a * b


def dft(x):
    N = len(x)
    X = []
    for k in range(N):
        s = Complex(0.0, 0.0)
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            s += cmul(x[n], w)
        X.append(s / N)
    return X


def idft(X):
    N = len(X)
    x = []
    for n in range(N):
        s = Complex(0.0, 0.0)
        for k in range(N):
            angle = 2.0 * math.pi * k * n / N
            w = Complex(math.cos(angle), math.sin(angle))
            s += cmul(X[k], w)
        x.append(s)
    return x


if __name__ == "__main__":
    x = [1.0, 3.0, -2.0, 5.0, 0.0, -1.0, 4.0, -3.0]
    N = len(x)

    reset_op_count()
    X = dft(x)
    dft_ops = op_count
    print("x[n] =", x)
    print("\nПрямое ДПФ (X[k]):")
    for k, val in enumerate(X):
        print(f" X[{k}] = {val.real:8.4f} + {val.imag:8.4f}j")
    print("\nТрудоёмкость ДПФ:")
    print(f"  слагаемых: {N * N}, T = c * N^2 = {C} * {N}^2 = {dft_ops}")

    reset_op_count()
    x_rec = idft(X)
    idft_ops = op_count
    print("\nОбратное ДПФ:")
    for n, val in enumerate(x_rec):
        print(f" x[{n}] = {val.real:8.4f}")
    print("\nТрудоёмкость ОДПФ:")
    print(f"  слагаемых: {N * N}, T = c * N^2 = {C} * {N}^2 = {idft_ops}")
