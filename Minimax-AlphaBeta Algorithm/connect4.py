import time


def elem_identice(lista):
    mt = set(lista)
    if len(mt) == 1:
        castigator = list(mt)[0]
        if castigator != Joc.GOL:
            print(len(lista))
            return castigator
        else:
            return False
    else:
        return False


class Joc:
    NR_COLOANE = 7
    NR_LINII = 6
    NR_CONNECT = 4  # cu cate simboluri adiacente se castiga
    SIMBOLURI_JUC = ['X', '0']  # ['G', 'R'] sau ['X', '0']
    JMIN = None  # 'R'
    JMAX = None  # 'G'
    GOL = '.'

    def __init__(self, tabla=None):
        self.matr = tabla or [Joc.GOL] * (Joc.NR_COLOANE * Joc.NR_LINII)

    def final(self):

        rez = False
        # verificam linii
        for lin in range(Joc.NR_LINII):
            for connect in range(4):
                rez = elem_identice(
                    self.matr[(lin * Joc.NR_COLOANE) + connect: (lin * Joc.NR_COLOANE) + connect + 4])
                if rez is not False:
                    return rez

        # verificam coloane
        for col in range(Joc.NR_COLOANE):
            for connect in range(3):
                rez = elem_identice(
                    self.matr[col + connect * Joc.NR_COLOANE: col + (connect + 4) * Joc.NR_COLOANE: Joc.NR_COLOANE])
                if rez is not False:
                    return rez

        # verificam diagonale \
        for lin in range(Joc.NR_LINII - 3):
            for col in range(Joc.NR_COLOANE - 3):
                rez = elem_identice(
                    self.matr[lin * Joc.NR_COLOANE + col: (lin + 3) * Joc.NR_COLOANE + col + 4: Joc.NR_COLOANE + 1])
                if rez is not False:
                    return rez

        # verificam diagonale /
        for lin in range(Joc.NR_LINII - 3):
            for col in range(Joc.NR_COLOANE, Joc.NR_COLOANE - 4, -1):
                rez = elem_identice(
                    self.matr[lin * Joc.NR_COLOANE + col: (lin + 3) * Joc.NR_COLOANE + col - 2: Joc.NR_COLOANE - 1])
                if rez is not False:
                    return rez

        if rez is False and Joc.GOL not in self.matr:
            return 'remiza'
        else:
            return False

    def mutari(self, jucator_opus):
        l_mutari = []

        mat_curent = self.matr
        for col in range(Joc.NR_COLOANE):
            index = (Joc.NR_LINII - 1) * Joc.NR_COLOANE + col
            while mat_curent[index] != Joc.GOL and index > col:
                index -= Joc.NR_COLOANE

            if index > 0 and mat_curent[index] == Joc.GOL:
                aux = [jucator_opus if i == index else mat_curent[i] for i in range(len(mat_curent))]
                l_mutari.append(Joc(aux))

        return l_mutari

    def nr_intervale_deschise(self, jucator):
        # un interval de 4 pozitii adiacente (pe linie, coloana, diag \ sau diag /)
        # este deschis pt "jucator" daca nu contine "juc_opus"

        juc_opus = Joc.JMIN if jucator == Joc.JMAX else Joc.JMAX
        rez = 0

        # linii
        for lin in range(Joc.NR_LINII):
            for connect in range(4):
                if juc_opus not in self.matr[(lin * Joc.NR_COLOANE) + connect: (lin * Joc.NR_COLOANE) + connect + 4]:
                    rez += 1

        # coloane
        for col in range(Joc.NR_COLOANE):
            for connect in range(3):
                if juc_opus not in self.matr[col + connect * Joc.NR_COLOANE: col + (
                        connect + 4) * Joc.NR_COLOANE: Joc.NR_COLOANE]:
                    rez += 1

        # diagonale \
        for lin in range(Joc.NR_LINII - 3):
            for col in range(Joc.NR_COLOANE - 3):
                if juc_opus not in self.matr[lin * Joc.NR_COLOANE + col: (
                                                                                 lin + 3) * Joc.NR_COLOANE + col + 4: Joc.NR_COLOANE + 1]:
                    rez += 1

        # diagonale /
        for lin in range(Joc.NR_LINII - 3):
            for col in range(Joc.NR_COLOANE, Joc.NR_COLOANE - 4, -1):
                if juc_opus not in self.matr[lin * Joc.NR_COLOANE + col: (
                                                                                 lin + 3) * Joc.NR_COLOANE + col - 2: Joc.NR_COLOANE - 1]:
                    rez += 1

        return rez

    def fct_euristica(self):
        return self.nr_intervale_deschise(Joc.JMAX) - self.nr_intervale_deschise(Joc.JMIN)

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX:
            return (999 + adancime)
        elif t_final == Joc.JMIN:
            return (-999 - adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def __str__(self):
        sir = ''
        for nr_col in range(self.NR_COLOANE):
            sir += str(nr_col) + ' '
        sir += '\n'

        for lin in range(self.NR_LINII):
            k = lin * self.NR_COLOANE
            sir += (" ".join([str(x) for x in self.matr[k: k + self.NR_COLOANE]]) + "\n")
        return sir


class Stare:
    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = self.jucator_opus()
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent: " + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza scorul
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent < stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor
            if (alpha < stare_noua.scor):
                alpha = stare_noua.scor
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')

        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (scor_curent > stare_noua.scor):
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if (beta > stare_noua.scor):
                beta = stare_noua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta, lin, col):
    difLinUp, difColLeft = min(lin, 3), min(col, 3)
    difLinDown, difcolRight = min(Joc.NR_LINII - lin - 1, 3), min(Joc.NR_COLOANE - col - 1, 3)
    diagL1 = min(3, min(difLinUp, difColLeft))
    diagR1 = min(3, min(difLinDown, difcolRight))
    diagR2 = min(3, min(difcolRight, difLinUp))
    diagL2 = min(3, min(difColLeft, difLinDown))

    final = False

    # verif coloana
    for i in range(lin - difLinUp, lin + difLinDown - 3 + 1):
        if final is False:
            final = elem_identice(
                stare_curenta.tabla_joc.matr[i * Joc.NR_COLOANE + col: (i + 4) * Joc.NR_COLOANE + col: Joc.NR_COLOANE])

    # verif linia
    for j in range(col - difColLeft, col + difcolRight - 3 + 1):
        if final is False:
            final = elem_identice(stare_curenta.tabla_joc.matr[lin * Joc.NR_COLOANE + j: lin * Joc.NR_COLOANE + j + 4])

    # verif diag \
    for diag in range(col - diagL1, col + diagR1 - 3):
        if final is False:
            final = elem_identice(stare_curenta.tabla_joc.matr[diag * Joc.NR_COLOANE + col - diagL1: (
                                                                                                                 diag + 4) * Joc.NR_COLOANE + col - diagL1: Joc.NR_COLOANE + 1])

    # verif diag /
    for diag in range(col + diagR2, col - diagL2 + 2, -1):
        if final is False:
            final = elem_identice(stare_curenta.tabla_joc.matr[(lin - diag + 1) * Joc.NR_COLOANE + diag: (
                                                                                                                     lin - diag + 5) * Joc.NR_COLOANE + diag - 2: Joc.NR_COLOANE - 1])

    if final:
        if final == "remiza":
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui (de sugerat o valoare < 5): ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    [s1, s2] = Joc.SIMBOLURI_JUC.copy()  # lista de simboluri posibile
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} sau cu {}? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.SIMBOLURI_JUC):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, Joc.SIMBOLURI_JUC[0], Stare.ADANCIME_MAX)

    linie = -1
    coloana = -1
    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    coloana = int(input("coloana = "))
                    if (coloana in range(0, 7)):
                        linie = -1
                        while linie + 1 < Joc.NR_LINII and stare_curenta.tabla_joc.matr[
                            (linie + 1) * Joc.NR_COLOANE + coloana] == Joc.GOL:
                            linie += 1
                        if linie == -1:
                            print("Toata coloana este ocupata.")
                        else:
                            raspuns_valid = True
                    else:
                        print("Coloana invalida (trebuie sa fie un numar intre 0 si {}).".format(Joc.NR_COLOANE - 1))

                except ValueError:
                    print("Coloana trebuie sa fie un numar intreg.")

            # dupa iesirea din while sigur am valida coloana
            # deci pot plasa simbolul pe "tabla de joc"
            pozitie = linie * Joc.NR_COLOANE + coloana
            stare_curenta.tabla_joc.matr[pozitie] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta, linie, coloana)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-5000, 5000, stare_curenta)
            linie1 = -1
            coloana1 = -1
            for i in range(len(stare_curenta.tabla_joc.matr)):
                if stare_curenta.tabla_joc.matr[i] != stare_actualizata.stare_aleasa.tabla_joc.matr[i]:
                    linie1 = i // Joc.NR_COLOANE
                    coloana1 = i % Joc.NR_COLOANE

            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if afis_daca_final(stare_curenta, linie1, coloana1):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()
