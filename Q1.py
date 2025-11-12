import random
import math
import matplotlib.pyplot as plt

# --- تنظیم backend غیر-GUI (مهم!) ---
plt.switch_backend('Agg')  # این خط خیلی مهمه! بدون GUI کار می‌کنه

# -------------------------------------
def gcd(a, b):
    original_a, original_b = a, b
    a, b = abs(a), abs(b)
    if a < b:
        a, b = b, a
    steps = []
    u_a, v_a = 1, 0   # ضرایب a
    u_b, v_b = 0, 1   # ضرایب b
    iteration = 0
    final_u, final_v = 0, 0
    # --- سطر اول: r = a % b ---
    r = a % b
    steps.append((a, b, r, u_a, v_a))
    iteration += 1
    while r != 0:
        q = a // b
        new_r = a % b
        # ضرایب جدید برای r = a - q*b
        u_r = u_a - q * u_b
        v_r = v_a - q * v_b
        # ذخیره گام
        steps.append((a, b, new_r, u_a, v_a))
        # به‌روزرسانی
        a, b = b, new_r
        u_a, v_a = u_b, v_b
        u_b, v_b = u_r, v_r
        r = new_r
        iteration += 1
    # حالا a = gcd
    g = a
    # ضرایب نهایی: u_a, v_a (برای a = gcd)
    final_u, final_v = u_a, v_a
    # اصلاح علامت
    if original_a < 0:
        final_u = -final_u
    if original_b < 0:
        final_v = -final_v
    # سطر آخر: b = 0
    steps.append((g, 0, "", final_u, final_v))
    # --- چاپ جدول ---
    print("n   a     b     r     u     v")
    print("-" * 38)
    for i, step in enumerate(steps):
        a_val, b_val, r_val, u_val, v_val = step
        r_str = str(r_val) if r_val != "" else ""
        print(f"{i:<3} {a_val:<5} {b_val:<5} {r_str:<5} {u_val:<5} {v_val:<5}")
    print("-" * 38)
    # --- خروجی نهایی ---
    abs_u, abs_v = abs(final_u), abs(final_v)
    u_part = f"{final_u}*a" if final_u >= 0 else f"(-{abs_u})*a"
    v_part = f"{final_v}*b" if final_v >= 0 else f"(-{abs_v})*b"
    print(f"gcd = {u_part} + {v_part}")
    print(f"gcd({original_a}, {original_b}) = {g}")
    print(f"gcd = ({final_u})*{original_a} + ({final_v})*{original_b} = {g}")
    return g, final_u, final_v, iteration


def simulate_gcd_iterations(num_samples=100, max_val=100000):
    iterations = []
    log_bounds = []
    ratios = []
    print(f"\nشبیه‌سازی روی {num_samples} زوج تصادفی در بازه [1, {max_val}]...")
    for _ in range(num_samples):
        a = random.randint(1, max_val)
        b = random.randint(1, max_val)
        if a < b: a, b = b, a
        _, _, _, iters = gcd(a, b)
        iterations.append(iters)
        bound = math.log2(b) + 1
        log_bounds.append(bound)
        ratios.append(iters / bound if bound > 0 else 0)
    return iterations, log_bounds, ratios


def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1): a, b = b, a + b
    return b


def plot_analysis(iterations, log_bounds, ratios):
    plt.figure(figsize=(15, 10))

    # نمودار 1: توزیع تکرارها
    plt.subplot(2, 2, 1)
    max_iters = max(iterations)
    plt.hist(iterations, bins=range(1, max_iters + 2), alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(x=sum(iterations) / len(iterations), color='red', linestyle='--',
                label=f'میانگین: {sum(iterations) / len(iterations):.2f}')
    plt.title('Distribution of the number of repetitions of the Euclidean algorithm')
    plt.xlabel('Number of repetitions')
    plt.ylabel('Abundance')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # نمودار 2: تکرارها vs log(b)
    plt.subplot(2, 2, 2)
    plt.scatter(log_bounds, iterations, alpha=0.6, color='green', s=30)
    max_val = max(log_bounds)
    plt.plot([0, max_val], [0, max_val], 'r--', label='y = x')
    plt.title('Number of iterations versus log₂(b) + 1')
    plt.xlabel('log₂(b) + 1')
    plt.ylabel('Number of repetitions')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # نمودار 3: نسبت
    plt.subplot(2, 2, 3)
    plt.hist(ratios, bins=20, alpha=0.7, color='orange', edgecolor='black')
    plt.title('Ratio distribution (repetitions / (log₂(b)+1))')
    plt.xlabel('ratio')
    plt.ylabel('Abundance')
    plt.grid(True, alpha=0.3)

    # نمودار 4: فیبوناچی
    plt.subplot(2, 2, 4)
    fib_pairs = [(fib(n + 1), fib(n)) for n in range(5, 25)]
    fib_iters = []
    fib_logs = []
    for a, b in fib_pairs:
        _, _, _, iters = gcd(a, b)
        fib_iters.append(iters)
        fib_logs.append(math.log2(b) + 1)

    fib_x = [fib(n) for n in range(5, 25)]
    plt.plot(fib_x, fib_iters, 'o-', label='repeat', color='purple')
    plt.plot(fib_x, fib_logs, 'x--', label='log₂(b) + 1', color='red')
    plt.title('Worst case: Fibonacci numbers')
    plt.xlabel('b (Fibonacci number)')
    plt.ylabel('Number of repetitions / theoretical limit')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    # ذخیره فایل PNG
    plt.savefig("gcd_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()  # حتماً ببند
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
    iterations, log_bounds, ratios = simulate_gcd_iterations(100, 100000)
    print(f"\nمیانگین تعداد تکرارها: {sum(iterations) / len(iterations):.2f}")
    print(f"حداکثر تعداد تکرارها: {max(iterations)}")

    plot_analysis(iterations, log_bounds, ratios)
    print("\nتصویر در 'gcd_analysis.png' ذخیره شد.")