import time
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_key_pair(key_size=4096):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    public_key = private_key.public_key()
    return private_key, public_key

# Crypto
def encrypt_message(message, public_key):
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return ciphertext

# Decrypt
def decrypt_message(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return plaintext.decode()

# Đo thời gian
def measure_performance(messages, key_size=4096, trials=5):
    private_key, public_key = generate_rsa_key_pair(key_size)
    encrypt_times = []
    decrypt_times = []
    lengths = [len(msg) for msg in messages]
    
    for msg in messages:
        total_encrypt_time = 0
        total_decrypt_time = 0
        
        for _ in range(trials):
            # Mã hóa
            start_time = time.time()
            ciphertext = encrypt_message(msg, public_key)
            total_encrypt_time += time.time() - start_time
            
            # Giải mã
            start_time = time.time()
            decrypted_msg = decrypt_message(ciphertext, private_key)
            total_decrypt_time += time.time() - start_time
            
            assert decrypted_msg == msg, f"Giải mã thất bại cho thông điệp: {msg}"
        
        encrypt_times.append(total_encrypt_time / trials)
        decrypt_times.append(total_decrypt_time / trials)
        print(f"Độ dài {len(msg)} byte: Mã hóa mất = {encrypt_times[-1]:.6f}s, Giải mã mất = {decrypt_times[-1]:.6f}s")
    
    return lengths, encrypt_times, decrypt_times

# Vẽ biểu đồ
def plot_performance(lengths, encrypt_times, decrypt_times):
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, encrypt_times, label='Thời gian mã hóa', marker='o')
    plt.plot(lengths, decrypt_times, label='Thời gian giải mã', marker='s')
    plt.xlabel('Độ dài thông điệp (byte)')
    plt.ylabel('Thời gian (giây)')
    plt.title('Hiệu suất mã hóa/giải mã RSA theo độ dài thông điệp (Khóa 4096 bit)')
    plt.legend()
    plt.grid(True)
    plt.savefig('rsa_message_length_performance.png')
    plt.show()

def main():
    # Ví dụ
    messages = [
        "Nguyen Hoang Son",
        "Nguyen Anh Kiet",
        "Day la bai bao cao giua ky mon Cau Truc roi rac",
        "Truong Dai hoc Ton Duc Thang la truong dai hoc cong lap tu chu tai chinh." * 2,
    ]
    
    print("Kiểm tra RSA với thông điệp mẫu:")
    private_key, public_key = generate_rsa_key_pair()
    for msg in messages:
        print(f"\nThông điệp gốc: {msg}")
        ciphertext = encrypt_message(msg, public_key)
        print(f"Bản gốc: {ciphertext.hex()[:50]}... (độ dài {len(ciphertext)} byte)")
        decrypted_msg = decrypt_message(ciphertext, private_key)
        print(f"Giải mã: {decrypted_msg}")
        print(f"Kết quả: {'Thành công' if decrypted_msg == msg else 'Thất bại'}")
    
    # Đo hiệu suất
    print("\nĐo hiệu suất RSA với các độ dài thông điệp:")
    lengths, encrypt_times, decrypt_times = measure_performance(messages)
    
    # Vẽ biểu đồ
    print("\nBiểu đồ hiệu suất:")
    plot_performance(lengths, encrypt_times, decrypt_times)

if __name__ == "__main__":
    main()