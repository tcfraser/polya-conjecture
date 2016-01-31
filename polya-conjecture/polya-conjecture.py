import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import groupby

# Computer modern fonts
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

def prime_sieve(n):
    sqrt_n = int(math.sqrt(n))
    sieve = np.arange(0, n+1)
    sieve[1] = 0 # 1 is not prime

    for k in np.arange(2, sqrt_n):
        if sieve[k] != 0: # if hasn't been checked
            non_primes = np.arange(2*k, n+1, k)
            sieve[non_primes] = 0

    primes = [p for p in sieve if p != 0]

    return primes

def prime_factors(k, sieve):
    sqrt_k = math.sqrt(k)
    for p in sieve:
        if (p > sqrt_k):
            break
        if k % p == 0:
            return [p] + prime_factors(k // p, sieve)
    return [k]

def liouville(n_p_k):
    if n_p_k % 2 == 0:
        return 1
    else:
        return -1

def sum_liouville(n):
    sieve = prime_sieve(n)
    count = 0
    partial_sums = np.zeros(n)
    for k in np.arange(1, n+1):
        print("Progress: {0:.3}%".format(k/n * 100))
        p_fact = prime_factors(k, sieve)
        count += liouville(len(p_fact))
        partial_sums[k-1] = count

    return(count, partial_sums)

def factors_latex():
    start = 10
    stop = 100000

    sample = np.sort(np.random.choice(np.arange(start, stop), 15))

    sieve = prime_sieve(np.max(sample))

    latex_code_format = "| ${k}$ | ${fact}$ | ${count}$ | ${liouville}$ |"
    latex_code = ""

    for k in sample:
        p_fact = prime_factors(k, sieve)
        p_fact_multi = [(p, len(list(group))) for p, group in groupby(p_fact)]

        fact = ""
        for p_mul in p_fact_multi:
            if (len(fact) > 0):
                fact += "\cdot"
            p = p_mul[0]
            mul = p_mul[1]

            if (mul == 1):
                fact += "{p}".format(p=p)
            else:
                fact += "{p}^{mul}".format(p=p, mul=mul)

        count = len(p_fact)
        l = liouville(count)
        if l > 0:
            l = "+" + str(l)
        else:
            l = str(l)
        latex_code += latex_code_format.format(k=k, fact=fact, count=count, liouville=l)
        latex_code += "\n"
    return latex_code

def plot(n):
    k = np.arange(1, n+1)
    count, partial_sums = sum_liouville(n)
    plt.figure()
    plt.plot(k, partial_sums)

    plt.title(r'Summatory Liouville $T(n) = \sum_{k=1}^{n}L(k)$')
    plt.xlabel(r'$n$')
    plt.ylabel(r'$T(n)$')

    # plt.savefig('../figures/{n}.png'.format(n=n), dpi=800, format='png')
    plt.savefig('../figures/{n}_low_res.png'.format(n=n), dpi=150, format='png')
    # plt.savefig('../figures/{n}.svg'.format(n=n), format='svg')
    # plt.savefig('../figures/{n}.pdf'.format(n=n), format='pdf')
    plt.show()

# plot(100)
# plot(10000)
# plot(100000)
# plot(1000000)

print(factors_latex())
