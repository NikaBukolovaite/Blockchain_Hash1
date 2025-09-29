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

Eksperimentinis tyrimas testuoja hash funcijas – AES pagrįstą hash ir paprastą ,,toy“ hash – pagal pagrindinius hash'o kriterijus:

- Išvedimo dydis
- Deterministiškumas
- Efektyvumas
- Kolizijos
- Lavinos efektas
- Negrįžtamumas

Norint paleisti tyrimą į komandinę eilutę reikia įrašyti:

```bash
python test_hash.py
```

Rezultatai atsiras faile test_hash.py

# 💻 Kompiuterio charakteristikos (ant kurio buvo daromas eksperimentas)

| Komponentas |      Specifikacija      |
| :---------- | :---------------------: |
| CPU         | AMD Ryzen 5 4600H </br> |
| RAM         |     8GB DDR4 </br>      |
| DISK        |    SSD (NVMe) </br>     |

# Išvedimo dydis

Šis testas tikrina, ar hash funkcijos visada grąžina vienodo ilgio išvestį, neprilausomai nuo įvesties dydžio.

#### Išvedimo dydžio testo rezultatai

| Failas:         | nuskaitymo_failai/empty.txt | nuskaitymo_failai/one_symbol1.txt | nuskaitymo_failai/one_symbol2.txt | nuskaitymo_failai/one_symbol3.txt | nuskaitymo_failai/one_symbol4.txt | nuskaitymo_failai/random1.txt | nuskaitymo_failai/random2.txt | nuskaitymo_failai/similar1a.txt | nuskaitymo_failai/similar1b.txt | nuskaitymo_failai/similar2a.txt | nuskaitymo_failai/similar2b.txt |
| :-------------- | :-------------------------: | :-------------------------------: | :-------------------------------: | :-------------------------------: | :-------------------------------: | :---------------------------: | :---------------------------: | :-----------------------------: | :-----------------------------: | :-----------------------------: | :-----------------------------: |
| AES Hash ilgis: |        32 simboliai         |           32 simboliai            |           32 simboliai            |           32 simboliai            |           32 simboliai            |         32 simboliai          |         32 simboliai          |          32 simboliai           |          32 simboliai           |          32 simboliai           |          32 simboliai           |
| TOY Hash ilgis: |         16 simbolių         |            16 simbolių            |            16 simbolių            |            16 simbolių            |            16 simbolių            |          16 simbolių          |          16 simbolių          |           16 simbolių           |           16 simbolių           |           16 simbolių           |           16 simbolių           |

# Deterministiškumas

# Efektyvumas

# Kolizijų paieša

# Lavinos efektas

# Negrįžtamumo demonstracija

# Išvados
