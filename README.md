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

| Failas                            | AES Hash ilgis | TOY Hash ilgis | SHA-256 Hash ilgis |
| :-------------------------------- | :------------: | :------------: | :----------------: |
| nuskaitymo_failai/empty.txt       |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/one_symbol1.txt |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/one_symbol2.txt |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/one_symbol3.txt |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/one_symbol4.txt |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/random1.txt     |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/random2.txt     |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/similar1a.txt   |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/similar1b.txt   |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/similar2a.txt   |  32 simboliai  |  16 simbolių   |    64 simboliai    |
| nuskaitymo_failai/similar2b.txt   |  32 simboliai  |  16 simbolių   |    64 simboliai    |

# Deterministiškumas

Šis testas tikrina, ar pati įvestis išduoda identišką hash - testas kelis kartus hash'uoja tą patį failą ir tada lygina rezultatus. Jei abu hash deterministiniai, tai išvestis yra TRUE.

| Deterministiškumo testo rezultatas |      |
| :--------------------------------- | ---: |
| Deterministiškumas AES:            | True |
| Deterministiškumas TOY:            | True |

# Efektyvumas

Šis testas tikrina hash'avimo greitį augant įvesties dydžiui - matuojama, kiek laiko hash'uojamos ,,konstitucija.txt“ failo 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 ir tada viso failo eilutės. Testas buvo atliktas kelis kartus - lentelėje ir grafike vaizduojamas 3 testų vidurkis.

#### Efektyvumo testo rezultatas

| Eilučių kiekis             | AES Hash laikas (sek.) | TOY Hash laikas (sek.) | SHA-256 Hash laikas (sek.) |
| :------------------------- | :--------------------: | :--------------------: | :------------------------: |
| 1 eilutė                   |        0.000000        |        0.000458        |          0.000005          |
| 2 eilutės                  |        0.000000        |        0.000000        |          0.000001          |
| 4 eilutės                  |        0.000000        |        0.000000        |          0.000002          |
| 8 eilutės                  |        0.001257        |        0.000000        |          0.000001          |
| 16 eilučių                 |        0.000000        |        0.000000        |          0.000002          |
| 32 eilutės                 |        0.001002        |        0.001012        |          0.000002          |
| 64 eilutės                 |        0.002071        |        0.000000        |          0.000006          |
| 128 eilutės                |        0.004241        |        0.001027        |          0.000023          |
| 256 eilutės                |        0.010296        |        0.002012        |          0.000033          |
| 512 eilučių                |        0.023281        |        0.005755        |          0.000046          |
| Visas failas (789 eilutės) |        0.063517        |        0.009396        |          0.000071          |

