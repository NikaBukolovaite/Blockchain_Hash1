import os
import time
import random
import string
from Hash import aes_hashing, toy_hash_hex

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

    # Išvedimo dydžio testas
    results.append("---Išvedimo dydžio testas---")
    for f in files:
        if os.path.exists(f):
            with open(f, "rb") as file:
                data = file.read()
            aes_hash_val = aes_hashing(data).hex()
            toy_hash_val = toy_hash_hex(data)

            results.append(f"Failas: {f}")
            results.append(f"AES Hash ilgis: {len(aes_hash_val)} simbolių")
            results.append(f"TOY Hash ilgis: {len(toy_hash_val)} simbolių")
            results.append("-" * 40)
        else:
            results.append(f"Failas nerastas: {f}")

    # Deterministiškumo testas
    results.append("\n---Deterministiškumo testas---")
    test_file = "nuskaitymo_failai/random1.txt"
    if os.path.exists(test_file):
        with open(test_file, "rb") as file:
            data = file.read()

        h1 = aes_hashing(data).hex()
        h2 = aes_hashing(data).hex()
        results.append(f"Deterministiškumas AES: {h1 == h2}")

        h3 = toy_hash_hex(data)
        h4 = toy_hash_hex(data)
        results.append(f"Deterministiškumas TOY: {h3 == h4}")
    else:
        results.append(f"Failas nerastas: {test_file}")
        
    # Efektyvumo testas
    results.append("\n---Efektyvumo testas---")
    test_file = "nuskaitymo_failai/konstitucija.txt"
    if os.path.exists(test_file):
        with open(test_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
               
        n = 1  # pradinis eilučių skaičius
        while n <= len(lines):
            test_input = "".join(lines[:n]).encode("utf-8")
             
            start = time.time()
            aes_hashing(test_input)
            end = time.time()
            aes_time = end - start
             
            start = time.time()
            toy_hash_hex(test_input)
            end = time.time()
            toy_time = end - start

            results.append(
                f"Panaudota {n} eilučių, Baitų: {len(test_input)}, "
                f"AES laikas: {aes_time:.6f}s, TOY laikas: {toy_time:.6f}s"
            )
            n *= 2
            
        full_input = "".join(lines).encode("utf-8")
        start = time.time()
        aes_hashing(full_input)
        end = time.time()
        aes_time = end - start

        start = time.time()
        toy_hash_hex(full_input)
        end = time.time()
        toy_time = end - start

        results.append(
            f"Visas failas ({len(lines)} eilučių, {len(full_input)} baitų), "
            f"AES laikas: {aes_time:.6f}s, TOY laikas: {toy_time:.6f}s"
        )

    else:
        results.append(f"Failas nerastas: {test_file}")
        
	# Kolizijų paieškos testas
    results.append("\n---Kolizijų paieškos testas---")
    lengths = [10, 100, 500, 1000]
    for length in lengths:
        aes_collisions = 0
        toy_collisions = 0
        total_pairs = 100000
        
        for _ in range(total_pairs):
            s1 = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')
            s2 = ''.join(random.choices(string.ascii_letters + string.digits, k=length)).encode('utf-8')

            if s1 == s2: #cia jei netycia sutampa string tai, kad praleistu ir neskaiciuotu kolizijos
                continue

            aes1 = aes_hashing(s1).hex()
            aes2 = aes_hashing(s2).hex()
            toy1 = toy_hash_hex(s1)
            toy2 = toy_hash_hex(s2)
        
            if aes1 == aes2:
                aes_collisions += 1
            if toy1 == toy2:
                toy_collisions += 1
                    
        results.append(
            f"Ilgis: {length} simbolių, Iš viso porų: {total_pairs}, "
            f"AES kolizijos: {aes_collisions}, TOY kolizijos: {toy_collisions}"
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

    aes_hex_diff_total = aes_hex_diff_min = aes_hex_diff_max = 0
    toy_hex_diff_total = toy_hex_diff_min = toy_hex_diff_max = 0
    aes_bit_diff_total = aes_bit_diff_min = aes_bit_diff_max = 0
    toy_bit_diff_total = toy_bit_diff_min = toy_bit_diff_max = 0
    aes_hex_diff_min = toy_hex_diff_min = aes_bit_diff_min = toy_bit_diff_min = 100.0

    for i in range(total_pairs_to_test):
        original_bytes = original_inputs[i].encode("utf-8")
        modified_bytes = modified_inputs[i].encode("utf-8")

        aes_hash_original = aes_hashing(original_bytes).hex()
        aes_hash_modified = aes_hashing(modified_bytes).hex()
        toy_hash_original = toy_hash_hex(original_bytes)
        toy_hash_modified = toy_hash_hex(modified_bytes)

        # hex lygmens skirtumai (% simbolių, kurie skiriasi)
        aes_hex_difference_percentage = sum(char_o != char_m for char_o, char_m in zip(aes_hash_original, aes_hash_modified)) / len(aes_hash_original) * 100
        toy_hex_difference_percentage = sum(char_o != char_m for char_o, char_m in zip(toy_hash_original, toy_hash_modified)) / len(toy_hash_original) * 100

        aes_hex_diff_total += aes_hex_difference_percentage
        toy_hex_diff_total += toy_hex_difference_percentage
        aes_hex_diff_min = min(aes_hex_diff_min, aes_hex_difference_percentage)
        aes_hex_diff_max = max(aes_hex_diff_max, aes_hex_difference_percentage)
        toy_hex_diff_min = min(toy_hex_diff_min, toy_hex_difference_percentage)
        toy_hex_diff_max = max(toy_hex_diff_max, toy_hex_difference_percentage)

        # bit lygmens skirtumai (% bitų, kurie skiriasi)
        aes_bits_original = bin(int(aes_hash_original, 16))[2:].zfill(len(aes_hash_original) * 4)
        aes_bits_modified = bin(int(aes_hash_modified, 16))[2:].zfill(len(aes_hash_modified) * 4)
        toy_bits_original = bin(int(toy_hash_original, 16))[2:].zfill(len(toy_hash_original) * 4)
        toy_bits_modified = bin(int(toy_hash_modified, 16))[2:].zfill(len(toy_hash_modified) * 4)

        aes_bit_difference_percentage = sum(bit_o != bit_m for bit_o, bit_m in zip(aes_bits_original, aes_bits_modified)) / len(aes_bits_original) * 100
        toy_bit_difference_percentage = sum(bit_o != bit_m for bit_o, bit_m in zip(toy_bits_original, toy_bits_modified)) / len(toy_bits_original) * 100

        aes_bit_diff_total += aes_bit_difference_percentage
        toy_bit_diff_total += toy_bit_difference_percentage
        aes_bit_diff_min = min(aes_bit_diff_min, aes_bit_difference_percentage)
        aes_bit_diff_max = max(aes_bit_diff_max, aes_bit_difference_percentage)
        toy_bit_diff_min = min(toy_bit_diff_min, toy_bit_difference_percentage)
        toy_bit_diff_max = max(toy_bit_diff_max, toy_bit_difference_percentage)

    results.append(f"AES HEX vidutiniškai skiriasi: {aes_hex_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {aes_hex_diff_min:.2f}%, maksimalus skirtumas: {aes_hex_diff_max:.2f}%")
    results.append(f"TOY HEX vidutiniškai skiriasi: {toy_hex_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {toy_hex_diff_min:.2f}%, maksimalus skirtumas: {toy_hex_diff_max:.2f}%")
    results.append(f"AES BIT vidutiniškai skiriasi: {aes_bit_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {aes_bit_diff_min:.2f}%, maksimalus skirtumas: {aes_bit_diff_max:.2f}%")
    results.append(f"TOY BIT vidutiniškai skiriasi: {toy_bit_diff_total / total_pairs_to_test:.2f}%, minimalus skirtumas: {toy_bit_diff_min:.2f}%, maksimalus skirtumas: {toy_bit_diff_max:.2f}%")

	# Negrįžtamumo testas
    results.append("\n---Negrįžtamumo testas---")

    base_message = "LabaiSlaptasSlaptazodis1234567890"
    salt_length = random.randint(5, 15)
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=salt_length))

    aes_hash_no_salt = aes_hashing(base_message.encode("utf-8")).hex()
    toy_hash_no_salt = toy_hash_hex(base_message.encode("utf-8"))

    aes_hash_with_salt = aes_hashing((base_message + salt).encode("utf-8")).hex()
    toy_hash_with_salt = toy_hash_hex((base_message + salt).encode("utf-8"))

    results.append(f"Originalus tekstas: {base_message}")
    results.append(f"Naudota salt: {salt}")
    results.append(f"AES hash be salt: {aes_hash_no_salt}")
    results.append(f"AES hash su salt: {aes_hash_with_salt}")
    results.append(f"TOY hash be salt: {toy_hash_no_salt}")
    results.append(f"TOY hash su salt: {toy_hash_with_salt}")
    results.append(f"AES skiriasi: {aes_hash_no_salt != aes_hash_with_salt}")
    results.append(f"TOY skiriasi: {toy_hash_no_salt != toy_hash_with_salt}")

    for line in results:
        print(line)

    with open("test_output.txt", "w", encoding="utf-8") as fout:
        fout.write("\n".join(results))

    print("\nRezultatai išsaugoti faile: test_output.txt")

if __name__ == "__main__":
    run_tests()
