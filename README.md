# 💻 Hashing programa

Ši programa skaičiuoja maišos (hash) reikšmes duomenims, naudojant vieną iš dviejų metodų:

- Nastios ir Nikos AES\* pagrindu sukurta hash funkcija
- ChatGPT „toy hash“ (paprastas 64-bit nekriptografinis variantas)

\*AES reiškia „Advanced Encryption Standard“, tai simetrinis šifravimo metodas, kuris reiškia, kad tas pats raktas naudojamas informacijos šifravimui ir atšifravimui.

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

Šis testas tikrina, ar hash funkcijos visada grąžina vienodo ilgio išvestį, neprilausomai nuo įvesties dydžio - hash'uojami įvairaus dydžio failai ir tikrinamas hash ilgis.

#### Išvedimo dydžio testo rezultatai

| Failas:         | nuskaitymo_failai/empty.txt | nuskaitymo_failai/one_symbol1.txt | nuskaitymo_failai/one_symbol2.txt | nuskaitymo_failai/one_symbol3.txt | nuskaitymo_failai/one_symbol4.txt | nuskaitymo_failai/random1.txt | nuskaitymo_failai/random2.txt | nuskaitymo_failai/similar1a.txt | nuskaitymo_failai/similar1b.txt | nuskaitymo_failai/similar2a.txt | nuskaitymo_failai/similar2b.txt |
| :-------------- | :-------------------------: | :-------------------------------: | :-------------------------------: | :-------------------------------: | :-------------------------------: | :---------------------------: | :---------------------------: | :-----------------------------: | :-----------------------------: | :-----------------------------: | :-----------------------------: |
| AES Hash ilgis: |        32 simboliai         |           32 simboliai            |           32 simboliai            |           32 simboliai            |           32 simboliai            |         32 simboliai          |         32 simboliai          |          32 simboliai           |          32 simboliai           |          32 simboliai           |          32 simboliai           |
| TOY Hash ilgis: |         16 simbolių         |            16 simbolių            |            16 simbolių            |            16 simbolių            |            16 simbolių            |          16 simbolių          |          16 simbolių          |           16 simbolių           |           16 simbolių           |           16 simbolių           |           16 simbolių           |

# Deterministiškumas

Šis testas tikrina, ar pati įvestis išduoda identišką hash - testas kelis kartus hash'uoja tą patį failą ir tada lygina rezultatus. Jei abu hash deterministiniai, tai išvestis yra TRUE.

| Deterministiškumo testo rezultatas |      |
| :--------------------------------- | ---: |
| Deterministiškumas AES:            | True |
| Deterministiškumas TOY:            | True |

# Efektyvumas

Šis testas tikrina hash'avimo greitį augant įvesties dydžiui - matuojama, kiek laiko hash'uojamos ,,konstitucija.txt“ failo 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 ir tada viso failo eilutės. Testas buvo atliktas kelis kartus - lentelėje ir grafike vaizduojamas 3 testų vidurkis.

#### Efektyvumo testo rezultatas

| Eilučių kiekis:    | 1 eilutė | 2 eilutės | 4 eilutės | 8 eilutės | 16 eilutės | 32 eilutės | 64 eilutės | 128 eilutės | 256 eilutės | 512 eilutės | Visas failas (789 eilutės) |
| :----------------- | :------: | :-------: | --------- | --------- | ---------- | ---------- | ---------- | ----------- | ----------- | ----------- | -------------------------- |
| AES laikas (sek.): | 0.000000 | 0.000000  | 0.000000  | 0.001257  | 0.000000   | 0.001002   | 0.002071   | 0.004241    | 0.010296    | 0.023281    | 0.043517                   |
| TOY laikas (sek.): | 0.000458 | 0.000000  | 0.000000  | 0.000000  | 0.000000   | 0.001012   | 0.000000   | 0.001027    | 0.002012    | 0.005755    | 0.009396                   |

# Kolizijų paieša

Šis testas tirina, ar skirtingos įvestys gali duoti tą patį hash'ą. Yra sugeneruojama 100 000 atsitiktinių porų ir tikrinama, ar hash'ai sutampa.

