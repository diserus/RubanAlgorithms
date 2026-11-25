INF = float("inf")


def fmt(x):
    return "∞" if x == INF else str(x)


def format_D(D_k):
    return "(" + ", ".join(fmt(x) for x in D_k) + ")"


def fmt_term(d, w):
    return f"{fmt(d)}+({fmt(w)})" if w < 0 else f"{fmt(d)}+{fmt(w)}"


def ford_bellman(C, v0=0):
    n = len(C)

    D = [[INF] * n]
    D[0][v0] = 0

    print(f"D^[0] = {format_D(D[0])}")

    k = 0
    while True:
        terms = [[D[k][j] + C[j][i] for j in range(n)] for i in range(n)]
        D.append([min(terms[i]) for i in range(n)])
        k += 1

        print(f"\nШаг {k}:")
        for i in range(n):
            summands = ", ".join(
                fmt_term(D[k - 1][j], C[j][i]) for j in range(n)
            )
            print(f"  D^[{k}]({i}) = min({summands}) = {fmt(D[k][i])}")
        print(f"  D^[{k}] = {format_D(D[k])}")

        if D[k] == D[k - 1]:
            print("\nСтабилизация: массив стоимостей перестал изменяться.")
            print("Получены кратчайшие расстояния от v0 до всех вершин.")
            return D, False

        if k >= n:
            print("\nСтабилизации нет — в графе есть цикл отрицательного веса.")
            return D, True


if __name__ == "__main__":
    C = [
        [0,   25,  15,   7,   2],
        [25,   0,   6, INF, INF],
        [15,   6,   0,   4, INF],
        [7,  INF,   4,   0,   3],
        [2,  INF, INF,   3,   0],
    ]

    print("Матрица стоимостей C(v_i, v_j):")
    for i, row in enumerate(C):
        print(f"  v{i}: {format_D(row)}")

    print()
    D, negative_cycle = ford_bellman(C)

    print("\nСтоимости переездов из вершины v0:")
    for i in range(len(C)):
        print(f"  v{i}: {format_D([D[k][i] for k in range(len(D))])}")

    print("\nКратчайшие расстояния от v0:")
    for i in range(len(C)):
        print(f"  до v{i}: {fmt(D[-1][i])}")

    print(f"\nЦикл отрицательного веса: {negative_cycle}")
