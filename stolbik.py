def stolbik(a, b, show=True):
    sign = -1 if (a < 0) != (b < 0) else 1
    a0, b0 = a, b                
    a, b = abs(a), abs(b)        

    result = 0
    shift = 0
    rows = []                   
    while b != 0:
        dig = b % 10
        b //= 10
        aa = a
        pos = 0
        row = 0
        perenos = 0
        while aa != 0 or perenos:
            dig2 = aa % 10
            num = dig * dig2 + perenos
            ost = num % 10
            perenos = num // 10
            row += ost * (10 ** pos)
            pos += 1
            aa //= 10
        if row:
            rows.append((row, shift))
        result += row * (10 ** shift)
        shift += 1

    result *= sign
    if show:
        print_column(a0, b0, rows, result)
    return result


def print_column(a, b, rows, result):
    a_str = str(a)
    b_str = "× " + str(b)
    row_strs = [str(row) + "0" * shift for row, shift in reversed(rows)]
    result_str = str(result)

    width = max([len(a_str), len(b_str), len(result_str)] + [len(s) for s in row_strs])
    sep = "-" * width

    print(a_str.rjust(width))
    print(b_str.rjust(width))
    print(sep)
    for s in row_strs:
        print(s.rjust(width))
    if row_strs:
        print(sep)
    print(result_str.rjust(width))


if __name__ == "__main__":
    for a, b in [(12345, 6789), (10000000, 4), (-123, 45), (12, -34), (-12, -34)]:
        stolbik(a, b)
        print()
