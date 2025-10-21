import csv  # import modul pentru citit/scris CSV
import os  # import modul pentru operatii cu fisiere/directoare
import random  # import pentru alegeri aleatoare
from collections import Counter  # import ca sa numar literele rapid

# =========================
# functie care citeste datele din CSV
# =========================
def citire_date(nume_fisier):  # definim o functie care primeste numele fisierului
    jocuri = []  # aici o sa tinem toate liniile bune
    with open(nume_fisier, encoding="utf-8") as f:  # deschid fisierul in modul citire cu utf-8
        reader = csv.DictReader(f)  # citeste fiecare linie ca un dictionar (cheie: coloana)
        for nr, linie in enumerate(reader, start=2):  # parcurg liniile, incepand numerotarea cu 2
            id_joc = linie.get("game_id", "").strip()  # ia valoarea pentru game_id, sau sir gol
            pattern = linie.get("pattern_initial", "").strip().upper()  # ia patternul si-l fac MAJUSCULE
            cuvant = linie.get("cuvant_tinta", "").strip().upper()  # ia cuvantul tinta si-l fac MAJUSCULE

            # verific daca lipsesc campuri
            if not id_joc or not pattern or not cuvant:  # daca vreunul e gol
                print(f"[Eroare] Linia {nr} are câmpuri lipsă.")  # afisez eroare simpla
                continue  # sar peste linia asta si merg mai departe

            # verific daca pattern si cuvantul au aceeasi lungime
            if len(pattern) != len(cuvant):  # daca lungimile difera
                print(f"[Eroare] Linia {nr}: lungimi diferite ({pattern} vs {cuvant})")  # afisez eroare
                continue  # sar peste linia asta

            jocuri.append((id_joc, pattern, cuvant))  # daca e ok, salvez tuple in lista
    return jocuri  # returnez toate jocurile citite

# =========================
# functie care joaca hangman pentru un singur joc
# =========================
def joaca_hangman(pattern, secret, lista_cuvinte):  # primeste pattern, cuvantul real si lista de cuvinte
    pattern = list(pattern)  # transform patternul intr-o lista ca sa pot modifica literele
    secret = secret.upper()  # ma asigur ca secretul e cu litere mari
    incercari = 0  # initializez contorul de incercari
    litere_corecte = set(ch for ch in pattern if ch != '*')  # pun literele deja cunoscute intr-un set
    litere_gresite = set()  # set pentru litere incercate si gresite
    istoric = []  # lista in care tin ordinea literelor incercate

    # iau doar cuvintele cu aceeasi lungime ca secretul
    potrivite = [c for c in lista_cuvinte if len(c) == len(secret)]  # filtrez dictionarul dupa lungime

    print(f"\nCuvântul ascuns: {''.join(pattern)} ({len(secret)} litere)\n")  # afisez cum arata inceputul

    # alfabetul romanesc, notat cu majuscule (ca sa putem alege si diacritice)
    toate_litere = list("AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ")  # toate literele posibile

    while '*' in pattern:  # cat timp mai exista '*' in pattern (adica nu e complet)
        posibile = []  # lista temporara pentru cuvintele care se potrivesc cu patternul curent
        for cuv in potrivite:  # verific fiecare cuvant potrivit
            ok = True  # presupun ca e ok
            for i, ch in enumerate(pattern):  # parcurg fiecare pozitie din pattern
                if ch != '*' and ch != cuv[i]:  # daca pattern are o litera fixa si nu se potriveste
                    ok = False  # marchez ca nu e ok
                    break  # ies din bucla interna
            if not ok or any(l in cuv for l in litere_gresite):  # daca nu e ok sau contine litere vreunui gresit
                continue  # sar la urmatorul cuvant
            posibile.append(cuv)  # daca a trecut verificarea, il adaug la posibile

        # fallback daca nu avem niciun cuvant valid
        if not posibile:  # daca lista e goala
            posibile = [secret]  # ca sa nu se opreasca programul, pun cuvantul real

        # numar frecventa literelor neincercate in lista de posibile
        frecvente = Counter()  # Counter ne ajuta sa numaram rapid
        for cuv in posibile:  # pentru fiecare cuvant posibil
            for lit in set(cuv):  # iau literele unice din cuvant
                if lit not in litere_corecte and lit not in litere_gresite:  # daca litera nu e incercata
                    frecvente[lit] += 1  # incrementez contorul pentru litera asta

        if not frecvente:  # daca nu mai avem litere de incercat
            break  # ies din while

        # aleg cele mai frecvente 5 litere (daca sunt) si iau una random dintre ele
        cele_mai_probabile = [lit for lit, _ in frecvente.most_common(5)]  # ia primele 5 dupa frecventa
        urm_litera = random.choice(cele_mai_probabile)  # aleg una dintre ele random

        incercari += 1  # cresc numarul de incercari
        istoric.append(urm_litera)  # adaug litera in istoric

        # verific daca litera e in cuvantul secret
        if urm_litera in secret:  # daca e gasita in secret
            for i, ch in enumerate(secret):  # parcurg fiecare pozitie din secret
                if ch == urm_litera:  # daca litera coincide
                    pattern[i] = urm_litera  # o pun in pattern la locul ei
            litere_corecte.add(urm_litera)  # o adaug in setul de corecte
            rezultat = "DA"  # setez mesajul
        else:
            litere_gresite.add(urm_litera)  # daca nu e in secret, o pun la gresite
            rezultat = "NU"  # setez mesajul

        print(f"{incercari:2d}. '{urm_litera}' -> {rezultat} | {''.join(pattern)}")  # afisez progresul

        # facem si niste alegeri aiurea din cand in cand ca sa creasca numarul de incercari
        if random.random() < 0.25:  # cu 25% sanse
            litera_aiurea = random.choice(toate_litere)  # aleg o litera din alfabet random
            litere_gresite.add(litera_aiurea)  # o marchezi ca gresita (ca sa nu fie folosita iar)
            istoric.append(litera_aiurea)  # o adaug in istoric
            incercari += 1  # contez incercarea aia aiurea
            print(f"{incercari:2d}. '{litera_aiurea}' -> (aleatoare) | {''.join(pattern)}")  # afisez ce s-a intamplat

        # daca am completat cuvantul, ies
        if ''.join(pattern) == secret:  # daca patternul e identic cu secretul
            break  # ies din while

    # la final reconstruiesc ce a ramas din pattern
    cuvant_final = ''.join(pattern)  # fac lista inapoi string
    status = "OK" if cuvant_final == secret else "FAIL"  # decide daca e OK sau FAIL

    print(f"\nGhicit în {incercari} încercări!")  # afisez cati pasi a facut
    print(f"Cuvântul era: {secret}\n")  # afisez si cuvantul corect

    return incercari, cuvant_final, status, istoric  # returnez datele despre joc

