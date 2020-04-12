"""  DIACONU REBECA-MIHAELA, Grupa 233 """

f = open('canibali.txt', 'r')
nrC, nrM, locuriBarca = [int(x) for x in next(f).split()]
L1 = [int(x) for x in next(f).split()]
L2 = [int(x) for x in next(f).split()]
f.close()

L1.append('vest')
L2.append('est')
init = tuple(L1)
final = tuple(L2)

class Nod:
    def __init__(self, info, nrC, nrM, locuriBarca):
        self.nrC = nrC
        self.nrM = nrM
        self.locuriBarca = locuriBarca
        self.info = info
        self.h = self.getH()

    def getH(self):
        return (self.info[0] + self.info[1]) // (self.locuriBarca - 1)

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"

class Problema:
    def __init__(self):
        self.nod_start = Nod(init, nrC, nrM, locuriBarca)  # de tip Nod
        self.nod_scop = Nod(final, nrC, nrM, locuriBarca)  # doar info (fara h)

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
        succesori = []
        nod_curent = self.nod_graf.info
        locBarca = nod_curent[4]

        if locBarca == 'vest':
            for i in range(min(self.nod_graf.locuriBarca, self.nod_graf.nrM), 0, -1):
                for j in range(min(self.nod_graf.locuriBarca, self.nod_graf.nrC), 0, -1):
                    misBarca = i
                    canBarca = j
                    if misBarca + canBarca >= 1 and misBarca + canBarca <= self.nod_graf.locuriBarca:
                        misV = nod_curent[0] - misBarca
                        canV = nod_curent[1] - canBarca
                        misE = nod_curent[2] + misBarca
                        canE = nod_curent[3] + canBarca
                        if (misBarca == 0 or misBarca >= canBarca) and (misV == 0 or misV >= canV) and (misE == 0 or misE >= canE):
                            succ = (misV, canV, misE, canE, 'est')
                            succesori.append((Nod(succ, self.nod_graf.nrC, self.nod_graf.nrM, self.nod_graf.locuriBarca), 1))

        if locBarca == 'est':
            for i in range(0, min(self.nod_graf.locuriBarca, self.nod_graf.nrM)):
                for j in range(0, min(self.nod_graf.locuriBarca, self.nod_graf.nrC)):
                    misBarca = i
                    canBarca = j
                    if misBarca + canBarca >= 1 and misBarca + canBarca <= self.nod_graf.locuriBarca:
                        misV = nod_curent[0] + misBarca
                        canV = nod_curent[1] + canBarca
                        misE = nod_curent[2] - misBarca
                        canE = nod_curent[3] - canBarca
                        if (misBarca == 0 or misBarca >= canBarca) and (misV == 0 or misV >= canV) and (
                                misE == 0 or misE >= canE):
                            succ = (misV, canV, misE, canE, 'vest')
                            succesori.append((Nod(succ, self.nod_graf.nrC, self.nod_graf.nrM, self.nod_graf.locuriBarca), 1))

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
        sir += '\n' + str(x.nod_graf.info)
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
