MODE 0
PRINT TAB(r,c)
# ascii repr of QR code
A$ = "ABCDEF"
C% = MID$(A$,i)
# loop 7 times
C% = C% / 2
IF (C% MOD 2 == 1)
