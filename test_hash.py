import os
import time
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

    for line in results:
        print(line)

    with open("test_output.txt", "w", encoding="utf-8") as fout:
        fout.write("\n".join(results))

    print("\nRezultatai išsaugoti faile: test_output.txt")

if __name__ == "__main__":
    run_tests()
