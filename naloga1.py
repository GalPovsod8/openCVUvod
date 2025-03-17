import cv2 as cv
import numpy as np

def zmanjsaj_sliko(slika, sirina, visina):  # CHECK [Y]
    '''Zmanjšaj sliko na velikost sirina x visina.'''
    return cv.resize(slika, (sirina, visina))

def prestej_piklse_z_barvo_koze(slika, barva_koze) -> int:  # CHECK [Y]
    '''Prešteje število pikslov kože v škatli.'''
    spodnja_meja, zgornja_meja = barva_koze
    maska = cv.inRange(slika, spodnja_meja, zgornja_meja)
    return np.count_nonzero(maska)

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze) -> list:
    '''Pregleda sliko z velikostjo škatle in prešteje piksle kože v vsaki škatli.
    Vrne seznam s številom pikslov kože v posameznih škatlah.'''

    visina, sirina, _ = slika.shape
    rezultati = []
    
    for y in range(0, visina - visina_skatle, visina_skatle):
        for x in range(0, sirina - sirina_skatle, sirina_skatle):
            skatla = slika[y:y + visina_skatle, x:x + sirina_skatle]
            stevilka_pikslov = prestej_piklse_z_barvo_koze(skatla, barva_koze)
            rezultati.append(stevilka_pikslov)
    return rezultati

def doloci_barvo_koze(slika, levo_zgoraj, desno_spodaj) -> tuple:
    '''Določi barvo kože na podlagi ROI (region of interest).'''
    roi = slika[levo_zgoraj[1]:desno_spodaj[1], levo_zgoraj[0]:desno_spodaj[0]]
    povprecna_barva = np.mean(roi, axis=(0, 1)).astype(np.uint8)

    spodnja_meja = np.clip(povprecna_barva - 30, 0, 255).astype(np.uint8)
    zgornja_meja = np.clip(povprecna_barva + 30, 0, 255).astype(np.uint8)

    return spodnja_meja, zgornja_meja

if __name__ == '__main__':
    kamera = cv.VideoCapture(0)

    if not kamera.isOpened():
        print('Kamera ni bila odprta.')
    else:
        ret, prva_slika = kamera.read()
        prva_slika = zmanjsaj_sliko(prva_slika, 320, 240)

        visina, sirina, _ = prva_slika.shape
        levo_zgoraj = (sirina // 3, visina // 3)
        desno_spodaj = (2 * sirina // 3, 2 * visina // 3)

        barva_koze = doloci_barvo_koze(prva_slika, levo_zgoraj, desno_spodaj)

        sirina_skatle, visina_skatle = 40, 40
        stolpci = (sirina - sirina_skatle) // sirina_skatle

        while True:
            ret, slika = kamera.read()
            # cv.imshow('Kamera', slika)

            slika = zmanjsaj_sliko(slika, 320, 240)
            skatle = obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze)

            for indeks, piksli in enumerate(skatle):
                if piksli > 100:
                    i = indeks // stolpci
                    j = indeks % stolpci
                    x, y = j * sirina_skatle, i * visina_skatle
                    cv.rectangle(slika, (x, y), (x + sirina_skatle, y + visina_skatle), (0, 255, 0), 2)

            cv.imshow('Detekcija Obraza', slika)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        kamera.release()
        cv.destroyAllWindows()
