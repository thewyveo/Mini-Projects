# learned this from the computational intelligence course

import random

def estimate_pi(samples):
    inside_circle = 0

    for _ in range(samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)

        if x*x + y*y <= 1:
            inside_circle += 1

    return (inside_circle / samples) * 4


if __name__ == "__main__":
    n = int(input("sample amount: "))   # 1mil/10mil starts giving the first 3 digits -k
    pi_estimate = estimate_pi(n)
    print(f"estimated π after {n} samples: {pi_estimate}")
