from bruce_decrypt import break_vigenere

# 尝试打开并读取加密的.txt文件
try:
    with open('encrypted.txt', 'r') as file:
        ciphertext = file.read()
    break_vigenere(ciphertext)
except FileNotFoundError:
    print("Encrypted text file not found.")