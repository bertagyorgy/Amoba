import random
from replit import clear
from colorama import Fore, Style

# --- FÜGGVÉNYEK ---

# A pálya generálása adott méret alapján
def general_palya(meret):
    return [["." for _ in range(meret)] for _ in range(meret)]

# A pálya kiírása a képernyőre
def kiir_palya(tabla):
    clear()
    for sor in tabla:
        print(" ".join([Fore.RED + cella if cella == "X" else Fore.BLUE + cella if cella == "O" else Fore.WHITE + cella for cella in sor]))
    print(Style.RESET_ALL)

# Játékos lépése
def jatekos_lepes(tabla, jatekos):
    while True:
        try:
            x, y = map(int, input(f"{Fore.WHITE}Hova teszed a {jatekos}-t? (pl. 2 3): {Style.RESET_ALL}").split())
            if tabla[x-1][y-1] == ".":
                tabla[x-1][y-1] = jatekos
                return x-1, y-1  # visszaadjuk a koordinátákat a győzelem ellenőrzéshez
            else:
                print(Fore.WHITE + "Ez a mező már foglalt, próbáld újra!" + Style.RESET_ALL)
        except (ValueError, IndexError):
            print(Fore.WHITE + "Érvénytelen koordináták, próbáld újra!" + Style.RESET_ALL)

# Bot lépése
def bot_lepes(tabla, bot_jel, jatekos_jel):
    meret = len(tabla)
    # Irányok, amelyekben a bot keres (nyolc irány: jobbra, balra, fel-le, átlók)
    iranyok = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]

    # 1. Kritikus blokk keresése (játékos két egymás melletti "X"-e)
    for x in range(meret):
        for y in range(meret):
            if tabla[x][y] == jatekos_jel:
                for dx, dy in iranyok:
                    try:
                        # Két egymás melletti játékos jel keresése
                        if tabla[x + dx][y + dy] == jatekos_jel:
                            # Megnézzük, hogy tudunk-e blokkolni valamelyik irányban
                            # Blokkolás egyik irányban
                            if 0 <= x - dx < meret and 0 <= y - dy < meret and tabla[x - dx][y - dy] == ".":
                                tabla[x - dx][y - dy] = bot_jel
                                return x - dx, y - dy
                            # Blokkolás másik irányban
                            if 0 <= x + 2*dx < meret and 0 <= y + 2*dy < meret and tabla[x + 2*dx][y + 2*dy] == ".":
                                tabla[x + 2*dx][y + 2*dy] = bot_jel
                                return x + 2*dx, y + 2*dy
                    except IndexError:
                        continue

    # 2. Saját nyerési lehetőség keresése (bot két egymás melletti "O"-ja)
    for x in range(meret):
        for y in range(meret):
            if tabla[x][y] == bot_jel:
                for dx, dy in iranyok:
                    try:
                        # Két egymás melletti bot jel keresése
                        if tabla[x + dx][y + dy] == bot_jel:
                            # Nyerési lehetőség kibővítése egyik irányban
                            if 0 <= x - dx < meret and 0 <= y - dy < meret and tabla[x - dx][y - dy] == ".":
                                tabla[x - dx][y - dy] = bot_jel
                                return x - dx, y - dy
                            # Nyerési lehetőség kibővítése másik irányban
                            if 0 <= x + 2*dx < meret and 0 <= y + 2*dy < meret and tabla[x + 2*dx][y + 2*dy] == ".":
                                tabla[x + 2*dx][y + 2*dy] = bot_jel
                                return x + 2*dx, y + 2*dy
                    except IndexError:
                        continue

    # 3. Ha nincs kritikus blokk és nyerési lehetőség, véletlenszerű lépés
    ures_poziciok = [(i, j) for i in range(meret) for j in range(meret) if tabla[i][j] == "."]
    if ures_poziciok:
        x, y = random.choice(ures_poziciok)
        tabla[x][y] = bot_jel
        return x, y

