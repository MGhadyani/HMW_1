import random
import math
import matplotlib.pyplot as plt

plt.switch_backend('Agg')   # برای اجرا بدون GUI

# ======================================================
#                 قسمت الف – تابع GCD توسعه‌یافته
# ======================================================
def gcd(a, b):
    original_a, original_b = a, b

    # اطمینان از کار روی مقدار مثبت
    a, b = abs(a), abs(b)

    # ضرایب اولیه برای a و b (طبق الگوریتم توسعه‌یافته)
    u1, v1 = 1, 0     # ضرایب مربوط به a
    u2, v2 = 0, 1     # ضرایب مربوط به b

    steps = []
    iteration = 0

    # چاپ اولین خط جدول
    print("\nn   a      b      r      u      v")
    print("-" * 45)

    while b != 0:
        r = a % b
        q = a // b   # خارج قسمت

        # ثبت گام فعلی قبل از به‌روزرسانی
        steps.append((a, b, r, u1, v1))

        # ضرایب جدید برای r = a - q*b
        ur = u1 - q * u2
        vr = v1 - q * v2

        # بروزرسانی برای تکرار بعد
        a, b = b, r
        u1, v1, u2, v2 = u2, v2, ur, vr

        iteration += 1

    # اکنون a = gcd است
    g = a
    final_u, final_v = u1, v1

    # اصلاح علامت‌ها با توجه به ورودی اولیه
    if original_a < 0:
        final_u = -final_u
    if original_b < 0:
        final_v = -final_v

    # چاپ جدول
    for i, step in enumerate(steps):
        print(f"{i:<3} {step[0]:<6} {step[1]:<6} {step[2]:<6} {step[3]:<6} {step[4]:<6}")

    # آخرین خط – b صفر شده
    print(f"{iteration:<3} {g:<6} {0:<6} {'':<6} {final_u:<6} {final_v:<6}")
    print("-"*45)

    # نمایش ترکیب خطی
    print(f"gcd({original_a}, {original_b}) = {g}")
    print(f"{g} = ({final_u})*{original_a} + ({final_v})*{original_b}")

    return g, final_u, final_v, iteration


# ======================================================
#         قسمت ب – شبیه‌سازی روی ۱۰۰ نمونه تصادفی
# ======================================================
def simulate_gcd_iterations(num_samples=100, low=10**5, high=10**7):
    iterations = []     # تعداد تکرار های واقعی الگوریتم برای هر زوج
    bounds_2log1 = []   # حد نظری: 2*log2(b) + 1
    ratios = []         # نسبت واقعی به نظری

    for _ in range(num_samples):
        a = random.randint(low, high)
        b = random.randint(low, high)

        if a < b: a, b = b, a
        _, _, _, iters = gcd(a, b)
        iterations.append(iters)  # تعداد تکرار های این زوج

        bound = 2 * math.log2(b) + 1    # <-- اینجا اصلاح شده: 2*log2(b) + 1
        bounds_2log1.append(bound)
        ratios.append(iters / bound if bound > 0 else 0)
    return iterations, bounds_2log1, ratios


def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1): a, b = b, a + b
    return b


def plot_analysis(iterations, bounds_2log1, ratios):
    plt.figure(figsize=(15, 10))

    # نمودار 1: توزیع تکرارها
    plt.subplot(2, 2, 1)
    max_iters = max(iterations)
    plt.hist(iterations, bins=range(1, max_iters + 2), alpha=0.7, edgecolor='black')
    avg_iters = sum(iterations) / len(iterations)
    plt.axvline(x=avg_iters, color='red', linestyle='--',
                label=f'میانگین: {avg_iters:.2f}')
    plt.title('Distribution of the number of repetitions of the Euclidean algorithm')
    plt.xlabel('Number of repetitions')
    plt.ylabel('Abundance')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # نمودار 2: تکرارها vs (2*log2(b)+1)
    plt.subplot(2, 2, 2)
    plt.scatter(bounds_2log1, iterations, alpha=0.6, s=30)
    max_val = max(bounds_2log1)
    # خط مرجع y = x (با محور x برابر حد نظری)
    plt.plot([0, max_val], [0, max_val], 'r--', label='y = x (2 log₂(b) + 1)')
    plt.title('Number of iterations versus 2·log₂(b) + 1')
    plt.xlabel('2·log₂(b) + 1')
    plt.ylabel('Number of repetitions')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # نمودار 3: نسبت
    plt.subplot(2, 2, 3)
    plt.hist(ratios, bins=20, alpha=0.7, edgecolor='black')
    plt.title('Ratio distribution (repetitions / (2·log₂(b)+1))')
    plt.xlabel('ratio')
    plt.ylabel('Abundance')
    plt.grid(True, alpha=0.3)

    # نمودار 4: فیبوناچی (بدترین حالت)
    plt.subplot(2, 2, 4)
    fib_pairs = [(fib(n + 1), fib(n)) for n in range(5, 25)]
    fib_iters = []
    fib_bounds = []
    for a, b in fib_pairs:
        _, _, _, iters = gcd(a, b)
        fib_iters.append(iters)
        fib_bounds.append(2 * math.log2(b) + 1)   # <-- همین حد نظری استفاده می‌شود

    fib_x = [fib(n) for n in range(5, 25)]
    plt.plot(fib_x, fib_iters, 'o-', label='تعداد تکرار (واقعی)')
    plt.plot(fib_x, fib_bounds, 'x--', label='2·log₂(b) + 1')
    plt.title('Worst case: Fibonacci numbers')
    plt.xlabel('b (Fibonacci number)')
    plt.ylabel('Number of repetitions / theoretical limit')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    # ذخیره فایل PNG
    plt.savefig("gcd_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("نمودارها با موفقیت در فایل 'gcd_analysis.png' ذخیره شد.")


if __name__ == "__main__":
    print("=== قسمت الف: الگوریتم اقلیدسی توسعه‌یافته ===")
    try:
        a = int(input("لطفاً عدد a را وارد کنید: "))
        b = int(input("لطفاً عدد b را وارد کنید: "))
        g, x, y, iters = gcd(a, b)
        print(f"\nتعداد تکرارهای حلقه اصلی: {iters}")
    except:
        print("ورودی نامعتبر!")

    print("\n" + "=" * 50)
    print("=== قسمت ب: شبیه‌سازی 100 نمونه تصادفی ===")
    iterations, bounds_2log1, ratios = simulate_gcd_iterations(100, 100000)
    print(f"\nمیانگین تعداد تکرارها: {sum(iterations) / len(iterations):.2f}")
    print(f"حداکثر تعداد تکرارها: {max(iterations)}")

    plot_analysis(iterations, bounds_2log1, ratios)
    print("\nتصویر در 'gcd_analysis.png' ذخیره شد.")
