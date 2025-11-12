# fermat_step_by_step.py
import math

def is_perfect_square(num):
    if num < 0: return False
    root = int(math.sqrt(num) + 0.5)
    return root * root == num

def fermat_factorization(n):
    if n <= 1 or n % 2 == 0: return None, 0
    x = math.ceil(math.sqrt(n))
    print(f"√{n} ≈ {math.sqrt(n):.3f} → x0 = {x}\n")
    steps = 0
    while True:
        steps += 1
        delta = x * x - n
        print(f"مرحله {steps}: {x}² - {n} = {delta}", end="")
        if is_perfect_square(delta):
            y = int(math.sqrt(delta) + 0.5)
            print(f" = {y}²  یافت شد!")
            p, q = x - y, x + y
            print(f"\n{n} = {x}² - {y}² = {p} × {q}")
            return (p, q), steps
        else:
            print("  (مربع کامل نیست)")
        x += 1

print("روش فرما — مرحله به مرحله")
print("="*50)
while True:
    try:
        inp = input("\nعدد فرد وارد کنید (یا 'خروج'): ").strip()
        if inp.lower() in ['خروج','exit','q']: break
        n = int(inp)
        factors, steps = fermat_factorization(n)
        if factors:
            print(f"تعداد مراحل: {steps}")
    except:
        print("ورودی نامعتبر!")