![imagine alt](https://github.com/NikaBukolovaite/Blockchain_Hash1/blob/3e9493577cab06d3c538f03cdf0d4ff879d916a4/nuotraukos/0e7a51f1-c7f6-45fd-a15e-f763a0063519.jpg)

# Kolizijų paieša

Šis testas tirina, ar skirtingos įvestys gali duoti tą patį hash'ą. Yra sugeneruojama 100 000 atsitiktinių porų ir tikrinama, ar hash'ai sutampa.

#### Kolizijų paieškos testo rezultatas

| Vieno string poroje ilgis: | AES kolizijos | TOY kolizijos | SHA-256 kolizijos |
| :------------------------- | :-----------: | :-----------: | :---------------: |
| 10                         |       0       |       0       |         0         |
| 100                        |       0       |       0       |         0         |
| 500                        |       0       |       0       |         0         |
| 1000                       |       0       |       0       |         0         |

# Lavinos efektas

Šis testas tikrina ar pakeitus 1 simbolį įvestyje, hash pasikeičia reikšmingai ar ne. Testas sugeneruoja 100 000 poras kurių ilgis yra 100 ir tos poros skiriasi tik 1 simboliu. Tada šios poros hash'uojamos ir matuojamas hash skirtumo procentas (HEX ir bitų lygmenimis) - kuo didesnis procentas, tuo didesnis skirtumas.

#### Lavinos efekto testo rezultatai

| Koks skirtumas: | AES HEX | TOY HEX | SHA-256 HEX | AES BIT | TOY BIT | SHA-256 BIT |
| :-------------- | :-----: | :-----: | :---------: | :-----: | :-----: | :---------: |
| Vidutinis       | 93.77%  | 92.86%  |   93.76%    | 50.00%  | 49.52%  |   50.00%    |
| Minimalus       | 68.75%  | 25.00%  |   78.12%    | 31.25%  |  7.81%  |   37.11%    |
| Maksimalus      | 100.00% | 100.00% |   100.00%   | 67.97%  | 79.69%  |   63.67%    |

# Negrįžtamumo demonstracija

Šis testas tikrina, ar hash išvestis keičiasi pridėjus atsitiktinį ,,salt“ ir, ar yra sunku grąžinti į pradinę reikšmę. Šis testas hash'uoja tą pačią žinutę be ir su papildomu ,,salt“, todėl jei hash'ai yra visiškai sirtingi - tai įrodo, kad negrįžtamumos testas sėkmingas.

#### Negrįžtamumo testo rezultatai

| Parametras / Aprašymas |                                             Reikšmė / Rezultatas |
| :--------------------- | ---------------------------------------------------------------: |
| Originalus tekstas:    |                                LabaiSlaptasSlaptazodis1234567890 |
| Naudota salt:          |                                                          WRTv8WL |
| AES hash be salt:      |                                 85d811f4e14454723aee506a64f25139 |
| AES hash su salt:      |                                 7015b72a290f5f1d29308a9a5b0ded22 |
| TOY hash be salt:      |                                                 81ba629eb5263a7b |
| TOY hash su salt:      |                                                 95fa1e175659c697 |
| SHA-256 hash be salt:  | 916094e0c7ddc4333d862af6476c8fe46e187cc0fe89c15b24e98ac8e40dc4cb |
| SHA-256 hash su salt:  | cc0e98558f8ef2f23449752ae609dff3caee193f9f044f3a3a29ba0a8ca84c4e |
| AES skiriasi:          |                                                             True |
| TOY skiriasi:          |                                                             True |
| SHA-256 skiriasi:      |                                                             True |

# AES, TOY ir SHA-256 hash palyginimas

| Savybė              |                               AES Hash                                |                                TOY Hash                                 |          SHA-256 Hash          |
| :------------------ | :-------------------------------------------------------------------: | :---------------------------------------------------------------------: | :----------------------------: |
| Išvedimo ilgis      |                        32 simboliai(128 bitai)                        |                         16 simbolių (64 bitai)                          |    64 simboliai (256 bitai)    |
| Deterministiškumas  |                                  Yra                                  |                                   Yra                                   |              Yra               |
| Greitis             | Lėtesnis (789 eilučių failą hash'uoja vidutiniškai per 0.043517 sek.) | Greitesnis (789 eilučių failą hash'uoja vidutiniškai per 0.009396 sek.) | Labai greitas (~0.000000 sek.) |
| Kolizijų atsparumas |                             Labai aukštas                             |                              Labai aukštas                              |         Labai aukštas          |
| Lavinos efektas     |                              Labai geras                              |                               Gana geras                                |          Labai geras           |
| Negrįžtamumas       |                                Stiprus                                |                  Silpnesnis (daugiau simbolių sutampa)                  |         Labai stiprus          |

- AES hash – generuoja gana ilgą išvestį ir pasižymi stipriomis kriptografinėmis savybėmis. Jis lėtesnis už TOY, bet užtikrina geresnį lavinos efektą ir atsparumą atakoms.
- TOY hash – žymiai greitesnis ir lengvesnis, tačiau dėl trumpesnės išvesties ir didesnio lavinos efekto svyravimo jis laikomas mažiau saugiu. Jis tiktų testavimui, eksperimentams ar mažiau svarbiems duomenims, bet ne realiose sistemose.
- SHA-256 hash – standartinis, plačiai pripažintas kriptografinis hash algoritmas. Jis pasižymi puikiu balansu tarp saugumo, našumo ir lavinos efekto. Tai saugiausias ir universaliausias pasirinkimas realioms sistemoms.

# Išvados

Po atliktų testų galime daryti aiškias išvadas apie trijų hash funkcijų – AES, TOY ir SHA-256 – savybes ir pritaikymą praktikoje. Visi jie atitinka pagrindinius hash funkcijų kriterijus: išvesties dydis yra pastovus, rezultatai deterministiniai, kolizijų nerasta, lavinos efektas ryškus, o atvirkštinis atkodavimas – neįmanomas.

SHA-256 išsiskiria kaip saugiausias sprendimas: jis generuoja ilgiausią išvestį, turi stipriausią lavinos efektą ir aukščiausią atsparumą atakoms. AES taip pat pasižymi aukštu saugumo lygiu ir patikimu veikimu, nors veikia šiek tiek lėčiau ir generuoja trumpesnį hash. Tuo tarpu TOY yra greičiausias, tačiau dėl trumpesnės išvesties ir silpnesnio negrįžtamumo jis tinkamiausias mokymosi ar eksperimentiniams tikslams.

Apibendrinant, šis tyrimas parodė, kad praktiniam naudojimui saugumo požiūriu optimaliausi yra SHA-256 ir AES, o TOY gali būti laikomas supaprastintu, edukaciniu pavyzdžiu.

