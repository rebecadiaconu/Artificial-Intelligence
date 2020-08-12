import time

import pygame, sys


# functie folosita la calcularea scorului
def manhattanDistance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


# creare interfata grafica
def buildGrid(display, tabla):
    coloana = -1
    linie = -1
    widthGrid = 100
    heightGrid = 100

    hareImg = pygame.image.load('233_Diaconu_Rebeca_Lab9_Pb5_imagineIepuras.png')
    hareImg = pygame.transform.scale(hareImg, (widthGrid, heightGrid))
    houndImg = pygame.image.load('233_Diaconu_Rebeca_Lab9_Pb5_imagineCatelus.png')
    houndImg = pygame.transform.scale(houndImg, (widthGrid, heightGrid))

    drt = []

    # in cazul pozitiilor de start si finish (10 si 0), mai adaugam inca 2 patratele, unul inainte si unul dupa
    for index in range(len(tabla)):

        # in cazul in care suntem la pozitiile 0 si 10, adaugam, unul inainte si unul dupa
        # de culoare neagra pentru a marca colturile imposibil de selectat
        if index == 0:
            patr = pygame.Rect(0 * (widthGrid + 1), 0 * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (0, 0, 0), patr)

            linie = 1
            coloana = 0
            patr = pygame.Rect(coloana * (widthGrid + 1), linie * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (255, 255, 255), patr)

            patr = pygame.Rect(0 * (widthGrid + 1), 2 * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (0, 0, 0), patr)

        elif index > 0 and index < 10:
            linie = (index - 1) % 3
            coloana = (index - 1) // 3 + 1
            patr = pygame.Rect(coloana * (widthGrid + 1), linie * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (255, 255, 255), patr)

        elif index == 10:
            patr = pygame.Rect(0 * (widthGrid + 1), 0 * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (0, 0, 0), patr)

            linie = 1
            coloana = 4
            patr = pygame.Rect(coloana * (widthGrid + 1), linie * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (255, 255, 255), patr)

            patr = pygame.Rect(0 * (widthGrid + 1), 0 * (heightGrid + 1), widthGrid, heightGrid)
            drt.append(patr)
            pygame.draw.rect(display, (0, 0, 0), patr)

        # daca in tabla curenta pe pozitia index se afla unul din jucatori
        # afisam imaginea asociata acestuia
        if tabla[index] == 'D':
            display.blit(houndImg, (coloana * widthGrid, linie * heightGrid))
        elif tabla[index] == 'R':
            display.blit(hareImg, (coloana * widthGrid, linie * heightGrid))

    pygame.display.flip()
    return drt


