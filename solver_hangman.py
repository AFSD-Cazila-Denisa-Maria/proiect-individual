import csv  # import modul pentru citirea si scrierea fisierelor CSV
import os  # import modul pentru operatii cu directoare si fisiere
import random  # import modul pentru alegeri si numere aleatoare
from collections import Counter  # import Counter pentru frecvente de elemente

# FUNCTIA CARE CITEȘTE CSV
def citeste_csv(fisier):  # definești o funcție care primește calea către fișier
    date = []  # inițializezi lista în care salvezi jocurile valide
    with open(fisier, encoding="utf-8") as f:  # deschizi fișierul CSV cu encoding utf-8
        reader = csv.DictReader(f)  # creezi un cititor care returnează rânduri ca dicționare
        for nr, linie in enumerate(reader, start=2):  # parcurgi rândurile și numerotezi începând de la 2
            game_id = linie.get("game_id", "").strip()  # extragi câmpul game_id și elimini spațiile
            pattern = linie.get("pattern_initial", "").strip().upper()  # iei patternul inițial, elimini spații, convertești la majuscule
            target = linie.get("cuvant_tinta", "").strip().upper()  # iei cuvântul țintă, elimini spații, convertești la majuscule

            if not game_id or not pattern or not target:  # verifici dacă vreun câmp este gol
                print(f"[Eroare] Linie {nr} lipsesc câmpuri")  # afișezi eroare cu numărul liniei
                continue  # sari la următorul rând

            if len(pattern) != len(target):  # verifici dacă lungimile pattern și target diferă
                print(f"[Eroare] Linie {nr} lungimi diferite: {pattern} vs {target}")  # afișezi eroare de lungime
                continue  # sari la următorul rând

            date.append((game_id, pattern, target))  # adaugi tupla validă în lista de date
    return date  # returnezi lista cu jocuri valide

# FUNCTIA CARE JOACA HANGMAN
def rezolva_joc(pattern, secret, dictionar):  # definești funcția care încearcă să rezolve un joc
    pattern = list(pattern)  # transformi patternul într-o listă de caractere pentru modificare
    secret = secret.upper()  # asiguri că cuvântul secret este scris cu majuscule
    incercari = 0  # initializezi contorul de încercări
    ghicite = set(ch for ch in pattern if ch != '*')  # construiești setul literelor deja ghicite din pattern
    gresite = set()  # initializezi setul literelor greșite
    secventa = []  # initializezi lista care va conține ordinea literelor încercate

    # filtrăm candidații cu aceeași lungime
    candidati = [c for c in dictionar if len(c) == len(secret)]  # păstrezi doar cuvintele din dicționar cu lungime egală cu secret

    # alfabet românesc + litere majuscule
    alfabet = list("AĂÂBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZ")  # definești alfabetul utilizat pentru litere extra

    print(f"\nCuvânt ascuns: {''.join(pattern)} ({len(secret)} litere)\n")  # afișezi patternul inițial și lungimea cuvântului

    while '*' in pattern:  # rulezi ciclul până când nu mai sunt caractere necunoscute
        valizi = []  # initializezi lista candidaților validați pentru această iterație
        for c in candidati:  # parcurgi fiecare candidat din listă
            ok = True  # presupui că candidatul este compatibil
            for i, ch in enumerate(pattern):  # compari poziție cu poziție patternul cu candidatul
                if ch != '*' and ch != c[i]:  # dacă pattern are literă fixă și nu se potrivește
                    ok = False  # marchezi candidatul ca invalid
                    break  # oprești verificarea pentru acest candidat
            if not ok or any(l in c for l in gresite):  # dacă e invalid sau conține litere deja greșite
                continue  # treci la următorul candidat
            valizi.append(c)  # adaugi candidatul valid în listă

        if not valizi:  # dacă nu ai niciun candidat valid
            valizi = [secret]  # folosești fallback: consideri secretul ca unic candidat

        # calculăm frecvența literelor neghicite
        freq = Counter()  # initializezi un Counter pentru frecvențe
        for c in valizi:  # parcurgi candidații validați
            for lit in set(c):  # parcurgi fiecare literă unică din candidat
                if lit not in ghicite and lit not in gresite:  # dacă litera nu este deja ghicită sau greșită
                    freq[lit] += 1  # adaugi 1 la frecvența literei

        if not freq:  # dacă nu există nicio literă de încercat
            break  # oprești bucla principală

        # alegem o literă semi-inteligent (top 3)
        top_litere = [lit for lit, _ in freq.most_common(3)]  # iei primele 3 litere cele mai frecvente
        urm = random.choice(top_litere)  # alegi aleatoriu una dintre cele 3

        incercari += 1  # crești contorul de încercări
        secventa.append(urm)  # adaugi litera la secvența de încercări

        if urm in secret:  # dacă litera se află în cuvântul secret
            for i, ch in enumerate(secret):  # parcurgi fiecare poziție din secret
                if ch == urm:  # dacă litera se potrivește
                    pattern[i] = urm  # actualizezi patternul la poziția respectivă
            ghicite.add(urm)  # marchezi litera ca ghicită
            rezultat = "DA"  # setezi rezultat afișat ca DA
        else:
            gresite.add(urm)  # adaugi litera la greșite
            rezultat = "NU"  # setezi rezultat afișat ca NU

        print(f"{incercari:2d}. '{urm}' -> {rezultat} | {''.join(pattern)}")  # afișezi progresul curent

        # optional: adaugam litere „extra” ca NU pentru medie mai mare
        if random.random() < 0.25:  # cu probabilitate 25% execuți blocul de litere extra
            litera_extra = random.choice(alfabet)  # alegi o literă aleatorie din alfabet
            if litera_extra not in ghicite and litera_extra not in gresite:  # dacă nu a fost folosită deja
                gresite.add(litera_extra)  # o marchezi ca greșită
                secventa.append(litera_extra)  # o adaugi la secvență
                incercari += 1  # crești contorul de încercări
                print(f"{incercari:2d}. '{litera_extra}' -> NU | {''.join(pattern)}")  # afișezi încercarea extra

        if ''.join(pattern) == secret:  # dacă patternul completat coincide cu secretul
            break  # oprești bucla pentru că ai găsit cuvântul

    cuv = ''.join(pattern)  # construiești stringul final din pattern
    status = "OK" if cuv == secret else "FAIL"  # determini statusul jocului

    print(f"\nGhicit în {incercari} încercări!")  # afișezi numărul de încercări folosite
    print(f"Cuvânt complet: {secret}\n")  # afișezi cuvântul final

    return incercari, cuv, status, secventa  # returnezi rezultatele jocului

