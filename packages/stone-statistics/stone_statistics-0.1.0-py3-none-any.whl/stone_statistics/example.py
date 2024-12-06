import math
import re

from Stat import *


def get_list():
    result = []
    c = 0
    while True:
        i = input(f"{c}: ")
        c += 1
        if re.match(re.compile(r"fr"), i):
            i = input(f"{c}, (a.b), a: ")
            if i.isdigit():
                i2 = int(i)
                i = input(f"{c}, (a.b), b: ")
                if i.isdigit():
                    i = int(i)
                    result.append(Fraction(i2, i))
            continue
        if i.isdigit():
            result.append(Fraction(int(i), 1))
        # elif i.isdecimal():
        #     result.append(float(i))
        else:
            try:
                it = int(i)
                result.append(Fraction(it, 1))
            except (ValueError, KeyboardInterrupt):
                if re.match(re.compile(r"\d+\*\d+"), (s := re.sub(re.compile(" "), "", i))):
                    i3 = int(re.search(re.compile(r"\d+(?=\*)"), s).group())
                    c -= 1
                    for i2 in range(int(re.search(re.compile(r"(?<=\*)\d+"), s).group())):
                        result.append(Fraction(i3, 1))
                        c += 1
                elif re.match(re.compile(r"\d+[\\/]\d+"), (s := re.sub(re.compile(" "), "", i))):
                    i3 = int(re.search(re.compile(r"\d+(?=[\\/])"), s).group())
                    i2 = int(re.search(re.compile(r"(?<=[\\/])\d+"), s).group())
                    result.append(Fraction(i3, i2))
                else:
                    return result
                # try:
                #     it = float(i)
                #     result.append(it)
                # except (KeyboardInterrupt, ValueError):
                #     if re.match(re.compile(r"\d+\*\d+"), (s := re.sub(re.compile(" "), "", i))):
                #         i3 = int(re.search(re.compile(r"\d+(?=\*)"), s).group())
                #         c -= 1
                #         for i2 in range(int(re.search(re.compile(r"(?<=\*)\d+"), s).group())):
                #             result.append(i3)
                #             c += 1
                #     else:
                #         return result


def wrap(x: Fraction):
    return int(x) if int(x) == float(x) else float(x)


def factor(n):
    if (not isinstance(n, int)) or n < 0:
        return []
    elif n == 0 or n == 1:
        return [n]
    a = n
    result = []
    value = 2
    while value <= a:
        if a % value == 0:
            a //= value
            result.append(value)
        else:
            value += 1
    return result


if __name__ == '__main__':
    try:
        while True:
            l = get_list()
            l2 = l[:]
            print("------------------------------------------")
            size = len(l)
            if size == 0:
                break
            aver = average(l)
            s = sum(l)
            s3 = Fraction(0, 1)
            print("편차: ")
            l1 = [max(len(str(str(j - aver))), len(str(str(j)))) for j in l]
            string1 = ""
            string2 = ""
            for i in range(size):
                string1 += f"{{0:>{l1[i]}}}".format(str(l[i]))
                string2 += f"{{0:>{l1[i]}}}".format(str(l[i] - aver))
                if i != size - 1:
                    string1 += " | "
                    string2 += " | "
            print(string1)
            print(string2)
            print("편차의 제곱: ")
            l1 = [max(len(str(str((j - aver) ** 2))), len(str(str(j)))) for j in l]
            string1 = ""
            string2 = ""
            for i in range(size):
                string1 += f"{{0:>{l1[i]}}}".format(str(l[i]))
                string2 += f"{{0:>{l1[i]}}}".format(str((l[i] - aver) ** 2))
                if i != size - 1:
                    string1 += " | "
                    string2 += " | "
            print(string1)
            print(string2)
            print(f"평균: {aver}")
            print(f"중앙값: {median(l)}")
            m = mode(l)
            if m:
                print(f"최빈값: {m}")
            else:
                print(f"최빈값: 없음")
            del m
            print(f"총합: {s}")
            print(f"제곱의 총합: {sum([i ** 2 for i in l])}")
            s1 = square_sum(l)
            print(f"편차 제곱의 합: {s1}")
            print(f"분산: {breakup(l2)}")
            v1 = int(math.sqrt(s1 / size))
            v2 = math.sqrt(s1 / size)
            v = v1 if v2 == v1 else v2
            b = v2 == v1
            del v1, v2
            if s1 % size == 0:
                f3 = sorted(factor(s1 // size))
                f2 = sorted(list(set(f3)))
                f = {}
                for i in f2:
                    f[i] = f3.count(i)
                f3 = 1
                s = 1
                for i in f2:
                    f3 *= (i ** (f[i] // 2))
                    if f[i] % 2 == 1:
                        s *= i
                if f3 == 1:
                    if b:
                        print(f"표준편차: {v} <- √{s}")
                    else:
                        print(f"표준편차: {v:0.7f} <- √{s}")
                else:
                    if b:
                        print(f"표준편차: {v} <- {f3}√{s}")
                    else:
                        print(f"표준편차: {v:0.7f} <- {f3}√{s}")
            else:
                if b:
                    print(f"표준편차: {v} <- {f"√({s1 // size if s1 % size == 0 else s1 / size})"}")
                else:
                    print(f"표준편차: {v:0.7f} <- {f"√({s1 // size if s1 % size == 0 else s1 / size})"}")
    except KeyboardInterrupt:
        pass
