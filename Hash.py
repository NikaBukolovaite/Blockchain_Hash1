from Crypto.Cipher import AES
import os
import sys
from typing import Union

BLOCK = 16

IV_LEFT = bytes.fromhex("0123456789abcdeffedcba9876543210")
IV_RIGHT = bytes.fromhex("fedcba98765432100123456789abcdef")

FINAL_CONST = bytes.fromhex('ffffffffffffffffffffffffffffffff')

def pad_message(message: bytes) -> bytes:
    L = len(message)
    message_in_bits = L * 8
    padded = message + b'\x80'
    num_of_zeros = (16 - (len(padded) + 8) % 16) % 16
    padded += b'\x00' * num_of_zeros
    padded += message_in_bits.to_bytes(8, 'big')
    return padded
  
def xor_bytes(a: bytes, b: bytes) -> bytes:
  if len(a) != len(b):
      raise ValueError("Ilgiai turi sutapti")
  return bytes([x ^ y for x, y in zip(a, b)])

def aes_hashing(message: bytes) -> bytes:

    state_left = IV_LEFT
    state_right = IV_RIGHT
    padded_message = pad_message(message)

    for i in range(0, len(padded_message), BLOCK):
        Mi = padded_message[i:i + BLOCK]

        cipher = AES.new(state_left, AES.MODE_ECB)
        encrypted = cipher.encrypt(state_right)

        state_right = xor_bytes(encrypted, Mi)
        state_left, state_right = state_right, state_left

    cipher = AES.new(state_left, AES.MODE_ECB)
    final_enc = cipher.encrypt(FINAL_CONST)

    return final_enc

def choose_file(folder: str = "nuskaitymo_failai") -> bytes:
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        print("Aplankale nėra failų")
        sys.exit(1)

    for i, file in enumerate(files, start=1):
        print(f"{i} - {file}")

    while True:
        choice = input("Pasirinkite failą (numerį): ")
        try:
            index = int(choice) - 1
            file_path = os.path.join(folder, files[index])
            with open(file_path, "rb") as f:
                return f.read()
        except (IndexError, ValueError):
            print("Neteisingas pasirinkimas, bandykite dar kartą. ")
            continue

#Chat GPT hash

def toy_hash(data: Union[str, bytes], seed: int = 0) -> int:
    if isinstance(data, str):
        data = data.encode("utf-8")

    offset = 0xCBF29CE484222325
    prime = 0x100000001B3
    mask = (1 << 64) - 1

    h = (offset ^ (seed & mask)) & mask
    for b in data:
        h ^= b
        h = (h * prime) & mask
    return h


def toy_hash_hex(data: Union[str, bytes], seed: int = 0) -> str:
    return f"{toy_hash(data, seed):016x}"

def main():
    if len(sys.argv) > 1:
        if sys.argv[-1].lower() in ["--aes", "--toy"]:
            flag = sys.argv[-1].lower()
            file_paths = sys.argv[1:-1]
        else:
            flag = None
            file_paths = sys.argv[1:]

        if not file_paths:
            print("Nenurodytas nė vienas failas")
            sys.exit(1)

        global_choice = None
        if flag is None:
            while True:
                global_choice = input("Pasirinkite hash funkciją visiems failams (1 - AES, 2 - ChatGPT): ")
                if global_choice in ["1", "2"]:
                    break
                else:
                    print("Neteisinga įvestis, bandykite dar kartą.")

        # Apdorojam visus failus
        output_file = "output.txt"
        with open(output_file, "w") as outfile:
            for file_path in file_paths:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        user_message = f.read()
                else:
                    print("Tokio failo nėra:", file_path)
                    continue

                # Hash skaičiavimas
                if flag == "--aes" or global_choice == "1":
                    digest_hex = aes_hashing(user_message).hex()
                elif flag == "--toy" or global_choice == "2":
                    digest_hex = toy_hash_hex(user_message)

                outfile.write(f"{file_path}: {digest_hex}\n")
                print(f"Failas: {file_path}")
                print("Hash:", digest_hex)
                print("---")

        print("Visi hash išsaugoti faile:", output_file)
        return
    
    else:
        while True:
            choice = input("1 - Nastios ir Nikos hash, 2 - Chat gpt hash: ")

            if choice == "1":
                while True:
                    sub_choice = input("1 - ivedimas ranka, 2 - skaitymas is failo: ")

                    if sub_choice == "1":
                        user_message = input("Iveskite zinute: ").encode('utf-8')
                        break
                    elif sub_choice == "2":
                        user_message = choose_file("nuskaitymo_failai")
                        break
                    else:
                        print("Neteisinga įvestis, bandykite dar kartą.")

                digest_hex = aes_hashing(user_message).hex()
                break

            elif choice == "2":
                while True:
                    sub_choice = input("1 - įvedimas ranka, 2 - skaitymas iš failo: ")

                    if sub_choice == "1":
                        user_message = input("Įveskite žinutę ChatGPT hash skaičiavimui: ")
                        digest_hex = toy_hash_hex(user_message)
                        break
                    elif sub_choice == "2":
                        file_data = choose_file("nuskaitymo_failai")
                        digest_hex = toy_hash_hex(file_data)
                        break
                    else:
                        print("Neteisinga įvestis, bandykite dar kartą.")

                break

            else:
                print("Neteisinga įvestis, bandykite dar kartą.")

    output_file = "output.txt"
    with open(output_file, "w") as file:
        file.write(digest_hex)

    print("Hash:", digest_hex)
    print("Hash išsaugotas faile:", output_file)

if __name__ == "__main__":
    main()

