import collections
import re
from collections import defaultdict
from math import gcd
from functools import reduce

# 英语字母频率，从A到Z
english_letter_freq = {'A': 8.2, 'B': 1.5, 'C': 2.8, 'D': 4.3, 'E': 13.0,
                       'F': 2.2, 'G': 2.0, 'H': 6.1, 'I': 7.0, 'J': 0.15,
                       'K': 0.77, 'L': 4.0, 'M': 2.4, 'N': 6.7, 'O': 7.5,
                       'P': 1.9, 'Q': 0.095, 'R': 6.0, 'S': 6.3, 'T': 9.1,
                       'U': 2.8, 'V': 0.98, 'W': 2.4, 'X': 0.15, 'Y': 2.0, 'Z': 0.074}


def kasiski_examination(ciphertext):
    spaced_repeats = defaultdict(list)

    for m in re.finditer(r'(?=([A-Z]{3,})).', ciphertext.upper()):
        spaced_repeats[m.group(1)].append(m.start())

    distances = []
    for positions in spaced_repeats.values():
        if len(positions) > 1:
            distances.extend(positions[i + 1] - positions[i] for i in range(len(positions) - 1))

    if distances:
        return reduce(gcd, distances)
    return 1

def decrypt_vigenere(ciphertext, key):
    decrypted_text = ""
    key_length = len(key)
    for i, char in enumerate(ciphertext):
        if char.upper() in english_letter_freq:
            shift = ord(key[i % key_length].upper()) - ord('A')
            decrypted_char = chr((ord(char.upper()) - shift - 65) % 26 + 65)
            decrypted_text += decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def chi_squared(test_text):
    # 计算文本中每个字母的频率
    counts = collections.Counter(test_text)
    chi_square_stat = 0
    for char, freq in english_letter_freq.items():
        observed = counts[char.upper()] + counts[char.lower()]
        expected = freq * len(test_text) / 100
        chi_square_stat += ((observed - expected) ** 2) / expected
    return chi_square_stat

def break_vigenere(ciphertext):
    key_length = kasiski_examination(ciphertext)
    best_key = ''
    best_chi, best_shift = float('inf'), 0
    for i in range(key_length):
        segment = ciphertext[i::key_length]
        for shift in range(26):
            decrypted_segment = decrypt_vigenere(segment, chr(shift + 65))
            chi = chi_squared(decrypted_segment)
            if chi < best_chi:
                best_chi, best_shift = chi, shift
        best_key += chr(best_shift + 65)
    print(f"Trying key length {key_length}: Best key is {best_key} with Chi-squared {best_chi}")
    print("Decrypted text:", decrypt_vigenere(ciphertext, best_key))
    print()