class Joc:
    nrPozitii = 11
    simboluriJoc = ['D', 'R']  # simbolurile din joc: D - dogs, R - rabbit
    JMIN = None  # utilizatorul
    JMAX = None  # calculatorul
    GOL = '#'  # simbol folosit pentru cand pozitia este libera

    def __init__(self, tabla=None, mutareVert=0):
        # vector in care tinem minte valorile regasite in fiecare din cele 11 pozitii
        self.tablaJoc = tabla or ['D', 'D', Joc.GOL, 'D', Joc.GOL, Joc.GOL, Joc.GOL, Joc.GOL, Joc.GOL, Joc.GOL, 'R']
        # numar mutari consecutive pe verticala facute de catelusi
        self.mutariVert = mutareVert
        self.Muchii = [[1, 2, 3],
                       [0, 2, 4, 5],
                       [0, 1, 3, 5],
                       [0, 2, 5, 6],  # lista cu toate muchiile existente in tabla de joc
                       [1, 5, 7],  # capatul muchiei este dat de indicele listei de varfuri in lista  Muchii
                       [1, 2, 3, 4, 6, 7, 8, 9],
                       [3, 5, 9],
                       [4, 5, 8, 10],
                       [5, 7, 9, 10],
                       [5, 6, 8, 10],
                       [7, 8, 9]]

    def final(self):
        winHare = False
        winHounds = False

        # pozitia iepurasului
        index = self.tablaJoc.index(Joc.simboluriJoc[1])

        # verific in lista de muchii pentru pozitia respectiva daca este cel putin un loc liber pentru iepuras
        # daca da, catelusii nu au castigat
        # daca nu, final de joc -> au castigat catelusii
        found = 0
        for mutare in self.Muchii[index]:
            if self.tablaJoc[mutare] == Joc.GOL:
                found = 1

        if found == 0:
            winHounds = True

        # verific daca iepurasul se afla in stanga catelusilor sau daca catelusii au
        # mutat consecutiv de 10 ori pe verticala
        # daca da, final de joc -> a castigat iepurasul
        if index == 0:
            winHare = True
        elif self.mutariVert >= 10:
            winHare = True
        else:
            # numarul de catelusi din dreapta iepurasului
            counter = 0
            for poz in range(self.nrPozitii):
                if self.tablaJoc[poz] == Joc.simboluriJoc[0]:
                    if (index - 1) / 3 <= (poz - 1) / 3:
                        counter += 1

            if counter == 3:
                winHare = True

        if winHare:
            return Joc.simboluriJoc[1]
        elif winHounds:
            return Joc.simboluriJoc[0]
        else:
            return False

    # functie ce genereaza mutarile posibile pentru iepuras
    def mutariHare(self, jucator):
        mutari = []

        # caut in lista de muchii a pozitiei unde ma aflu si vad unde avem o pozitie goala
        # daca gasesc pozitie goala, o adaug in lista de mutari
        index = self.tablaJoc.index(jucator)
        for mutare in self.Muchii[index]:
            if self.tablaJoc[mutare] == Joc.GOL:
                mutareNoua = [jucator if i == mutare else Joc.GOL if i == index else self.tablaJoc[i] for i in
                              range(self.nrPozitii)]
                mutari.append(Joc(mutareNoua, self.mutariVert))

        return mutari

    # verific daca mutarea pe care urmeaza sa o fac este pe verticala
    def goVert(self, mutare, index):
        movedVert = False

        # sunt pe a doua linie si vreau sa ma mut pe prima
        if mutare % 3 == 1 and index % 3 == 2 and abs(index - mutare) == 1:
            movedVert = True

        # sunt pe a douaa linie si vreau sa ma mut pe a treia
        elif mutare % 3 == 0 and index % 3 == 2 and abs(index - mutare) == 1:
            movedVert = True

        # sunt pe prima linie si vreau sa ma mut pe a doua
        elif mutare % 3 == 2 and index % 3 == 1 and abs(index - mutare) == 1:
            movedVert = True

        # sunt pe a treia linie si vreau sa ma muta pe a doua
        elif mutare % 3 == 2 and index % 3 == 0 and abs(index - mutare) == 1:
            movedVert = True

        return movedVert

    # verific sa nu merg inapoi cu catelusii
    # daca pozitia unde vreau sa ma duc este mai mica decat cea unde sunt
    # si nu ma mut pe verticala -> merg inapoi
    def goBackwards(self, mutare, index):
        movedBackwards = False
        if mutare < index:
            if not self.goVert(mutare, index):
                movedBackwards = True

        return movedBackwards

    # generez mutarile posibile pentru oricare din cei trei catelusi
    def mutariHounds(self, jucator):
        mutari = []

        # caut in tabla de joc curenta pozitiile catelusilor
        for index in range(self.nrPozitii):
            if self.tablaJoc[index] == jucator:
                # caut in lista de muchii a pozitiei pe care am gasit un catelus
                for mutare in self.Muchii[index]:
                    # daca pozitia este libera si nu merg inapoi, o adaug in lista
                    if self.tablaJoc[mutare] == Joc.GOL:
                        if not self.goBackwards(mutare, index):
                            mutareNoua = [jucator if i == mutare else Joc.GOL if i == index else self.tablaJoc[i] for i
                                          in
                                          range(self.nrPozitii)]
                            # daca merg pe verticala, cresc cu 1 numarul de mutari facute pana acum pe acea axa
                            # daca nu, resetez valoarea la 0
                            if self.goVert(mutare, index):
                                mutari.append(Joc(mutareNoua, self.mutariVert + 1))
                            else:
                                mutari.append(Joc(mutareNoua, 0))

        return mutari

    # calculez scorul in functie de jucator
    # folosesc distanta manhattan intre pozitii
    # pentru acest lucru a trebuit sa-mi imaginez lista mea de cele 11 pozitii in care retin situatia curenta a jocului
    # intr-o matrice de 3x5 ( 3 linii, 5 coloane, cum e vizibil si in interfata)
    # si calculez in functie de indicele pozitiei linia si coloana pe care s-ar afla in matrice

    # -> pentru IEPURAS: dist(iepuras,finish (pozitia 0)) - dist(iepuras, start(pozitia 10))
    #                    tinand cont ca trebuie sa evitam si catelusii am adunat la scor
    #                    si distanta dintre iepuras si fiecare dintre ei, luand in calcul urmatoarele 2 situatii:
    #                   1. se afla in dreapta catelusilor: am adunat dist dintre ei - 1
    #                      pentru fiecare catelus in parte, acest lucru insemnand ca, in cazul in care jocul nu este
    #                      terminat, ca inca are catelusi in stanga lui, deci scad -1 pentru fiecare
    #                   2. se afla pe aceeasi coloana: adun distanta dintre el si catel, fiind o situatie favorabila,
    #                      la urmatorul pas lasand catelul in spate
    #      DE CE E ACEASTA ABORDARE IN FAVOAREA IEPURASULUI?
    #      --> cu cat are mai multi catelusi in stanga, scorul va scadea, cu cat sunt mai putini si distanta dintre ei
    #          e mai mare, scorul va creste, nemai scazand 1 pentru fiecare
    # -> pentru CATELUSI: suma(dist(iepuras, fiecare catelus in parte)) / 3, pentru a obtine distanta medie dintre
    #                     iepuras si acestia
    #                     tratam aceleasi situatii ca pentru iepuras:
    #                   1. se afla in stanga iepurasului: scopul catelusilor e acela de a impiedica iepurasul sa
    #                      ajunga la finish, deci intereseaza distanta acestuia pana la pozitia 0, dar cum
    #                      este importanta si distanta dintre catel si iepure, am ales urmatoarea abordare:
    #                      pentru fiecare catel adun la scor: dif(dist(iepure, finish), dist(iepure, catel)) la care
    #                      adun 1, bonus pentru ca e in stanga iepurelui
    #                   2. se afla pe aceeasi coloana: in acest caz diferenta nu mai are rost, deci doar adun la scor
    #                      dist(iepure, catel), pentru fiecare in parte
    #      DE CE E ACEASTA ABORDARE IN FAVOAREA CATELUSILOR?
    #      --> cu cat se mentin in stanga iepurasului, scorul va primii bonus pentru fiecare catel, in caz contrar,
    #      scorul lor va scadea pentru ca distanta dintre ei va fi mai mica si scorul iepurasului va creste ( nu mai
    #      scadem -1 din el)
    def getScor(self, jucator):
        # liniile si coloanele pentru start(10) si finish(0)
        colStart = 4
        linStart = 1
        colFinish = 0
        linFinish = 1

        # linia si coloana unde s-ar afla iepurasul in matricea jocului
        index = self.tablaJoc.index(Joc.simboluriJoc[1])
        colR = (index - 1) // 3
        linR = (index - 1) % 3

        # lista pentru coloanele unde s-ar afla catelusii in matrice
        colD = []
        # lista pentru liniile unde s-ar afla catelusii in matrice
        linD = []

        for poz in range(self.nrPozitii):
            if self.tablaJoc[poz] == Joc.simboluriJoc[0]:
                col = (poz - 1) // 3
                lin = (poz - 1) % 3
                colD.append(col)
                linD.append(lin)

        # calculam scorul pentru iepuras
        if jucator == Joc.simboluriJoc[1]:
            score = manhattanDistance(linR, colR, linFinish, colFinish) - manhattanDistance(linR, colR, linStart,
                                                                                            colStart)
            # iepurasul e in dreapta catelusilor
            if colR > colD[0]:
                score += manhattanDistance(linR, colR, linD[0], colD[0]) - 1
            if colR > colD[1]:
                score += manhattanDistance(linR, colR, linD[1], colD[1]) - 1
            if colR > colD[2]:
                score += manhattanDistance(linR, colR, linD[2], colD[2]) - 1

            # iepurasul si catelusii sunt pe aceeasi coloana
            if colR == colD[0]:
                score += manhattanDistance(linR, colR, linD[0], colD[0])
            if colR == colD[1]:
                score += manhattanDistance(linR, colR, linD[1], colD[1])
            if colR == colD[2]:
                score += manhattanDistance(linR, colR, linD[1], colD[1])

            return score

        # calculam scorul pentru catelusi
        else:
            score = (manhattanDistance(linR, colR, linD[2], colD[2]) + manhattanDistance(linR, colR, linD[1],
                                                                                         colD[1]) + manhattanDistance(
                linR, colR, linD[0], colD[0])) / 3

            # iepurasul e in dreapta catelusilor
            if colR > colD[0]:
                score += manhattanDistance(linR, colR, linFinish, colFinish) - manhattanDistance(linR, colR, linD[0],
                                                                                                 colD[0]) + 1
            if colR > colD[1]:
                score += manhattanDistance(linR, colR, linFinish, colFinish) - manhattanDistance(linR, colR, linD[1],
                                                                                                 colD[1]) + 1
            if colR > colD[2]:
                score += manhattanDistance(linR, colR, linFinish, colFinish) - manhattanDistance(linR, colR, linD[2],
                                                                                                 colD[2]) + 1
            # iepurasul e pe aceeasi coloana cu catelusii
            if colR == colD[0]:
                score += manhattanDistance(linR, colR, linD[0], colD[0])
            if colR == colD[1]:
                score += manhattanDistance(linR, colR, linD[1], colD[1])
            if colR == colD[2]:
                score += manhattanDistance(linR, colR, linD[2], colD[2])

            return score

    # functie de estimare a scorului pentru cei 2 algoritmi folositi
    def estimeazaScor(self, adancime):
        tFinal = self.final()
        if tFinal == Joc.JMAX:
            return 99 + adancime
        elif tFinal == Joc.JMIN:
            return -99 + adancime
        else:
            return self.getScor(Joc.JMAX) - self.getScor(Joc.JMIN)

    # functia de afisare a tablei curente de joc
    def __str__(self):
        sir = ""
        sir += "    " + self.tablaJoc[1] + " - " + self.tablaJoc[4] + " - " + self.tablaJoc[7] + "    \n"
        sir += "  / | \ | / | \  " + "\n"
        sir += self.tablaJoc[0] + " - " + self.tablaJoc[2] + " - " + self.tablaJoc[5] + " - " + self.tablaJoc[
            8] + " - " + self.tablaJoc[10] + "\n"
        sir += "  \ | / | \ | /  " + "\n"
        sir += "    " + self.tablaJoc[3] + " - " + self.tablaJoc[6] + " - " + self.tablaJoc[9] + "    \n"

        return sir


