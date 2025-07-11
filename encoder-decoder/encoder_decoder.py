def generate_shifts(key):
    return [ord(c) % 26 for c in key]

def encode(text, key):
    shifts = generate_shifts(key)
    key_len = len(shifts)
    encoded = []

    for i, c in enumerate(text):
        if c.isalpha():
            shift = shifts[i % key_len]
            if c.islower():
                encoded.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
            else:
                encoded.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            encoded.append(c)  # (non-alphabetical characters stay the same)
    return ''.join(encoded)

def decode(text, key):
    shifts = generate_shifts(key)
    key_len = len(shifts)
    decoded = []

    for i, c in enumerate(text):
        if c.isalpha():
            shift = shifts[i % key_len]
            if c.islower():
                decoded.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
            else:
                decoded.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
        else:
            decoded.append(c)
    return ''.join(decoded)

if __name__ == "__main__":
    key = input("enter keyword: ").strip()
    choice = input("encode (e) or decode (d)? ").strip().upper()

    if choice.lower() == 'e':
        text = input("Enter text to encode: ")
        result = encode(text, key)
        with open("encoded.txt", "w") as f:
            f.write(result)
        print(f"encoded text saved to 'encoded.txt'")
    elif choice.lower() == 'd':
        try:
            with open("encoded.txt", "r") as f:
                enc_text = f.read()
            result = decode(enc_text, key)
            print("decoded text:")
            print(result)
        except FileNotFoundError:
            print("file 'encoded.txt' not found.")
    else:
        print("invalid choice. (e/d)")