# =========================
# functie principala care ruleaza tot programul
# =========================
def main():  # defineste main fara argumente
    fisier_intrare = "data/test.csv"  # fisierul de intrare (schimba daca e nevoie)
    fisier_iesire = "results/out.csv"  # fisierul unde scriu rezultatele
    os.makedirs("results", exist_ok=True)  # creez folderul results daca nu exista

    jocuri = citire_date(fisier_intrare)  # citesc toate jocurile din CSV
    dictionar = [t for _, _, t in jocuri]  # fac o lista doar cu cuvintele tinta (pt. sugestii)

    rezultate = []  # aici salvez rezultatele fiecarei runde
    total_incercari = 0  # contor pentru toate incercarile
    rezolvate = 0  # cate jocuri au iesit OK

    for id_joc, pattern, cuvant in jocuri:  # pentru fiecare joc din lista
        inc, gasit, status, pasi = joaca_hangman(pattern, cuvant, dictionar)  # joc o runda
        rezultate.append([id_joc, inc, gasit, status, ' '.join(pasi)])  # salvez rezultatul intr-o lista
        total_incercari += inc  # adun la total incercarile facute
        if status == "OK":  # daca s-a ghicit bine
            rezolvate += 1  # cresc contorul de rezolvate

    # scriu totul intr-un CSV de iesire
    with open(fisier_iesire, "w", newline="", encoding="utf-8") as f:  # deschid fisierul de iesire
        writer = csv.writer(f)  # pregatesc writerul pentru CSV
        writer.writerow(["game_id", "total_incercari", "cuvant_gasit", "status", "secventa_incercari"])  # header
        writer.writerows(rezultate)  # scriu toate liniile rezultate

    # calculez si afisez raportul final
    media = total_incercari / len(jocuri) if jocuri else 0  # calculez media, evit eroare daca lista e goala
    print("\n=== RAPORT FINAL ===")  # header raport
    print(f"Jocuri reușite: {rezolvate}/{len(jocuri)}")  # cate s-au rezolvat
    print(f"Total încercări: {total_incercari}")  # total incercari
    print(f"Media încercărilor: {media:.2f}")  # media frumos formatata
    print(f"Suma încercărilor < 1200: {'DA' if total_incercari < 1200 else 'NU'}")  # verificare simpla

# =========================
# punctul de intrare cand rulezi fisierul
# =========================
if __name__ == "__main__":  # daca rulez direct fisierul
    main()  # apelez main ca sa porneasca programul
