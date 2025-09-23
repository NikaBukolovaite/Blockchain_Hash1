# 💻 Hashing programa

Ši programa skaičiuoja maišos (hash) reikšmes duomenims, naudojant vieną iš dviejų metodų:

- Nastios ir Nikos AES pagrindu sukurta hash funkcija
- ChatGPT „toy hash“ (paprastas 64-bit nekriptografinis variantas)

Programa gali veikti tiek per komandinės eilutės argumentus, tiek per interaktyvų meniu.

# 📃 Naudojimo instrukcijos

## Programos paleidimas

### Paleidimas su vienu failu

```bash
> python Hash.py nuskaitymo_failai/konstitucija.txt --aes
```

- aes → naudoti Nastios ir Nikos AES pagrindu sukurta hash funkcija
- toy → naudoti ChatGPT „toy hash“

### Paleidimas su keliais failais

```bash
> python Hash.py nuskaitymo_failai/file1.txt nuskaitymo_failai/file2.txt --toy
```

Jei flag (--aes arba --toy) nenurodytas, programa vieną kartą paklaus, kurį algoritmą taikyti visiems failams:

```bash
> python Hash.py nuskaitymo_failai/file1.txt nuskaitymo_failai/file2.txt

Pasirinkite hash funkciją visiems failams (1 - AES, 2 - Toy):
```

### Paleidimas be argumentų (interaktyvus režimas)

```bash
python Hash.py
```

Programa paklaus:

- Kurį hash algoritmą naudoti (AES arba Toy)
- Ar žinutę įvesti ranka, ar pasirinkti failą iš aplanko nuskaitymo_failai/

### Klaidos atvejai

Jei failas nerandamas, programa klausia:

```bash
1 - pasirinkite kitą failą (iš nuskaitymo_failai/)
2 - įveskite žinutę ranka
```

Jei flag neteisingas, jis bus ignoruojamas ir algoritmą galėsite pasirinkti interaktyviai.
Jei nenurodytas nė vienas failas, programa persijungia į interaktyvų režimą.

### Rezultatai

Visi hash rezultatai įrašomi į failą output.txt.
Jei apdorojami keli failai, įrašai pateikiami eilutėmis:

```bash
nuskaitymo_failai/file1.txt: <hash>
nuskaitymo_failai/file2.txt: <hash>
```

# 🔬 Eksperimentinis tyrimas

# 💻 Kompiuterio charakteristikos (ant kurio buvo daromas eksperimentas)

| Komponentas |      Specifikacija      |
| :---------- | :---------------------: |
| CPU         | AMD Ryzen 5 4600H </br> |
| RAM         |     8GB DDR4 </br>      |
| DISK        |    SSD (NVMe) </br>     |

# Išvedimo dydis

# Deterministiškumas

# Efektyvumas

# Kolizijų paieša

# Lavinos efektas

# Negrįžtamumo demonstracija

# Išvados