class Stare:
    adancimeMax = None

    def __init__(self, tablaJoc, jCurent, adancime, parinte=None, scor=None):
        self.tablaCurenta = tablaJoc  # de tip Joc
        self.jCurent = jCurent
        self.parinte = parinte  # de tip Joc

        # adancimea in arborele de stari
        self.adancime = adancime

        # scorul starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutariPosibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stareAleasa = None

    # returneaza jucatorul opus
    def getJucatorOpus(self):
        if self.jCurent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    # returneaza o lista dde mutari posibile pentru tabla jocului
    def mutari(self):
        if self.jCurent == Joc.simboluriJoc[0]:
            listaMutari = self.tablaCurenta.mutariHounds(self.jCurent)
        else:
            listaMutari = self.tablaCurenta.mutariHare(self.jCurent)

        jucOpus = self.getJucatorOpus()
        listaStariMutari = []
        if len(listaMutari) != 0:
            for mutare in listaMutari:
                listaStariMutari.append(Stare(mutare, jucOpus, self.adancime - 1, parinte=self))

        return listaStariMutari

    # functie de afisare tabla curenta joc + jucator
    def __str__(self):
        sir = str(self.tablaCurenta) + "(Jucator curent: " + self.jCurent + ")\n"
        return sir


# Algoritmul MINIMAX

