import numpy as np
import argparse
import json
import textwrap
import os
import sys

def U(x, m):
    return x / m

def st(x, a, b, m):
    return a + U(x, m) * b

def tr(x, a, b, m):
    y = []
    for i in range(0, len(x)-1, 2):
        y.append(a + b * (U(x[i], m) + U(x[i+1], m) - 1))
    return np.array(y)

def ex(x, a, b, m):
    return a - b * np.log(U(x, m))

def nr(x, a, b, m):
    y = []
    for i in range(0, len(x)-1, 2):
        y.append(a + b * np.sqrt(-2 * np.log(1 - U(x[i], m))) * np.cos(2 * np.pi * U(x[i+1], m)))
        y.append(a + b * np.sqrt(-2 * np.log(1 - U(x[i], m))) * np.sin(2 * np.pi * U(x[i+1], m)))
    return np.array(y)

def ln(x, a, b, m):
    return a + np.exp(b - nr(x, 0, 1, m))

def ls(x, a, b, m):
    u = U(x, m)
    return a + b * np.log(u / (1 - u))

def factor(x):
    y = 1
    for i in range(x):
        y *= (i + 1)
    return y

def bi(x, a, b, m):
    y = []
    u = U(x, m)
    for i in u:
        s = 0
        k = 0
        while(True):
            s += (factor(b) / (factor(k) * factor(b - k)) * (a ** k) * ((1 - a) ** (b - k)))
            if s > i:
                y.append(k)
                break
            if k < b - 1:
                k += 1
                continue
            y.append(b)
    return np.array(y)

def gm(x, a, b, c, m):
    y = []
    u = U(x, m)
    if type(c) == type(1):
        for i in range(0, len(u), c):
            y.append(a - b  * np.log(np.prod(1 - u[i:i+c])))
    else:
        k = int(c - 0.5)
        for i in range(0, len(u), 2 * k + 2):
            z1, z2 = nr([x[i], x[i+1]], 0, 1, m)
            y.append(a + b * (z1 ** 2 / 2 - np.log(np.prod(1 - u[i+2:i+k+2]))))
            y.append(a + b * (z2 ** 2 / 2 - np.log(np.prod(1 - u[i+k+2:i+2*k+2]))))
    return np.array(y)

class ArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(ArgumentParser, self).__init__(*args, **kwargs)
        self.program = { key: kwargs[key] for key in kwargs }
        self.options = []

    def add_argument(self, *args, **kwargs):
        super(ArgumentParser, self).add_argument(*args, **kwargs)
        option = {}
        option["flags"] = [ item for item in args ]
        for key in kwargs:
            option[key] = kwargs[key]
        self.options.append(option)

    def print_help(self):
        wrapper = textwrap.TextWrapper(width=80)

        if "usage" in self.program:
            print("Usage: %s" % self.program["usage"])
        else:
            usage = []
            for option in self.options:
                usage += [ "[%s %s]" % (item, option["metavar"]) if "metavar" in option else "[%s %s]" % (item, option["dest"].upper()) if "dest" in option else "[%s]" % item for item in option["flags"] ]
            wrapper.initial_indent = "Usage: %s " % os.path.basename(sys.argv[0])
            wrapper.subsequent_indent = len(wrapper.initial_indent) * " "
            output = str.join(" ", usage)
            output = wrapper.fill(output)
            print(output)
        print()

        if "description" in self.program:
            print(self.program["description"])
            print()

        print("Аргументы:")
        maxlen = 0
        for option in self.options:
            option["flags2"] = str.join(", ", [ "%s %s" % (item, option["metavar"]) if "metavar" in option else "%s %s" % (item, option["dest"].upper()) if "dest" in option else item for item in option["flags"] ])
            if len(option["flags2"]) > maxlen:
                maxlen = len(option["flags2"])
        for option in self.options:
            template = "  %-" + str(maxlen) + "s  "
            wrapper.initial_indent = template % option["flags2"]
            wrapper.subsequent_indent = len(wrapper.initial_indent) * " "
            if "help" in option and "default" in option:
                output = option["help"]
                output += " (по умолчанию: '%s')" % option["default"] if isinstance(option["default"], str) else " (по умолчанию: %s)" % str(option["default"])
                output = wrapper.fill(output)
            elif "help" in option:
                output = option["help"]
                output = wrapper.fill(output)
            elif "default" in option:
                output = "По умолчанию: '%s'" % option["default"] if isinstance(option["default"], str) else "Default: %s" % str(option["default"])
                output = wrapper.fill(output)
            else:
                output = wrapper.initial_indent
            print(output)

        print("\nКоды распределений:\n\tst – стандартное равномерное с заданным интервалом;\n\ttr – треугольное распределение;\n\tex – общее экспоненциальное распределение;\n\tnr – нормальное распределение;\n\tgm – гамма распределение;\n\tln – логнормальное распределение;\n\tls – логистическое распределение;\n\tbi – биномиальное распределение.")
        


if __name__ == "__main__":
    parser = ArgumentParser(description="Приведение последовательности чисел к определенному распределению", argument_default=argparse.SUPPRESS, allow_abbrev=False, add_help=False)
    parser.add_argument("-d", "--distribution", type=str, help="код распределения для преобразования последовательности")
    parser.add_argument("-f", "--filename", type=str, help="имя файла с входной последовательностью")
    parser.add_argument("-p1", "-a", type=float, help="1-й параметр, необходимый, для генерации ПСЧ заданного распределения")
    parser.add_argument("-p2", "-b", type=int, help="2-й параметр, необходимый, для генерации ПСЧ заданного распределения")
    parser.add_argument("-p3", "-c", type=int, default=None, help="3-й параметр, необходимый, для генерации ПСЧ гамма-распределением")
    parser.add_argument("-h", "--help", action="help", help="выводит это сообщение")
    args = parser.parse_args()
    m = 1024
    dist_dct = {"st": st, "tr": tr, "ex": ex, "nr":nr, "gm": gm, "ln":ln, "ls": ls, "bi":bi}
    with open(args.filename, 'r') as fr:
        nums = np.array(json.load(fr))
    if args.distribution == "gm":
        dist_nums = dist_dct[args.distribution](nums, args.p1, args.p2, args.p3, m)
    else:
        dist_nums = dist_dct[args.distribution](nums, args.p1, args.p2, m)
    np.savetxt(f"dist-{args.distribution}.dat", dist_nums, fmt='%1.4f')
    
