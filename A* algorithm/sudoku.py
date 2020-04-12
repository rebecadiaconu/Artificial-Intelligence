
class Nod:
    def __init__(self, info, lMat, lCadran):
        self.lMat = lMat
        self.lCadran = lCadran
        self.info = info
        self.h = self.getH()

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"

    def getH(self):
        mat = self.info
        h = 0
        for i in range(self.lMat):
            for j in range(self.lMat):
                if mat[i][j] == 0:
                    h += 1
        return h


class Problema:
    def __init__(self):
        self.noduri = [
            Nod([[9, 7, 3, 0, 4, 2, 1, 8, 5],
                 [1, 2, 6, 5, 8, 3, 7, 9, 4],
                 [5, 8, 4, 7, 9, 1, 3, 6, 2],
                 [0, 9, 1, 4, 3, 8, 2, 5, 6],
                 [4, 6, 8, 1, 2, 5, 9, 7, 3],
                 [2, 3, 0, 9, 7, 6, 8, 4, 1],
                 [6, 1, 7, 2, 5, 9, 4, 3, 8],
                 [3, 4, 2, 8, 6, 7, 5, 1, 9],
                 [8, 5, 9, 3, 1, 4, 6, 2, 7]], 9, 3)
        ]

        self.nod_start = self.noduri[0]  # de tip Nod

""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf

    """

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g = 1, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip Nod
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
            Functie care calculeaza drumul asociat unui nod din arborele de cautare.
            Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum


    def testLinie(self, mat, linie, cif):
        for i in range(len(mat)):
            if mat[linie][i] == cif:
                return False

        return True

    def testCol(self, mat, coloana, cif):
        for i in range(len(mat)):
            if mat[i][coloana] == cif:
                return False

        return True

    def testCadran(self, mat, linie, col, cif):
        if linie % self.nod_graf.lCadran != 0 and col % self.nod_graf.lCadran  != 0:
            linie = linie - linie % self.nod_graf.lCadran
            col = col - col % self.nod_graf.lCadran

        for i in range(linie, linie + self.nod_graf.lCadran ):
            for j in range(col, col + self.nod_graf.lCadran ):
                if mat[i][j] == cif:
                    return False

        return True

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """
        succesori = []
        mat_curent = self.nod_graf.info
        for i in range(len(mat_curent)):
            for j in range(len(mat_curent)):
                if mat_curent[i][j] == 0:
                    for k in range(1, 10):
                        if self.testLinie(mat_curent, i, k) and self.testCol(mat_curent, j, k) and self.testCadran(mat_curent, i, j, k):
                            aux = [[int(k) if lin == i and col == j else int(mat_curent[lin][col]) for col in range(len(mat_curent))] for lin in range(len(mat_curent))]
                            succesori.append((Nod(aux, self.nod_graf.lMat, self.nod_graf.lCadran), 1))

        return succesori

    # se modifica in functie de problema
    def test_scop(self):
        mat = self.nod_graf.info
        for i in range(len(mat)):
            for j in range(len(mat)):
                if mat[i][j] == 0:
                    return False

        return True

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    cnt = 0
    for x in l:
        cnt += 1
        sir += "\n" + str(cnt) + "."
        for i in range(len(x.nod_graf.info)):
            sir += "\n" + str(x.nod_graf.info[i])
        sir += "\n"

    return sir


def afis_succesori_cost(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)

    return sir


def in_lista(l, nod):
    """
    lista "l" contine obiecte de tip NodParcurgere
    "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while open:
        nod_curent = open.pop(0)
        closed.append(nod_curent)

        if nod_curent.test_scop():
            break

        succesori = nod_curent.expandeaza()

        for succ in succesori:
            nod_nou = None
            nod = succ[0]
            cost = succ[1]

            nod_open = in_lista(open, nod)
            nod_closed = in_lista(closed, nod)

            g_nou = nod_curent.g + cost
            f_nou = g_nou + nod.h

            if nod_open:
                if f_nou < nod_open.f:
                    nod_open.f = f_nou
                    nod_open.g = g_nou
                    nod_open.parinte = nod_curent

            elif nod_closed:
                if f_nou < nod_closed.f:
                    nod_closed.g = g_nou
                    nod_closed.f = f_nou
                    nod_closed.parinte = nod_curent
                    open.append(nod_closed)

            else:
                nod_nou = NodParcurgere(nod_graf = nod, parinte = nod_curent, g = g_nou)
                open.append(nod_nou)

        open.sort(key = lambda nod: (nod.f, -nod.g))

    print("\n------------------ Concluzie -----------------------")
    if (len(open) == 0):
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        #print(*nod_curent.nod_graf.info, sep = '\n')
        print("Drum de cost minim: \n" + str_info_noduri(nod_curent.drum_arbore()))



if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()