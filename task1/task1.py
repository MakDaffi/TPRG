import argparse
import tqdm
import json
import textwrap
import os
import sys

def get_bit(num, num_bit):
    return (num & ( 1 << num_bit )) >> num_bit

def set_bit(num, num_bit, bit):
    mask = 1 << num_bit
    num &= ~mask
    if bit:
        return num | mask
    else:
        return num
    
def shift(num, s):
    new_num = 0
    bit = 0
    for i in range(s):
        new_num = set_bit(new_num, i, bit)
        bit = get_bit(num, i)
    new_num = set_bit(new_num, 0, bit)
    return new_num

def lc(args=["1024", "1664525", "1013904223", "1"]):
    mod = int(args[0])
    a = int(args[1])
    b = int(args[2])
    seed = int(args[3])
    next = seed
    while(True):
        next = (next * a + b) % mod
        yield next

def add(args=[1024, 24, 55, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23, 517, 897, 480, 376, 94, 23]):
    mod = int(args[0])
    a = int(args[1])
    b = int(args[2])
    x = list(map(int, args[3:]))
    i = 55
    while(True):
        val = (x[i-a] + x[i-b]) % mod
        x.append(val)
        i += 1
        yield val

def lfsr(args=["100000001001001", "0011000000"]):
    s = len(args[1])
    y = int(args[1], 2)
    x = int(args[0], 2)
    while(True):
        cur_bit = 0
        for i in range(s):
            cur_bit ^= get_bit(x, i) * get_bit(y, i)
        y = shift(y, s)
        y = set_bit(y, 0, cur_bit)
        yield y


def fp(args=[87, 20, 40, 69, 9, 7716351738766551435189019318376542618311247]):
    p = int(args[0])
    param = list(map(int, args[1:4]))
    param.append(0)
    w = int(args[4])
    x = int(args[5])
    mask_w = 0
    for i in range(w):
        mask_w = set_bit(mask_w, i, 1)
    mask_p = 0
    for i in range(p):
        mask_p = set_bit(mask_p, i, 1)
    while(True):
        cur_bit = 0
        for i in param:
            cur_bit ^= get_bit(x, i)
        x = shift(x, p)
        x = set_bit(x, 0, cur_bit)
        x = x & mask_p
        yield x & mask_w

def nfsr(args=["100000001001001", "0011000000", "101011001001001", "11010011000000", "101100010001001", "10110000111"]):
    r1 = lfsr([args[0], args[3]])
    r2 = lfsr([args[1], args[4]])
    r3 = lfsr([args[2], args[5]])
    w1 = 0
    for i in range(int(args[6])):
        w1 = set_bit(w1, i, 1)
    while True:
        a = next(r1)
        b = next(r2)
        c = next(r3)
        yield (a ^ b + b ^ c + c) & w1

def rc4(args=[213,968,838,64,355,214,212,36,695,139,897,518,656,956,810,510,985,105,670,8,907,951,685,989,222,931,169,286,289,556,731,902,688,701,771,533,990,630,708,884,255,683,25,214,792,348,34,758,9,781,946,580,615,955,585,5,886,563,81,38,809,444,619,222,544,53,635,621,630,251,497,257,2,467,897,790,728,676,722,838,465,781,10,828,903,235,857,841,146,719,681,678,961,652,491,38,256,909,251,21,110,811,273,25,642,286,489,478,184,812,770,846,241,141,266,500,375,827,633,761,154,663,461,206,529,212,667,342,360,165,523,749,582,803,553,345,786,990,361,702,256,380,234,238,73,965,266,300,847,755,969,681,146,843,125,306,845,752,879,458,788,833,727,817,122,239,765,877,827,327,733,658,644,880,150,474,493,689,670,368,611,263,113,417,834,103,725,754,117,824,623,338,540,337,879,521,183,370,808,120,571,871,301,210,796,744,398,106,845,745,842,876,399,27,105,601,802,831,53,266,157,352,175,303,505,484,994,425,292,729,654,584,860,420,412,49,281,417,703,400,48,404,772,389,733,152,271,585,404,333,381,696,928,609,659,180,9]):
    k = list(map(int, args[:-2]))
    w = int(args[-1])
    l = len(k)
    s = [i for i in range(l)]
    j = 0
    for i in range(l):
        j = (j + s[i] + k[i]) % l
        s[i], s[j] = s[j], s[i]
    i = 0
    while(True):
        num = 0
        for t in range(w):
            i = (i + 1) % l
            j = (j + s[i]) % l
            s[i], s[j] = s[j], s[i]
            num = set_bit(num, t, s[(s[i] + s[j]) % l] & 1)
        yield num