def miniMax(stare):
    if stare.adancime == 0 or stare.tablaCurenta.final():
        stare.scor = stare.tablaCurenta.estimeazaScor(stare.adancime)

        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutariPosibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariScor = [miniMax(mutare) for mutare in stare.mutariPosibile]

    if stare.jCurent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stareAleasa = max(mutariScor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stareAleasa = min(mutariScor, key=lambda x: x.scor)

    stare.scor = stare.stareAleasa.scor

    return stare


# Algoritmul ALPHA-BETA

def alphaBeta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tablaCurenta.final():
        stare.scor = stare.tablaCurenta.estimeazaScor(stare.adancime)
        return stare

    if alpha >= beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutariPosibile = stare.mutari()

    if stare.jCurent == Joc.JMAX:
        scorCurent = float('-inf')

        for mutare in stare.mutariPosibile:
            # calculeaza scorul
            stareNoua = alphaBeta(alpha, beta, mutare)

            if scorCurent < stareNoua.scor:
                stare.stareAleasa = stareNoua
                scorCurent = stareNoua.scor

            if alpha < stareNoua.scor:
                alpha = stareNoua.scor
                if alpha >= beta:
                    break

    elif stare.jCurent == Joc.JMIN:
        scorCurent = float('inf')

        for mutare in stare.mutariPosibile:
            stareNoua = alphaBeta(alpha, beta, mutare)

            if scorCurent > stareNoua.scor:
                stare.stareAleasa = stareNoua
                scorCurent = stareNoua.scor

            if beta > stareNoua.scor:
                beta = stareNoua.scor
                if alpha >= beta:
                    break

    stare.scor = stare.stareAleasa.scor

    return stare


# afisam pozitiile disponibile in acest joc, folosita cand cerem utilizatorului sa faca o mutare noua
def afisTablaMutari():
    sir = "\n"
    sir += "    1 - 4 - 7    \n"
    sir += "  / | \ | / | \  " + "\n"
    sir += "0 - 2 - 5 - 8 - 10\n"
    sir += "  \ | / | \ | /  " + "\n"
    sir += "    3 - 6 - 9    \n"

    print(sir)


# verificam daca este final de joc,
# daca da, afisam castigatorul impreuna cu numarul total de mutari si scorul fiecarui jucator
def afisDacaFinal(stareCurenta, nrMutariJuc, nrMutariPc):
    final = stareCurenta.tablaCurenta.final()

    if final:
        if final == Joc.simboluriJoc[1]:
            print("A castigat iepurasul!")
        else:
            print("Au castigat catelusii!")

        print("Numar total de mutari facute de calculator: " + str(nrMutariPc))
        print("Numar total de mutari facute de tine: " + str(nrMutariJuc))

        print("Scor calculator: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMAX)))
        print("Scorul tau: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMIN)))

        return True

    return False


def main():
    global tipAlgoritm, optionChoosed

    # initializare tip algoritm
    raspunsValid = False
    while not raspunsValid:
        tipAlgoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
        if tipAlgoritm in ['1', '2']:
            raspunsValid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX in functie de dificultate
    raspunsValid = False
    while not raspunsValid:
        n = int(input("Nivelul de dificultate al jocului: \n1. Incepator \n2. Mediu \n3. Avansat \n"))
        if n in range(1, 4):
            if n == 1:
                Stare.adancimeMax = 3
            elif n == 2:
                Stare.adancimeMax = 6
            elif n == 3:
                Stare.adancimeMax = 9
            raspunsValid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul, cuprins intre 1 si 3.")

    # initializare jucatori
    [s1, s2] = Joc.simboluriJoc.copy()  # lista de simboluri posibile
    raspunsValid = False
    while not raspunsValid:
        Joc.JMIN = str(input("Doriti sa jucati cu {} - dogs sau cu {} - rabbit? ".format(s1, s2))).upper()
        if (Joc.JMIN in Joc.simboluriJoc):
            raspunsValid = True
        else:
            print("Raspunsul trebuie sa fie {} sau {}.".format(s1, s2))
    Joc.JMAX = s1 if Joc.JMIN == s2 else s2

    # stabilire mod de joc: 1 - din consola, 2 - interfata
    raspunsValid = False
    while not raspunsValid:
        optionChoosed = int(input("Doriti sa jucati folosind: 1 - consola + tastatura, 2 - interfata + mouse \n"))
        if optionChoosed in range(1, 3):
            raspunsValid = True
        else:
            print("Numarul introdus trebuie sa apartina multimii {1, 2}!")

    # initializare tabla
    tablaCurenta = Joc()
    print("Tabla initiala")
    print(str(tablaCurenta))

    # creare stare initiala
    stareCurenta = Stare(tablaCurenta, Joc.simboluriJoc[0], Stare.adancimeMax)

    # se joaca in consola
    if optionChoosed == 1:
        # initializam pozitia pe care v-om muta cu -1, valoare care nu exista in tabla de joc
        pozitie = -1
        nrMutariJuc = 0
        nrMutariPc = 0

        while True:
            print("\n---------------------------------\n ")

            # afisam matricea jocului cu indicii fiecarei pozitii
            # pentru ca jucatorul sa stie ce are de ales
            afisTablaMutari()

            # preluare timp de start
            tInainte = time.perf_counter()

            # muta jucatorul
            if stareCurenta.jCurent == Joc.JMIN:
                print("ESTE RANDUL UTILIZATORULUI!\n")

                # intrebam daca doreste ca jocul sa fie oprit
                # daca da, afisam scorul curent al fiecarui jucator
                option = -1
                raspunsValid = False
                while not raspunsValid:
                    option = int(input("Doriti sa parasiti jocul? 0 - Nu, 1 - Da \n"))
                    if option in range(0, 2):
                        raspunsValid = True
                    else:
                        print("Va rog alegeti 0 sau 1!")

                # daca doreste sa opreasca jocul, afisam scorurile si oprim programul
                if option == 1:
                    print("Joc incheiat la dorinta ta!")
                    print("Scor calculator: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMAX)))
                    print("Scorul tau: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMIN)))
                    break

                # se joaca cu catelusii
                if stareCurenta.jCurent == Joc.simboluriJoc[0]:
                    raspunsValid = False
                    while not raspunsValid:
                        try:
                            # intrebam ce catelus doreste sa mute
                            pozitieCatel = int(input("Pe ce pozitie se afla catelul pe care doriti sa il muti? \n"))

                            # numarul dat este intre 0 si 10?
                            if pozitieCatel in range(0, 11):
                                # pe pozitia data se afla un catel?
                                if stareCurenta.tablaCurenta.tablaJoc[pozitieCatel] != stareCurenta.jCurent:
                                    print("Pe pozitia data nu se afla un catelus.")
                                else:
                                    # pozitia pe care acesta va fi mutat
                                    pozitie = int(input("Il muti la pozitia: "))

                                    # numarul dat este intre 0 si 10?
                                    if pozitie in range(0, 11):

                                        # verificam ca pozitia aleasa sa fie libera
                                        if stareCurenta.tablaCurenta.tablaJoc[pozitie] == Joc.GOL:
                                            # verific sa nu faca o mutare inapoi
                                            # daca cele 2 conditii sunt indeplinite -> mutare valida
                                            # daca nu, afisam mesaj corespunzator
                                            if stareCurenta.tablaCurenta.goBackwards(pozitie, pozitieCatel):
                                                print("Catelusii nu au voie sa mearga inapoi!")
                                                print("Mutari disponibile catelusi: sus, joc, dreapta, diagonala "
                                                      "dreapta (sus sau jos)")
                                            else:
                                                # mutarea este valida -> eliberam vechea pozitie si
                                                # verificam sa nu faca 10 mutari pe verticala
                                                stareCurenta.tablaCurenta.tablaJoc[pozitieCatel] = Joc.GOL
                                                if stareCurenta.tablaCurenta.goVert(pozitie, pozitieCatel):
                                                    stareCurenta.tablaCurenta.mutariVert += 1
                                                else:
                                                    stareCurenta.tablaCurenta.mutariVert = 0
                                                raspunsValid = True
                                        else:
                                            print("Acea pozitie este deja ocupata!")
                                    else:
                                        print("Pozitia trebuie sa fie un numar intre 0 ai 10!")
                            else:
                                print("Catelusii se afla pe pozitii intre 0 si 10!")
                        except ValueError:
                            print("Pozitia aleasa trebuie sa fie un numar intreg.")

                # joaca cu iepurasul
                else:
                    raspunsValid = False
                    while not raspunsValid:
                        try:
                            # pozitia pe care acesta va fi mutat
                            pozitie = int(input("Doriti sa muti pe pozitia: "))

                            # numarul dat este intre 0 si 10?
                            if pozitie in range(0, 11):
                                # verificam sa nu fie identica cu pozitia curenta a iepurasului
                                if pozitie != stareCurenta.tablaCurenta.tablaJoc.index(Joc.simboluriJoc[1]):

                                    # verificam ca pozitia aleasa sa fie libera
                                    # daca cele 2 conditii sunt indeplinite -> mutare valida
                                    # daca nu, afisam mesaj corespunzator
                                    if stareCurenta.tablaCurenta.tablaJoc[pozitie] != Joc.GOL:
                                        print("Acea pozitie este deja ocupata!")
                                    else:
                                        # mutare valida -> eliberam pozitia veche
                                        stareCurenta.tablaCurenta.tablaJoc[
                                            stareCurenta.tablaCurenta.tablaJoc.index(
                                                Joc.simboluriJoc[1])] = Joc.GOL
                                        raspunsValid = True
                                else:
                                    print("Iepurasul de afla deja pe acea pozitie!")
                            else:
                                print("Pozitia trebuie sa fie un numar intre 0 ai 10!")
                        except ValueError:
                            print("Pozitia aleasa trebuie sa fie un numar intreg.")

                # mutam jucatorul pe pozitia aleasa
                stareCurenta.tablaCurenta.tablaJoc[pozitie] = Joc.JMIN

                # afisarea starii jocului in urma mutarii utilizatorului
                print("\nTabla dupa mutarea utilizatorului:")
                print(str(stareCurenta))

                # crestem numarul de mutari cu 1 si preiau timpul de final, dupa realizarea mutarii
                # afisez timpul in care s-a gandit jucatorul
                nrMutariJuc += 1
                tDupa = time.perf_counter()
                print(f"Ti-ai ales urmatoarea mutare in {tDupa - tInainte:0.8f} secunde.")

                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                if afisDacaFinal(stareCurenta, nrMutariJuc, nrMutariPc):
                    break
                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stareCurenta.jCurent = stareCurenta.getJucatorOpus()

            # muta calculatorul
            else:
                print("ESTE RANDUL CALCULATORULUI! \n")

                # preiau timpul in secunde de dinainte de mutare
                tInainte = time.perf_counter()

                if tipAlgoritm == '1':
                    stareActualizata = miniMax(stareCurenta)
                else:
                    # tip_algoritm = 2
                    stareActualizata = alphaBeta(-5000, 5000, stareCurenta)

                stareCurenta.tablaCurenta = stareActualizata.stareAleasa.tablaCurenta

                # afisez tabla de joc dupa mutarea calculatorului
                if optionChoosed == 1:
                    print("Tabla dupa mutarea calculatorului:")
                    print(str(stareCurenta))

                # preiau timpul in secunde de dupa mutare si cresc numarul de mutari realizate cu 1
                nrMutariPc += 1
                tDupa = time.perf_counter()
                print(f"Calculatorul a \"gandit\" timp de {tDupa - tInainte:0.8f} secunde.")

                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                if afisDacaFinal(stareCurenta, nrMutariJuc, nrMutariPc):
                    break

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stareCurenta.jCurent = stareCurenta.getJucatorOpus()

    # se joaca cu interfata
    elif optionChoosed == 2:
        pozitie = -1
        nrMutariJuc = 0
        nrMutariPc = 0

        # setari interfata grafica: initializare
        pygame.init()
        pygame.display.set_caption('hare and hounds')
        ecran = pygame.display.set_mode(size=(500, 300))

        cells = buildGrid(ecran, tablaCurenta.tablaJoc)

        # observand ca pygame-ul ruleaza codul de foarte multe ori pe secunda, a trebuit sa
        # renunt la while-uri si sa iau niste variabile pentru fiecare situatie cruciala jocului:
        #    1. afisare al cui este randul
        #    2. gasire catel (in cazul in care se joaca cu catelusii) si mutare jucator
        #    3. mutare finalizata, afisare timp si semn ca urmatorul jucator poate face mutarea
        findDog = False  # False -> pozCatel nu a fost selectata, True -> pozitie selectata si valida
        moved = False  # False -> jucatorul nu a mutat, True -> mutare realizata si valida
        showMessage = False  # False -> randul jucatorului nu a venit, True -> randul este in derulare

        # pozitia pe care doresc sa mut
        pozitie = -1
        # pozitie initiala catel
        pozitieCatel = -1

        while True:

            # muta utilizatorul
            if stareCurenta.jCurent == Joc.JMIN:

                # variabila este False, randul jucatorului nu a inceput, deci afisez mesaj de inceput
                if showMessage == False:
                    print("\n---------------------------------\n ")
                    print("ESTE RANDUL TAU!\n")
                    print("Patratelele negre sunt imposibil de accesat!")

                # preiau timpul in secunde de dinainte de mutare
                tInainte = time.perf_counter()

                # se joaca cu iepurasul, randul a inceput, setez varibila de afisare la True si cer pozitia
                if stareCurenta.jCurent == Joc.simboluriJoc[1] and showMessage == False:
                    showMessage = True
                    print("Unde doresti sa muti iepurasul?")

                # se joaca cu catelusii, randul a inceput, setez varibila de afisare la True si cer pozitia
                elif stareCurenta.jCurent == Joc.simboluriJoc[0] and showMessage == False:
                    showMessage = True
                    print("Selectati catelusul pe care doriti sa-l mutati!")

                # luam fiecare eveniment posibil in pygame si intreb doar de cele ce pot aparea aici
                for event in pygame.event.get():
                    # dorim sa inchidem jocul (butonul de X, situat dreapta sus)
                    if event.type == pygame.QUIT:
                        print("Joc incheiat la dorinta ta!")
                        print("Scor calculator: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMAX)))
                        print("Scorul tau: " + str(stareCurenta.tablaCurenta.getScor(Joc.JMIN)))
                        pygame.quit()
                        sys.exit()

                    # CAZ 1 -> joc cu iepurasul
                    # click mouse, moved = False -> jucam cu iepurasul, nu a fost mutat inca
                    if event.type == pygame.MOUSEBUTTONDOWN and Joc.JMIN == Joc.simboluriJoc[1] and moved == False:
                        pozitie = -1
                        pos = pygame.mouse.get_pos()  # pozitia pe care s-a dat click in matricea interfetei

                        # caut patratelul in care s-a dat click-ul in lista de celule apartinand interfetei
                        for index in range(15):
                            if cells[index].collidepoint(pos):
                                # calculez linia si coloana din matricea interfetei
                                # in functie de pozitia din vectorul de celule (patratele)
                                linie = index % 3
                                coloana = index // 3

                                # verific sa nu fie unul din colturile acesteia
                                if linie != 1 and (coloana == 0 or coloana == 4):
                                    print("Spatiu imposibil de selectat!")
                                else:
                                    # daca ne aflam pe plansa, calculez indicele din vectorul de pozitii,
                                    # scazand cele 2 patratele negre, adaugate pentru a marca colturile plansei
                                    if coloana == 0:
                                        pozitie = 0
                                    elif coloana == 4:
                                        pozitie = 10
                                    else:
                                        pozitie = index - 2
                                # verific ca ne aflam pe una din pozitiile adiacente celei a iepurasului si
                                # daca pozitia este libera
                                if pozitie in stareCurenta.tablaCurenta.Muchii[
                                    stareCurenta.tablaCurenta.tablaJoc.index(Joc.simboluriJoc[1])] and \
                                        stareCurenta.tablaCurenta.tablaJoc[pozitie] == Joc.GOL:
                                    # mutare valida -> setez variabila la True -> rand incheiat
                                    moved = True
                                    break
                                else:
                                    print('Iepurasul nu poate ajunge in aceasta pozitie.')

                    # CAZ 2.1 -> click mouse, findDog = False, moved = False -> rand neincheiat,
                    # catelus de mutat neselectat
                    elif event.type == pygame.MOUSEBUTTONDOWN and Joc.JMIN == Joc.simboluriJoc[
                        0] and findDog == False and moved == False:
                        pos = pygame.mouse.get_pos()  # pozitia catel selectat

                        # caut patratelul in care s-a dat click-ul in lista de celule apartinand interfetei
                        for index in range(15):
                            if cells[index].collidepoint(pos):
                                # calculez linia si coloana din matricea interfetei
                                # in functie de pozitia din vectorul de celule (patratele)
                                linie = index % 3
                                coloana = index // 3

                                # verific sa nu fie unul din colturile acesteia
                                if linie != 1 and (coloana == 0 or coloana == 4):
                                    print("Spatiu imposibil de selectat!")
                                else:
                                    # daca ne aflam pe plansa, calculez indicele din vectorul de pozitii,
                                    # scazand cele 2 patratele negre, adaugate pentru a marca colturile plansei
                                    if coloana == 0:
                                        pozitieCatel = 0
                                    elif coloana == 4:
                                        pozitieCatel = 10
                                    else:
                                        pozitieCatel = index - 2

                                if stareCurenta.tablaCurenta.tablaJoc[pozitieCatel] == Joc.simboluriJoc[0]:

                                    # mutare valida -> setez variabila la True -> catelus selectat
                                    findDog = True
                                    print("Catelus selectat!")
                                    print("Unde doriti sa il mutati?")
                                    break
                                else:
                                    print("In pozitia selectata nu se afla un catelus!")

                    # CAZ 2.2 -> click mouse, findDog = True, moved = False -> rand neincheiat,
                    # catel selectat, mutare nerealizata
                    elif event.type == pygame.MOUSEBUTTONDOWN and Joc.JMIN == Joc.simboluriJoc[
                        0] and findDog == True and moved == False:
                        # initializare pozitie cu o valoare inexistenta in tabla de joc
                        pozitie = -1
                        pos = pygame.mouse.get_pos()  # pozitia pe care s-a dat click in matricea interfetei

                        # caut patratelul in care s-a dat click-ul in lista de celule apartinand interfetei
                        for index in range(15):
                            if cells[index].collidepoint(pos):
                                # calculez linia si coloana din matricea interfetei
                                # in functie de pozitia din vectorul de celule (patratele)
                                linie = index % 3
                                coloana = index // 3

                                # verific sa nu fie unul din colturile acesteia
                                if linie != 1 and (coloana == 0 or coloana == 4):
                                    print("Spatiu imposibil de selectat!")
                                else:
                                    # daca ne aflam pe plansa, calculez indicele din vectorul de pozitii,
                                    # scazand cele 2 patratele negre, adaugate pentru a marca colturile plansei
                                    if coloana == 0:
                                        pozitie = 0
                                    elif coloana == 4:
                                        pozitie = 10
                                    else:
                                        pozitie = index - 2

                                # pozitia selectata se afla in muchiile adiacente si este goala
                                if pozitie in stareCurenta.tablaCurenta.Muchii[pozitieCatel] and \
                                        stareCurenta.tablaCurenta.tablaJoc[pozitie] == Joc.GOL:
                                    # verific sa nu faca o mutare inapoi
                                    if stareCurenta.tablaCurenta.goBackwards(pozitie, pozitieCatel):
                                        print("Catelusii nu au voie sa mearga inapoi!")
                                        print("Mutari disponibile catelusi: sus, joc, dreapta, "
                                              "diagonala dreapta (sus sau jos)")
                                    else:
                                        # mutare valida -> setez variabila la True -> catelus mutat
                                        # verific cazul in care mutarea este executata pe verticala
                                        if stareCurenta.tablaCurenta.goVert(pozitie, pozitieCatel):
                                            stareCurenta.tablaCurenta.mutariVert += 1
                                        else:
                                            stareCurenta.tablaCurenta.mutariVert = 0
                                        moved = True
                                        break
                                else:
                                    print("Pozitie indisponibila!")

                    # mutarea a avut loc, rand incheiat
                    if moved == True:
                        # cresc numarul de mutari cu 1
                        nrMutariJuc += 1

                        # daca joc cu catelusii, eliberez pozitia precedenta si mut pe cea selectata
                        if Joc.JMIN == Joc.simboluriJoc[0]:
                            stareCurenta.tablaCurenta.tablaJoc[pozitieCatel] = Joc.GOL
                            stareCurenta.tablaCurenta.tablaJoc[pozitie] = Joc.JMIN
                        else:
                            # daca joc cu iepuarsul, eliberez pozitia precedenta si mut pe cea selectata
                            stareCurenta.tablaCurenta.tablaJoc[
                                stareCurenta.tablaCurenta.tablaJoc.index(Joc.simboluriJoc[1])] = Joc.GOL
                            stareCurenta.tablaCurenta.tablaJoc[pozitie] = Joc.JMIN

                        # actualizez interfata
                        cells = buildGrid(ecran, stareCurenta.tablaCurenta.tablaJoc)

                        # preiau timpul final, dupa incheierea mutarii
                        tDupa = time.perf_counter()
                        print(f"Ti-ai ales urmatoarea mutare in {tDupa - tInainte:0.8f} secunde.")

                        # testez daca jocul a ajuns intr-o stare finala
                        # si afisez un mesaj corespunzator in caz ca da
                        if afisDacaFinal(stareCurenta, nrMutariJuc, nrMutariPc):
                            pygame.quit()
                            sys.exit()

                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                        stareCurenta.jCurent = stareCurenta.getJucatorOpus()



            # muta calculatorul
            else:
                print("ESTE RANDUL CALCULATORULUI! \n")

                # preiau timpul in msecunde de dinainte de mutare
                tInainte = time.perf_counter()

                if tipAlgoritm == '1':
                    stareActualizata = miniMax(stareCurenta)
                else:
                    # tip_algoritm = 2
                    stareActualizata = alphaBeta(-5000, 5000, stareCurenta)

                stareCurenta.tablaCurenta = stareActualizata.stareAleasa.tablaCurenta

                # actualizez interfata
                cells = buildGrid(ecran, stareCurenta.tablaCurenta.tablaJoc)

                # preiau timpul in secunde de dupa mutare si cresc numarul de mutari cu 1
                nrMutariPc += 1
                tDupa = time.perf_counter()
                print(f"Calculatorul a \"gandit\" timp de {tDupa - tInainte:0.8f} secunde.")

                # testez daca jocul a ajuns intr-o stare finala
                # si afisez un mesaj corespunzator in caz ca da
                if afisDacaFinal(stareCurenta, nrMutariJuc, nrMutariPc):
                    pygame.quit()
                    sys.exit()

                # S-a realizat o mutare. Schimb jucatorul cu cel opus
                stareCurenta.jCurent = stareCurenta.getJucatorOpus()

                # resetez variabilele pentru un nou rand al utilizatorului
                findDog, moved, showMessage = False, False, False


if __name__ == "__main__":
    # timp start joc
    tStart = time.perf_counter()
    main()
    # timp final joc
    tFinal = time.perf_counter()
    print(f"Jocul a durat timp de {tFinal - tStart:0.2f} secunde.")
