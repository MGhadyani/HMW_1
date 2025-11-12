import random

# تابع تشخیص اول بودن (بهینه)
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# تابع محاسبه ord_p(a)
def ord_p(a, p):
    if a % p != 0:
        return 0
    count = 0
    while a % p == 0:
        a //= p
        count += 1
    return count

# تابع تجزیه کامل به عوامل اول (با اطمینان از اول بودن همه عوامل)
def prime_factorization(n):
    if n <= 1:
        return {}
    factors = {}
    # عامل 2
    count = 0
    while n % 2 == 0:
        count += 1
        n //= 2
    if count > 0:
        factors[2] = count
    # اعداد فرد تا sqrt(n)
    f = 3
    while f * f <= n:
        count = 0
        while n % f == 0:
            count += 1
            n //= f
        if count > 0:
            factors[f] = count
        f += 2
    # اگر n > 1 باقی مانده
    if n > 1:
        # اگر اول است → اضافه کن
        if is_prime(n):
            factors[n] = 1
        else:
            # اگر مرکب است → تجزیه ادامه بده (با روش pollard یا ساده)
            # اینجا از روش ساده استفاده می‌کنیم
            sub_factors = factorize_large(n)
            for p, exp in sub_factors.items():
                factors[p] = factors.get(p, 0) + exp

    return factors


# تابع کمکی برای تجزیه اعداد بزرگ مرکب (روش ساده)
def factorize_large(n):
    factors = {}
    f = 3
    while f * f <= n:
        count = 0
        while n % f == 0:
            count += 1
            n //= f
        if count > 0:
            factors[f] = count
        f += 2
    if n > 1:
        if is_prime(n):
            factors[n] = 1
        else:
            # اگر هنوز مرکب بود، دوباره ادامه بده (نادر است)
            # می‌تونیم از روش Pollard Rho استفاده کنیم، ولی فعلاً ساده
            for i in range(f, int(n ** 0.5) + 1, 2):
                if n % i == 0:
                    factors[i] = factors.get(i, 0) + 1
                    n //= i
                    while n % i == 0:
                        factors[i] += 1
                        n //= i
            if n > 1:
                factors[n] = 1
    return factors


# تولید 100 عدد تصادفی
numbers = [random.randint(2, 10 ** 6) for _ in range(100)]

# پردازش
for num in numbers:
    original_num = num

    if is_prime(num):
        print(f"{num} : اول")
        continue

    factors = prime_factorization(num)

    # نمایش توان‌دار
    expr_parts = []
    for p, exp in sorted(factors.items()):
        if exp == 1:
            expr_parts.append(f"{p}")
        else:
            expr_parts.append(f"{p}^{exp}")
    factorization_str = " * ".join(expr_parts)

    # نمایش ord_p
    ord_parts = [f"ord{p}({original_num}) = {exp}" for p, exp in sorted(factors.items())]

    print(f"{original_num} : مرکب = {factorization_str}")
    print(f"     → {', '.join(ord_parts)}")
    print()