def rsa(args=["12709189", "53", "245", "10"]):
    n = int(args[0])
    e = int(args[1])
    x = int(args[2])
    w = int(args[3])
    while(True):
        z = 0
        for i in range(w):
            x = x ** e % n
            z = set_bit(z, w - i - 1, x & 1)
        yield z

def bbs(args=["15621", "10"]):
    p = 127
    q = 131
    n = p * q
    x = int(args[0])
    w = int(args[1])
    while(True):
        z = 0
        for i in range(w):
            x = x * x % n
            z = set_bit(z, w - i - 1, x & 1)
        yield z

def mt(args=["1024","17461461673"]):
    p, w, r, q, a, u, s, t, l, b, c = 624, 32, 31, 397, 2567483615, 11, 7, 15, 18, 2636928640, 4022730752
    mod = int(args[0])
    lower_mask = (1 << r) - 1
    w1 = 0
    for i in range(w):
        w1 = set_bit(w1, i, 1)
    upper_mask = (~lower_mask * -1) & w1
    MT = [int(args[1])]
    for i in range(1, p):
        MT.append((MT[i - 1] ^ (MT[i - 1] >> 30)) + i)
    ind = p
    while(True):
        if (ind >= p):
            for i in range(p):
                x = (MT[i] & upper_mask) + (MT[(i + 1) % p] & lower_mask)
                xA = x >> 1
                if (x & 1):
                    xA ^= a
                MT[i] = MT[(i + q) % p] ^ xA
            ind = 0
        y = MT[ind]
        ind += 1
        y ^= (y >> u)
        y ^= (y << s) & b
        y ^= (y << t) & c
        y ^= (y >> l)
        yield y % mod

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

        print("\nМетоды генерации случайного числа:\n\tlc-линейный конгруэнтный метод;\n\tadd-адитивный метод;\n\t5p-пятипараметрический метод;\n\tlfsr-регистр сдвига с обратной связью(РСЛОС);\n\tnfsr-нелинейная комбинация РСЛОС;\n\tmt-Вихрь Мерсена;\n\trc4-RC4;\n\trsa-ГПСЧ на основе RSA;\n\tbbs-алгоритм Блюма-Блюма-Шуба;")
        print("\nПорядок элементов вектора параметров:\n\tlc-модуль, множитель, приращение, начальное значение\n\tadd-модуль, младший индекс, старший индекс, последовательность начальных значений\n\t5p-p,q1,q2,q3,w, начальное значение;\n\tlfsr-Двоичное представление вектора коэффициентов, начальное значение регистра;\n\tnfsr-параметры для R1,R2,R3,длина слова;\n\tmt-модуль, начальное значение x;\n\trc4-256 начальных значений, количество генерируемых бит;\n\trc4-модуль n, число e, w, начальное значение x;\n\tbbs-начальное значение x (взаимно простое с n),w-длина слова")


if __name__ == "__main__":
    parser = ArgumentParser(description="Генераторы случайных чисел.", argument_default=argparse.SUPPRESS, allow_abbrev=False, add_help=False)
    parser.add_argument("-g", "--generator", type=str, help="выбор генератора")
    parser.add_argument("-i", "--init", type=str, help="инициализационный вектор генератора (значения записываются через запятую)")
    parser.add_argument("-n", "--amount_of_numbers", type=int, default=10000, help="количество генерируемых чисел")
    parser.add_argument("-f", "--filename", type=str, default="random_sequence.dat", help="имя файла, в который записывается последовательность")
    parser.add_argument("-h", "--help", action="help", help="выводит это сообщение")
    args = parser.parse_args()
    gens_dct = {"lc": lc, "mt": mt, "add": add, "5p":fp, "lfsr": lfsr, "nfsr":nfsr, "rc4": rc4, "rsa":rsa, "bbs":bbs}
    gen = gens_dct[args.generator](args.init.split(sep=","))
    print("--!Генерация начата!--")
    ans = [next(gen) % 1024 for _ in tqdm.tqdm(range(args.amount_of_numbers))]
    print("--!Генерация завершена!--")
    print("--!Запись в файл...!--")
    with open(args.filename, 'w') as fw:
        json.dump(ans, fw)
    print("--!Запись в файл завершена!--")