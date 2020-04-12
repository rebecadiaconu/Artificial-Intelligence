# Minimax-AlphaBeta informed search algorithm - Two players games

# X_and_0.py
      Tabla de joc are dimensiune 3 x 3.
      Cei 2 jucatori isi atribuie la inceput unul din simbolurile “X” si ”0”. Mereu prima mutare este a
    jucatorului care are simbolul “X”. Cei 2 jucatori pun alternativ simbolul propriu intr-o casuta
    goala.
      Castiga jucatorul care are 3 simboluri adiacente pe o linie, coloana sau diagonala. Daca toate
    9 casutele sunt completate, dar nu a castigat niciun jucator, atunci jocul se termina cu remiza.
    
# connect4.py
      Tabla de joc are 6 linii si 7 coloane si este pozitionata vertical (perpendicular pe masa).
      Se stabilesc simbolurile care vor fi folosite de fiecare dintre cei 2 jucatori (puteti folosi tot “X”
    si “0”; sau “G” si “R” de la galben si rosu). Mereu muta primul jucatorul cu “X” (sau cu “G”),
    apoi cei doi muta alternativ.
      Jucatorul curent isi alege o coloana (care nu este complet plina) si pune piesa cu simbolul sau
    in dreptul acelei coloane. Tabla de joc fiind verticala, piesa va ajunge pe cea mai jos pozitie
    libera de pe acea coloana.
      Castiga jucatorul care are 4 simboluri adiacente pe linie, coloana, diagonala \ sau diagonala /.
      Daca toate 42 casutele sunt completate, dar nu a castigat niciun jucator, atunci jocul se
    termina cu remiza.
