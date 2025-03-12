import cv2 as cv
import numpy as np
#from helper import dostop_do_piksla, izrezi_del_slike

def zmanjsaj_sliko(slika, sirina, visina): #CHECK [Y]
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    cv.resize(slika, (sirina, visina))
    pass

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Sprehodi se skozi sliko v velikosti škatle (sirina_skatle x visina_skatle) in izračunaj število pikslov kože v vsaki škatli.
    Škatle se ne smejo prekrivati!
    Vrne seznam škatel, s številom pikslov kože.
    Primer: Če je v sliki 25 škatel, kjer je v vsaki vrstici 5 škatel, naj bo seznam oblike
      [[1,0,0,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1]]. 
      V tem primeru je v prvi škatli 1 piksel kože, v drugi 0, v tretji 0, v četrti 1 in v peti 1.'''

    visina, sirina, _ = slika.shape
    rezultati = []
    for y in range(0, visina - visina_skatle, visina_skatle):
        for x in range(0, sirina - sirina_skatle, sirina_skatle):
            skatla = slika[y:y + visina_skatle, x:x + sirina_skatle]
            stevilka_pikslov = prestej_piksle_z_barvo_koze(skatel, barva_koze)
            rezultati.append(stevilka_pikslov)
    return rezultati
    pass

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int: #CHECK [Y]
    '''Prestej število pikslov z barvo kože v škatli.'''
    spodnja_meja, zgornja_meja = barva_koze
    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    return np.count_nonzero(maska)
    pass

def doloci_barvo_koze(slika,levo_zgoraj,desno_spodaj) -> tuple: #CHECK [Y]
    '''Ta funkcija se kliče zgolj 1x na prvi sliki iz kamere. 
    Vrne barvo kože v območju ki ga definira oklepajoča škatla (levo_zgoraj, desno_spodaj).
      Način izračuna je prepuščen vaši domišljiji.'''

    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
    povprecna_barva = np.mean(roi, axis=(0, 1))
    spodnja_meja = np.array([max(0, povprecna_barva - 30)], dtype=np.uint8)
    zgornja_meja = np.array([min(255, povprecna_barva + 30)], dtype=np.uint8)
    return spodnja_meja, zgornja_meja
    pass

if __name__ == '__main__':
    #Pripravi kamero - CHECK [?]

    # Naložimo kamero - CHECK [Y]
    kamera = cv.VideoCapture(0)
    # Preverimo, če je kamera pravilno naložena  - CHECK [Y]
    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        while True:
            # Preberemo sliko iz kamere
            ret, slika = kamera.read()
            cv.imshow('Kamera', slika)
            # Če pritisnemo tipko 'q', zapremo okno
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        # Zapremo okno
        kamera.release()
        cv.destroyAllWindows()
    pass

    #Zajami prvo sliko iz kamere

    #Izračunamo barvo kože na prvi sliki

    #Zajemaj slike iz kamere in jih obdeluj     
    
    #Označi območja (škatle), kjer se nahaja obraz (kako je prepuščeno vaši domišljiji)
        #Vprašanje 1: Kako iz števila pikslov iz vsake škatle določiti celotno območje obraza (Floodfill)?
        #Vprašanje 2: Kako prešteti število ljudi?

        #Kako velikost prebirne škatle vpliva na hitrost algoritma in točnost detekcije? Poigrajte se s parametroma velikost_skatle
        #in ne pozabite, da ni nujno da je škatla kvadratna.