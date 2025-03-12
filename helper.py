# helper.py

def dostop_do_piksla(slika, x, y):
    '''Dostop do piksla.'''
    return slika[y, x]

def izrezi_del_slike(slika, x, y, sirina, visina):
    '''Izreži del slike.'''
    return slika[y:y+visina, x:x+sirina]

def shranjevanje_slike(slika, ime_slike):
    '''Shrani sliko.'''
    cv.imwrite(ime_slike, slika)

def spremeni_velikost_slike_faktor(slika, f):
    '''Spremeni velikost slike za faktor f.'''
    return cv.resize(slika, (0, 0), fx=f, fy=f)

def spremeni_velikost_slike_diskretno(slika, sirina, visina):
    '''Spremeni velikost slike na določeno širino in višino.'''
    return cv.resize(slika, (sirina, visina))