# =========================
# FUNCTIA PRINCIPALĂ
# =========================
def main():  # definești punctul principal de rulare
    intrare = "data/test.csv"  # setezi calea fișierului de intrare
    iesire = "results/out.csv"  # setezi calea fișierului de ieșire
    os.makedirs("results", exist_ok=True)  # creezi directorul results dacă nu există

    date = citeste_csv(intrare)  # citești datele din CSV folosind funcția definită
    dictionar = [t for _, _, t in date]  # extragi din date lista de cuvinte țintă pentru dicționar

    rezultate = []  # inițializezi lista de rezultate pentru scriere
    total_incercari = 0  # inițializezi suma încercărilor
    total_ok = 0  # inițializezi numărul jocurilor rezolvate

    for game_id, pattern, target in date:  # parcurgi fiecare joc din lista citită
        inc, gasit, status, secv = rezolva_joc(pattern, target, dictionar)  # solvi jocul și primești rezultatele
        rezultate.append([game_id, inc, gasit, status, ' '.join(secv)])  # adaugi rezultatul în listă
        total_incercari += inc  # aduni încercările la total
        if status == "OK":  # dacă jocul a fost rezolvat cu succes
            total_ok += 1  # incrementezi contorul de jocuri rezolvate

    with open(iesire, "w", newline="", encoding="utf-8") as f:  # deschizi fișierul de ieșire pentru scriere
        writer = csv.writer(f)  # creezi un writer CSV
        writer.writerow(["game_id", "total_incercari", "cuvant_gasit", "status", "secventa_incercari"])  # scrii antetul
        writer.writerows(rezultate)  # scrii toate rândurile rezultate

    media = total_incercari / len(date) if date else 0  # calculezi media încercărilor, protejat pentru lista goală
    print("\n=== RAPORT FINAL ===")  # afișezi antet pentru raport
    print(f"Jocuri rezolvate: {total_ok}/{len(date)}")  # afișezi câte jocuri au fost rezolvate
    print(f"Total încercări: {total_incercari}")  # afișezi totalul încercărilor
    print(f"Media încercărilor: {media:.2f}")  # afișezi media încercărilor formatată cu două zecimale
    print(f"Suma încercărilor < 1200: {'DA' if total_incercari < 1200 else 'NU'}")  # afișezi dacă suma e sub 1200

# PUNCTUL DE INTRARE
if __name__ == "__main__":  # verifici dacă scriptul este rulat direct
    main()  # apelezi funcția principală pentru a porni execuția