# Győzelem ellenőrzése (sorok, oszlopok és átlók alapján)
def ellenoriz_gyoztest(palya, gyozelmi_hossz=5):
    meret = len(palya)

    # Sorok és oszlopok ellenőrzése
    for i in range(meret):
        x_szamlalo_sor = o_szamlalo_sor = 0
        x_szamlalo_oszlop = o_szamlalo_oszlop = 0

        for j in range(meret):
            # Sorok ellenőrzése
            if palya[i][j] == "X":
                x_szamlalo_sor += 1
            else:
                x_szamlalo_sor = 0
            if palya[i][j] == "O":
                o_szamlalo_sor += 1
            else:
                o_szamlalo_sor = 0

            # Oszlopok ellenőrzése
            if palya[j][i] == "X":
                x_szamlalo_oszlop += 1
            else:
                x_szamlalo_oszlop = 0
            if palya[j][i] == "O":
                o_szamlalo_oszlop += 1
            else:
                o_szamlalo_oszlop = 0

            # Győzelem ellenőrzése
            if x_szamlalo_sor == gyozelmi_hossz or x_szamlalo_oszlop == gyozelmi_hossz:
                return (True, "X")
            if o_szamlalo_sor == gyozelmi_hossz or o_szamlalo_oszlop == gyozelmi_hossz:
                return (True, "O")

    # Átlók ellenőrzése
    for offset in range(-meret + 1, meret):
        x_szamlalo_felso_atlo = o_szamlalo_felso_atlo = 0
        x_szamlalo_also_atlo = o_szamlalo_also_atlo = 0

        for i in range(meret):
            j_felso = i + offset
            j_also = meret - 1 - i - offset
            if 0 <= j_felso < meret:
                if palya[i][j_felso] == "X":
                    x_szamlalo_felso_atlo += 1
                else:
                    x_szamlalo_felso_atlo = 0
                if palya[i][j_felso] == "O":
                    o_szamlalo_felso_atlo += 1
                else:
                    o_szamlalo_felso_atlo = 0
            if 0 <= j_also < meret:
                if palya[i][j_also] == "X":
                    x_szamlalo_also_atlo += 1
                else:
                    x_szamlalo_also_atlo = 0
                if palya[i][j_also] == "O":
                    o_szamlalo_also_atlo += 1
                else:
                    o_szamlalo_also_atlo = 0

            if x_szamlalo_felso_atlo == gyozelmi_hossz or x_szamlalo_also_atlo == gyozelmi_hossz:
                return (True, "X")
            if o_szamlalo_felso_atlo == gyozelmi_hossz or o_szamlalo_also_atlo == gyozelmi_hossz:
                return (True, "O")

    return (False, False)

# Játékos mód kiválasztása
def jatek_mod_kivalasztas():
    while True:
        valasztas = input(Fore.WHITE + "Bot ellen akarsz játszani (1) vagy két játékos módot választasz (2)? " + Style.RESET_ALL)
        if valasztas == "1":
            return "bot"
        elif valasztas == "2":
            return "multiplayer"
        else:
            print(Fore.WHITE + "Érvénytelen választás, próbáld újra!" + Style.RESET_ALL)

# --- FŐ PROGRAM ---

def jatek():
    # Játékos mód kiválasztása
    mod = jatek_mod_kivalasztas()

    # Pálya méretének bekérése
    meret = int(input(Fore.WHITE + "Mekkora legyen a pálya? " + Style.RESET_ALL))

    # Pálya legenerálása
    tabla = general_palya(meret)

    # Játék ciklus
    jatekosok = ["X", "O"]
    aktualis_jatekos_index = 0
    utolso_jatekos_lepes = None

    while True:
        # Pálya kiírása
        kiir_palya(tabla)

        # Játékos lépése
        if mod == "bot" and aktualis_jatekos_index == 1:
            utolso_jatekos_lepes = bot_lepes(tabla, jatekosok[1], jatekosok[0])
        else:
            aktualis_jatekos = jatekosok[aktualis_jatekos_index]
            utolso_jatekos_lepes = jatekos_lepes(tabla, aktualis_jatekos)  # lépés koordinátái

        # Győzelem ellenőrzése
        gyoztes = ellenoriz_gyoztest(tabla)

        if gyoztes[0]:
            kiir_palya(tabla)
            print(Fore.WHITE + f"{gyoztes[1]} nyert!" + Style.RESET_ALL)
            break

        # Játékos váltás
        aktualis_jatekos_index = 1 - aktualis_jatekos_index

# A játék elindítása
if __name__ == "__main__":
    jatek()
