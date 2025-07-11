import random
import string

def generate_password(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    if not (use_upper or use_lower or use_digits or use_symbols):
        raise ValueError("you have to enable at least one character type")

    char_pool = ""
    if use_upper:
        char_pool += string.ascii_uppercase
    if use_lower:
        char_pool += string.ascii_lowercase
    if use_digits:
        char_pool += string.digits
    if use_symbols:
        char_pool += string.punctuation

    return ''.join(random.choice(char_pool) for _ in range(length))


if __name__ == "__main__":
    length = int(input("password length: "))
    if length < 1:
        raise ValueError("provide a valid password length (integer)")
    upper = input("include uppercase letters? (y/n): ").lower() == 'y'
    lower = input("include lowercase letters? (y/n): ").lower() == 'y'
    digits = input("include digits? (y/n): ").lower() == 'y'
    symbols = input("include symbols? (y/n): ").lower() == 'y'

    password = generate_password(length, use_upper=upper, use_lower=lower, use_digits=digits, use_symbols=symbols)
    print(f"\n✅ Your generated password:\n{password}")