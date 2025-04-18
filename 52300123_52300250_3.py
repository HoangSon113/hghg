import math
import time
from random import randint

def is_prime(n):
    """Kiểm tra số nguyên tố"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def generate_prime(min_val, max_val):
    """Tạo số nguyên tố ngẫu nhiên trong khoảng [min_val, max_val]"""
    prime = randint(min_val, max_val)
    while not is_prime(prime):
        prime = randint(min_val, max_val)
    return prime

def mod_inverse(e, phi):
    """Tìm nghịch đảo modulo của e mod phi"""
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Không tìm thấy nghịch đảo modulo")

def generate_keypair():
    """Tạo cặp khóa công khai và riêng tư"""
    # Chọn hai số nguyên tố p, q
    p = generate_prime(100, 1000)
    q = generate_prime(100, 1000)
    while p == q:
        q = generate_prime(100, 1000)
    
    # Tính n = p * q và phi = (p-1) * (q-1)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Chọn e: 1 < e < phi, nguyên tố cùng nhau với phi
    e = randint(3, phi - 1)
    while math.gcd(e, phi) != 1:
        e = randint(3, phi - 1)
    
    # Tìm d: nghịch đảo modulo của e
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """Mã hóa thông điệp"""
    e, n = public_key
    # Chuyển plaintext thành số (ASCII) và mã hóa
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """Giải mã thông điệp"""
    d, n = private_key
    # Giải mã và chuyển về ký tự
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# Test chương trình
if __name__ == "__main__":
    print("Tạo cặp khóa RSA...")
    public_key, private_key = generate_keypair()
    print(f"Khóa công khai: {public_key}")
    print(f"Khóa riêng tư: {private_key}")
    
    # Test case
    test_messages = ["Hello", "RSA Test", "Cryptography", "Short", "VeryLongMessage123"]
    
    print("\nKết quả kiểm tra:")
    for message in test_messages:
        print(f"\nThông điệp gốc: {message}")
        # Mã hóa
        encrypted_msg = encrypt(public_key, message)
        print(f"Thông điệp mã hóa: {encrypted_msg}")
        # Giải mã
        decrypted_msg = decrypt(private_key, encrypted_msg)
        print(f"Thông điệp giải mã: {decrypted_msg}")
        # Kiểm tra
        print(f"Kết quả đúng: {decrypted_msg == message}")

# Đo thời gian
print("\nĐo thời gian thực thi:")
for message in test_messages:
    start_time = time.time()
    encrypted_msg = encrypt(public_key, message)
    encrypt_time = time.time() - start_time
    
    start_time = time.time()
    decrypted_msg = decrypt(private_key, encrypted_msg)
    decrypt_time = time.time() - start_time
    
    print(f"\nThông điệp: {message}")
    print(f"Thời gian mã hóa: {encrypt_time:.6f} giây")




