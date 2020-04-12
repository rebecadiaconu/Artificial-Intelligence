# A* informed search algorithm

# cuburiAstar.py & blocuri.txt
      Se considera M cuburi. Fiecare cub are un identificator, de exemplu o litera.
      Cuburile sunt asezate in N stive. Putem avea si stive vide (fara cuburi).
      Se da o configuratie initiala a cuburilor asezate in stive si de asemenea o configuratie
    finala.
      Se cere secventa de mutari necesara (configuratiile intermediare) pentru a ajunge de la
    starea initiala la starea finala. In cadrul unei mutari, nu putem lua decat un cub aflat 
    in varful unei stive si il putem pune doar in varful unei alte stive.

# 8puzzle.py & puzzle.txt
      Se da o cutie patratica 3*3 in care se gasesc 8 tablite distincte cu numere de la 1 la 8.
      Se dau o configuratie initiala si o configuratie finala.
      Tablitele se pot muta in cutie doar prin glisarea in spatiul liber. O mutare consta, deci,
    dintr-o singura glisare. Se cere sa se afiseze mutarile necesare pentru a ajunge de la configuratia 
    initiala la cea finala folosind Algoritmul A*.
    
# canibali.py & canibali.txt
      Se considera ca avem un numar (notat cu N) egal de canibali si misionari pe malul unui rau. Ei vor sa
    treaca raul cu ajutorul unei barci cu M locuri.
      Daca pe unul din maluri sau in barca numarul de canibali e mai mare (strict) decat numarul de misionari, 
    atunci canibalii o sa ii manance pe misionari.
      Barca nu se poate deplasa goala de la un mal la altul.
      Care este secventa de actiuni care trebuie realizata astfel incat misionarii sa nu ajunga 
    pranz pentru canibali?
    
# evadarealuiMormocel.py & mormocel.txt
      O broscuta mica de tot statea pe o frunza la fel de mica, ce plutea alene pe suprafata unui lac. Broscuta,
    spre deosebire de alte surate de-ale sale nu stia sa inoate si nu-i placea apa si poate de aceea isi dorea
    tare mult sa scape din lac si sa ajunga la mal. Singurul mod in care putea sa realizeze acest lucru era
    sa sara din frunza in frunza.
      Forma lacului poate fi aproximata la un cerc. Coordonatele frunzelor sunt raportate la centrul acestui
    cerc (deci originea axelor de coordonate, adica punctul (0,0) se afla in centrul cercului). Lungimea unei
    sarituri e maxim valoarea greutatii/3. Din cauza efortului depus, broscuta pierde o unitate de
    energie(greutate) la fiecare saritura. Se considera ca pierderea in greutate se face in timpul saltului,
    deci cand ajunge la destinatie are deja cu o unitate mai putin. Daca broscuta ajunge la greutatea 0,
    atunci moare.
      Pe unele frunze exista insecte, pe altele nu. Cand broscuta ajunge pe o frunza mananca o parte din
    insectele gasite si acest lucru ii da energie pentru noi sarituri. In fisierul de intrare se va specifica
    numarul de insecte gasite pe fiecare frunza. Daca broscuta mananca o insecta, ea creste in greutate
    cu o unitate. Atentie, odata ce a mancat o parte din insectele de pe o frunza, aceasta ramane bineinteles
    fara acel numar de insecte. O tranzitie e considerata a fi un salt plus consumarea insectelor de pe
    frunza pe care a ajuns.
    
# sudoku.py
    Implementarea jocului de sudoku.
    
# !!! Datele de intrare pentru toate problemele sunt citite din fisier, cu exceptia jocului de sudoku, unde au fost introduse de mana in interiorul clasei.