#### Kolizijų paieškos testo rezultatas

| Vieno string poroje ilgis: | AES kolizijos | TOY kolizijos |
| :------------------------- | :-----------: | :-----------: |
| 10                         |       0       |       0       |
| 100                        |       0       |       0       |
| 500                        |       0       |       0       |
| 1000                       |       0       |       0       |

# Lavinos efektas

Šis testas tikrina ar pakeitus 1 simbolį įvestyje, hash pasikeičia reikšmingai ar ne. Testas sugeneruoja 100 000 poras kurių ilgis yra 100 ir tos poros skiriasi tik 1 simboliu. Tada šios poros hash'uojamos ir matuojamas hash skirtumo procentas (HEX ir bitų lygmenimis) - kuo didesnis procentas, tuo didesnis skirtumas.

#### Lavinos efekto testo rezultatai

| Koks skirtumas: | AES HEX | TOY HEX | AES BIT | TOY BIT |
| :-------------- | :-----: | :-----: | :-----: | :-----: |
| Vidutinis       | 93.77%  | 92.86%  | 50.00%  | 49.52%  |
| Minimalus       | 68.75%  | 25.00%  | 31.25%  |  7.81%  |
| Maksimalus      | 100.00% | 100.00% | 67.97%  | 79.69%  |

# Negrįžtamumo demonstracija

Šis testas tikrina, ar hash išvestis keičiasi pridėjus atsitiktinį ,,salt“ ir, ar yra sunku grąžinti į pradinę reikšmę. Šis testas hash'uoja tą pačią žinutę be ir su papildomu ,,salt“, todėl jei hash'ai yra visiškai sirtingi - tai įrodo, kad negrįžtamumos testas sėkmingas.

| Negrįžtamumo testo rezultatai |                                   |
| :---------------------------- | --------------------------------: |
| Originalus tekstas:           | LabaiSlaptasSlaptazodis1234567890 |
| Naudota salt:                 |                         lKS2dSRmQ |
| AES hash be salt:             |  85d811f4e14454723aee506a64f25139 |
| AES hash su salt:             |  5807982f06e01d42e5269c7b7f527811 |
| TOY hash be salt:             |                  81ba629eb5263a7b |
| TOY hash su salt:             |                  c418db9e0ea84a7a |
| AES skiriasi:                 |                              True |
| TOY skiriasi:                 |                              True |

# AES ir TOY hash palyginimas

| Savybė              |                               AES hash                                |                                TOY hash                                 |
| :------------------ | :-------------------------------------------------------------------: | :---------------------------------------------------------------------: |
| Išvedimo ilgis      |                        32 simboliai(128 bitai)                        |                         16 simbolių (64 bitai)                          |
| Deterministiškumas  |                                  Yra                                  |                                   Yra                                   |
| Greitis             | Lėtesnis (789 eilučių failą hash'uoja vidutiniškai per 0.043517 sek.) | Greitesnis (789 eilučių failą hash'uoja vidutiniškai per 0.009396 sek.) |
| Kolizijų atsparumas |                             Labai aukštas                             |                              Labai aukštas                              |
| Lavinos efektas     |                              Labai geras                              |                               Gana geras                                |
| Negrįžtamumas       |                                Stiprus                                |                  Silpnesnis (daugiau simbolių sutampa)                  |

- AES hash – saugesnis ir atsparesnis atakoms, nes turi ilgesnę išvestį, geresnį lavinos efektą ir aukštą negrįžtamumą.
- TOY hash – greitesnis, bet mažiau saugus, nes turi trumpesnę išvestį, bet ne toks geras lavinos efektas ir negrįžtamumas.

# Išvados

Atlikti testai patvirtina, kad abi funkcijos atitinka pagrindines hash savybes:

- Išvedimo dydis
- Deterministiškumas
- Efektyvumas
- Kolizijos
- Lavinos efektas
- Negrįžtamumas

Vis dėlto, dėl didesnio saugumo AES pagrįstas hash yra tinkamesnis.
