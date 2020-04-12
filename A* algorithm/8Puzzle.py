"""  DIACONU REBECA-MIHAELA, Grupa 233 """

f = open('puzzle.txt', 'r')
lMatrice = int(next(f))
matInit = []
for i in range(lMatrice):
    aux = [x for x in next(f).split()]
    matInit.append(aux)

final = []
for i in range(lMatrice):
    aux = [x for x in next(f).split()]
    final.append(aux)

f.close()


class Nod:
    def __init__(self, info, lMatrice):
        self.lMatrice = lMatrice
        self.info = info
        self.h = self.getH()

    def getH(self):
        h = 0
        mat_curent = self.info
        for i in range(self.lMatrice):
            for j in range(self.lMatrice):
                for k in range(self.lMatrice):
                    poz = (final[k].index(mat_curent[i][j]) if mat_curent[i][j] in final[k] else -1)
                    if poz > -1:
                        h += abs(i - k) + abs(j - poz)
                        break

        return h



    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Problema:
    def __init__(self):
        self.nod_start = Nod(matInit, lMatrice) # de tip Nod
        self.nod_scop = Nod(final, lMatrice)  # doar info (fara h)

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
        trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
        fie None, daca nu exista niciun nod cu acea informatie."""

        for nod in self.noduri:
            if nod.info == info:
                return nod

""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf

    """

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
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

    def contine_in_drum(self, nod):
        """
            Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
            Verificarea se face mergand din parinte in parinte pana la radacina
            Se compara doar informatiile nodurilor (proprietatea info)
            Returnati True sau False.

            "nod" este obiect de tip Nod (are atributul "nod.info")
            "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """
        nod_curent = self

        while nod_curent:
            if nod_curent.nod_graf.info == nod.info:
                return True
            else:
                nod_curent = nod_curent.parinte

        return False

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """
        index = -2
        index2 = -2
        succesori = []
        x = '0'
        mat = self.nod_graf.info

        for i in range(len(mat)):
            poz = (mat[i].index(x) if x in mat[i] else -1)
            if poz != -1:
                index = i
                index2 = poz
                break

        if index - 1 >= 0:
            mat_nou = [[mat[index - 1][index2] if i == index and j == index2 else x if i == index - 1 and j == index2 else mat[i][j] for j in range(len(mat))] for i in range(len(mat))]
            succesori.append((Nod(mat_nou, self.nod_graf.lMatrice), 1))

        if index + 1 <= len(mat) - 1:
            mat_nou = [[mat[index + 1][index2] if i == index and j == index2 else x if i == index + 1 and j == index2 else mat[i][j] for j in range(len(mat))] for i in range(len(mat))]
            succesori.append((Nod(mat_nou, self.nod_graf.lMatrice), 1))

        if index2 - 1 >= 0:
            mat_nou = [[mat[index][index2 - 1] if i == index and j == index2 else x if i == index and j == index2 - 1 else mat[i][j] for j in range(len(mat))] for i in range(len(mat))]
            succesori.append((Nod(mat_nou, self.nod_graf.lMatrice), 1))

        if index2 + 1 <= len(mat) - 1:
            mat_nou = [[mat[index][index2 + 1] if i == index and j == index2 else x if i == index and j == index2 + 1 else mat[i][j] for j in range(len(mat))] for i in range(len(mat))]
            succesori.append((Nod(mat_nou, self.nod_graf.lMatrice), 1))

        return succesori

    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop.info

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for x in l:
        sir += "\n" + " g = " + str(x.g) + "."
        for i in range(len(x.nod_graf.info)):
            sir += "\n" + str(x.nod_graf.info[i])
        sir += "\n" + " h = " + str(x.nod_graf.h) + "\n"

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

            if nod_curent.contine_in_drum(nod):
                pass
            else:
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
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()