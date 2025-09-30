import os
import time
import random
import string
from Hash import aes_hashing, toy_hash_hex
import hashlib

def run_tests():
    files = [
        "nuskaitymo_failai/empty.txt", 
        "nuskaitymo_failai/one_symbol1.txt", 
        "nuskaitymo_failai/one_symbol2.txt", 
        "nuskaitymo_failai/one_symbol3.txt", 
        "nuskaitymo_failai/one_symbol4.txt", 
        "nuskaitymo_failai/random1.txt", 
        "nuskaitymo_failai/random2.txt", 
        "nuskaitymo_failai/similar1a.txt", 
        "nuskaitymo_failai/similar1b.txt", 
        "nuskaitymo_failai/similar2a.txt", 
        "nuskaitymo_failai/similar2b.txt"
    ]

    results = []


    def sha256_hash_hex(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    # Išvedimo dydžio testas
    results.append("---Išvedimo dydžio testas---")
    for f in files:
        if os.path.exists(f):
            with open(f, "rb") as file:
                data = file.read()

            aes_val = aes_hashing(data).hex()
            toy_val = toy_hash_hex(data)
            sha256_val = sha256_hash_hex(data)

            results.append(f"Failas: {f}")
            results.append(f"AES Hash ilgis: {len(aes_val)} simbolių")
            results.append(f"TOY Hash ilgis: {len(toy_val)} simbolių")
            results.append(f"SHA-256 Hash ilgis: {len(sha256_val)} simbolių")
            results.append("-" * 40)
        else:
            results.append(f"Failas nerastas: {f}")

    # Deterministiškumo testas
    results.append("\n---Deterministiškumo testas---")
    test_file = "nuskaitymo_failai/random1.txt"
    if os.path.exists(test_file):
        with open(test_file, "rb") as file:
            data = file.read()

        results.append(f"Deterministiškumas AES: {aes_hashing(data).hex() == aes_hashing(data).hex()}")
        results.append(f"Deterministiškumas TOY: {toy_hash_hex(data) == toy_hash_hex(data)}")
        results.append(f"Deterministiškumas SHA-256: {sha256_hash_hex(data) == sha256_hash_hex(data)}")
    else:
        results.append(f"Failas nerastas: {test_file}")

    # Efektyvumo testas
    results.append("\n---Efektyvumo testas---")
    test_file = "nuskaitymo_failai/konstitucija.txt"
    if os.path.exists(test_file):
        with open(test_file, "r", encoding="utf-8") as file:
            lines = file.readlines()

        n = 1
        while n <= len(lines):
            test_input = "".join(lines[:n]).encode("utf-8")

            start = time.time();
            aes_hashing(test_input);
            aes_time = time.time() - start
            start = time.time();
            toy_hash_hex(test_input);
            toy_time = time.time() - start
            start = time.time();
            sha256_hash_hex(test_input);
            sha256_time = time.time() - start

            results.append(
                f"Panaudota {n} eilučių, Baitų: {len(test_input)}, "
                f"AES: {aes_time:.6f}s, TOY: {toy_time:.6f}s, SHA-256: {sha256_time:.6f}s"
            )
            n *= 2

        full_input = "".join(lines).encode("utf-8")
        start = time.time();
        aes_hashing(full_input);
        aes_time = time.time() - start
        start = time.time();
        toy_hash_hex(full_input);
        toy_time = time.time() - start
        start = time.time();
        sha256_hash_hex(full_input);
        sha256_time = time.time() - start

        results.append(
            f"Visas failas ({len(lines)} eilučių, {len(full_input)} baitų), "
            f"AES: {aes_time:.6f}s, TOY: {toy_time:.6f}s, SHA-256: {sha256_time:.6f}s"
        )
    else:
        results.append(f"Failas nerastas: {test_file}")

     # --- Kolizijų paieškos testas ---
    results.append("\n---Kolizijų paieškos testas---")
    lengths = [10, 100, 500, 1000]
    for length in lengths:
        aes_collisions = 0
        toy_collisions = 0
        sha256_collisions = 0
        total_pairs = 100000  

        for _ in range(total_pairs):
            s1 = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')
            s2 = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')

            if s1 == s2:  # praleidžiam identiškus
                continue

            aes1 = aes_hashing(s1).hex()
            aes2 = aes_hashing(s2).hex()
            toy1 = toy_hash_hex(s1)
            toy2 = toy_hash_hex(s2)
            sha1 = sha256_hash_hex(s1)
            sha2 = sha256_hash_hex(s2)

            if aes1 == aes2:
                aes_collisions += 1
            if toy1 == toy2:
                toy_collisions += 1
            if sha1 == sha2:
                sha256_collisions += 1

        results.append(
            f"Ilgis: {length} simbolių, Iš viso porų: {total_pairs}, "
            f"AES kolizijos: {aes_collisions}, TOY kolizijos: {toy_collisions}, SHA-256 kolizijos: {sha256_collisions}"
        )

    # Lavinos efekto testas
    results.append("\n---Lavinos efekto testas---")

    total_pairs_to_test = 100000
    input_string_length = 100

    original_inputs = [
        ''.join(random.choices(string.ascii_letters + string.digits, k=input_string_length))
        for _ in range(total_pairs_to_test)
    ]

    modified_inputs = []
    for original_input in original_inputs:
        original_list = list(original_input)
        position_to_change = random.randint(0, len(original_list) - 1)
        new_random_character = random.choice(string.ascii_letters + string.digits)

        while new_random_character == original_list[position_to_change]:
            new_random_character = random.choice(string.ascii_letters + string.digits)

        original_list[position_to_change] = new_random_character
        modified_inputs.append("".join(original_list))

    # AES
    aes_hex_diff_total = aes_hex_diff_min = aes_hex_diff_max = 0
    aes_bit_diff_total = aes_bit_diff_min = aes_bit_diff_max = 0
    aes_hex_diff_min = aes_bit_diff_min = 100.0

    # TOY
    toy_hex_diff_total = toy_hex_diff_min = toy_hex_diff_max = 0
    toy_bit_diff_total = toy_bit_diff_min = toy_bit_diff_max = 0
    toy_hex_diff_min = toy_bit_diff_min = 100.0

    # SHA-256
    sha_hex_diff_total = sha_hex_diff_min = sha_hex_diff_max = 0
    sha_bit_diff_total = sha_bit_diff_min = sha_bit_diff_max = 0
    sha_hex_diff_min = sha_bit_diff_min = 100.0

    for i in range(total_pairs_to_test):
        original_bytes = original_inputs[i].encode("utf-8")
        modified_bytes = modified_inputs[i].encode("utf-8")

        # AES
        aes_hash_original = aes_hashing(original_bytes).hex()
        aes_hash_modified = aes_hashing(modified_bytes).hex()

        # TOY
        toy_hash_original = toy_hash_hex(original_bytes)
        toy_hash_modified = toy_hash_hex(modified_bytes)

        # SHA-256
        sha_hash_original = sha256_hash_hex(original_bytes)
        sha_hash_modified = sha256_hash_hex(modified_bytes)

        # --- HEX lygmens skirtumai ---
        aes_hex_difference_percentage = sum(c1 != c2 for c1, c2 in zip(aes_hash_original, aes_hash_modified)) / len(
            aes_hash_original) * 100
        toy_hex_difference_percentage = sum(c1 != c2 for c1, c2 in zip(toy_hash_original, toy_hash_modified)) / len(
            toy_hash_original) * 100
        sha_hex_difference_percentage = sum(c1 != c2 for c1, c2 in zip(sha_hash_original, sha_hash_modified)) / len(
            sha_hash_original) * 100

        aes_hex_diff_total += aes_hex_difference_percentage
        toy_hex_diff_total += toy_hex_difference_percentage
        sha_hex_diff_total += sha_hex_difference_percentage

        aes_hex_diff_min = min(aes_hex_diff_min, aes_hex_difference_percentage)
        aes_hex_diff_max = max(aes_hex_diff_max, aes_hex_difference_percentage)
        toy_hex_diff_min = min(toy_hex_diff_min, toy_hex_difference_percentage)
        toy_hex_diff_max = max(toy_hex_diff_max, toy_hex_difference_percentage)
        sha_hex_diff_min = min(sha_hex_diff_min, sha_hex_difference_percentage)
        sha_hex_diff_max = max(sha_hex_diff_max, sha_hex_difference_percentage)

        # --- BIT lygmens skirtumai ---
        aes_bits_original = bin(int(aes_hash_original, 16))[2:].zfill(len(aes_hash_original) * 4)
        aes_bits_modified = bin(int(aes_hash_modified, 16))[2:].zfill(len(aes_hash_modified) * 4)
        toy_bits_original = bin(int(toy_hash_original, 16))[2:].zfill(len(toy_hash_original) * 4)
        toy_bits_modified = bin(int(toy_hash_modified, 16))[2:].zfill(len(toy_hash_modified) * 4)
        sha_bits_original = bin(int(sha_hash_original, 16))[2:].zfill(len(sha_hash_original) * 4)
        sha_bits_modified = bin(int(sha_hash_modified, 16))[2:].zfill(len(sha_hash_modified) * 4)

        aes_bit_difference_percentage = sum(b1 != b2 for b1, b2 in zip(aes_bits_original, aes_bits_modified)) / len(
            aes_bits_original) * 100
        toy_bit_difference_percentage = sum(b1 != b2 for b1, b2 in zip(toy_bits_original, toy_bits_modified)) / len(
            toy_bits_original) * 100
        sha_bit_difference_percentage = sum(b1 != b2 for b1, b2 in zip(sha_bits_original, sha_bits_modified)) / len(
            sha_bits_original) * 100

        aes_bit_diff_total += aes_bit_difference_percentage
        toy_bit_diff_total += toy_bit_difference_percentage
        sha_bit_diff_total += sha_bit_difference_percentage

        aes_bit_diff_min = min(aes_bit_diff_min, aes_bit_difference_percentage)
        aes_bit_diff_max = max(aes_bit_diff_max, aes_bit_difference_percentage)
        toy_bit_diff_min = min(toy_bit_diff_min, toy_bit_difference_percentage)
        toy_bit_diff_max = max(toy_bit_diff_max, toy_bit_difference_percentage)
        sha_bit_diff_min = min(sha_bit_diff_min, sha_bit_difference_percentage)
        sha_bit_diff_max = max(sha_bit_diff_max, sha_bit_difference_percentage)

    # Rezultatai
    results.append(
        f"AES HEX vidutiniškai skiriasi: {aes_hex_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {aes_hex_diff_min:.2f}%, maksimalus skirtumas: {aes_hex_diff_max:.2f}%")
    results.append(
        f"TOY HEX vidutiniškai skiriasi: {toy_hex_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {toy_hex_diff_min:.2f}%, maksimalus skirtumas: {toy_hex_diff_max:.2f}%")
    results.append(
        f"SHA-256 HEX vidutiniškai skiriasi: {sha_hex_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {sha_hex_diff_min:.2f}%, maksimalus skirtumas: {sha_hex_diff_max:.2f}%")
    results.append(
        f"AES BIT vidutiniškai skiriasi: {aes_bit_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {aes_bit_diff_min:.2f}%, maksimalus skirtumas: {aes_bit_diff_max:.2f}%")
    results.append(
        f"TOY BIT vidutiniškai skiriasi: {toy_bit_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {toy_bit_diff_min:.2f}%, maksimalus skirtumas: {toy_bit_diff_max:.2f}%")
    results.append(
        f"SHA-256 BIT vidutiniškai skiriasi: {sha_bit_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {sha_bit_diff_min:.2f}%, maksimalus skirtumas: {sha_bit_diff_max:.2f}%")

    # Negrįžtamumo testas
    results.append("\n---Negrįžtamumo testas---")

    base_message = "LabaiSlaptasSlaptazodis1234567890"
    salt_length = random.randint(5, 15)
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=salt_length))

    # AES
    aes_hash_no_salt = aes_hashing(base_message.encode("utf-8")).hex()
    aes_hash_with_salt = aes_hashing((base_message + salt).encode("utf-8")).hex()

    # TOY
    toy_hash_no_salt = toy_hash_hex(base_message.encode("utf-8"))
    toy_hash_with_salt = toy_hash_hex((base_message + salt).encode("utf-8"))

    # SHA-256
    sha_hash_no_salt = sha256_hash_hex(base_message.encode("utf-8"))
    sha_hash_with_salt = sha256_hash_hex((base_message + salt).encode("utf-8"))

    # Rezultatai
    results.append(f"Originalus tekstas: {base_message}")
    results.append(f"Naudota salt: {salt}")

    results.append(f"AES hash be salt: {aes_hash_no_salt}")
    results.append(f"AES hash su salt: {aes_hash_with_salt}")
    results.append(f"TOY hash be salt: {toy_hash_no_salt}")
    results.append(f"TOY hash su salt: {toy_hash_with_salt}")
    results.append(f"SHA-256 hash be salt: {sha_hash_no_salt}")
    results.append(f"SHA-256 hash su salt: {sha_hash_with_salt}")

    results.append(f"AES skiriasi: {aes_hash_no_salt != aes_hash_with_salt}")
    results.append(f"TOY skiriasi: {toy_hash_no_salt != toy_hash_with_salt}")
    results.append(f"SHA-256 skiriasi: {sha_hash_no_salt != sha_hash_with_salt}")

    for line in results:
        print(line)

    with open("test_output.txt", "w", encoding="utf-8") as fout:
        fout.write("\n".join(results))

    print("\nRezultatai išsaugoti faile: test_output.txt")

if __name__ == "__main__":
        run_tests()
