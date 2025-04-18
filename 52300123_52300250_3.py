import math
import time
from random import randint
import matplotlib.pyplot as plt

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
    p = generate_prime(100, 1000)
    q = generate_prime(100, 1000)
    while p == q:
        q = generate_prime(100, 1000)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = randint(3, phi - 1)
    while math.gcd(e, phi) != 1:
        e = randint(3, phi - 1)
    
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    """Mã hóa thông điệp"""
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    """Giải mã thông điệp"""
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

<<<<<<< HEAD
# Test chương trình và vẽ biểu đồ
=======
# Test
>>>>>>> e3ed4760751926b209984e2cfb3573b3dcb988b9
if __name__ == "__main__":
    print("=== Tạo cặp khóa RSA ===")
    public_key, private_key = generate_keypair()
    print(f"Khóa công khai: {public_key}")
    print(f"Khóa riêng tư: {private_key}")
    
    # Test case
    test_messages = ["Hello", "Nguyen Hoang Sơn", "Nguyen Anh Kiet", "Cong nghe thong tin", "Ton Duc Thang University"]
    
    print("\n=== Kết quả kiểm tra ===")
    for message in test_messages:
        print(f"\nThông điệp gốc: {message}")
        encrypted_msg = encrypt(public_key, message)
        print(f"Thông điệp mã hóa: {encrypted_msg}")
        decrypted_msg = decrypt(private_key, encrypted_msg)
        print(f"Thông điệp giải mã: {decrypted_msg}")
        print(f"Kết quả đúng: {decrypted_msg == message}")
    
    print("\n=== Đo thời gian thực thi ===")
    time_data = []
    for message in test_messages:
        start_time = time.time()
        encrypted_msg = encrypt(public_key, message)
        encrypt_time = time.time() - start_time
        
        start_time = time.time()
        decrypted_msg = decrypt(private_key, encrypted_msg)
        decrypt_time = time.time() - start_time
        
        print(f"\nThông điệp: {message} (độ dài: {len(message)} ký tự)")
        print(f"Thời gian mã hóa: {encrypt_time:.6f} giây")
        print(f"Thời gian giải mã: {decrypt_time:.6f} giây")
        time_data.append((len(message), encrypt_time, decrypt_time))
    
    print("\n=== Phân tích thời gian (tọa độ x: độ dài, y: thời gian) ===")
    print("Độ dài\tMã hóa (s)\tGiải mã (s)")
    for length, enc_time, dec_time in time_data:
        print(f"{length}\t{enc_time:.6f}\t{dec_time:.6f}")
    
    # Vẽ biểu đồ
    print("\n=== Vẽ biểu đồ thời gian ===")
    lengths = [data[0] for data in time_data]
    enc_times = [data[1] for data in time_data]
    dec_times = [data[2] for data in time_data]
    
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, enc_times, marker='o', label='Thời gian mã hóa', color='blue')
    plt.plot(lengths, dec_times, marker='s', label='Thời gian giải mã', color='red')
    plt.xlabel('Độ dài thông điệp (ký tự)')
    plt.ylabel('Thời gian (giây)')
    plt.title('Thời gian mã hóa và giải mã RSA theo độ dài thông điệp')
    plt.legend()
    plt.grid(True)
    plt.show()