import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. Funktion: Transformation mit Nächste-Nachbarn (Aufgabe 2)
# -------------------------------------------------------------
def scherung_naechste_nachbarn(img, sx, richtung='rueckwaerts'):
    h, w = img.shape
    w_neu = int(np.ceil(w + sx * h))
    h_neu = h
    img_ziel = np.zeros((h_neu, w_neu), dtype=np.uint8)

    if richtung == 'vorwaerts':
        # 2a. Vorwärts-Transformation (Schleife über Quellbild)
        for y in range(h):
            for x in range(w):
                x_strich = int(np.round(x + sx * y))
                y_strich = y
                if 0 <= x_strich < w_neu:
                    img_ziel[y_strich, x_strich] = img[y, x]
                    
    elif richtung == 'rueckwaerts':
        # 2b. Rückwärts-Transformation (Schleife über Zielbild)
        for y_strich in range(h_neu):
            for x_strich in range(w_neu):
                x = x_strich - sx * y_strich
                y = y_strich
                
                x_nn = int(np.round(x))
                y_nn = int(np.round(y))
                
                if 0 <= x_nn < w and 0 <= y_nn < h:
                    img_ziel[y_strich, x_strich] = img[y_nn, x_nn]
                    
    return img_ziel


# -------------------------------------------------------------
# 2. Funktion: Rückwärts-Transformation mit Bilinearer Interpolation (Aufgabe 3)
# -------------------------------------------------------------
def scherung_bilinear(img, sx):
    h, w = img.shape
    w_neu = int(np.ceil(w + sx * h))
    h_neu = h
    img_ziel = np.zeros((h_neu, w_neu), dtype=np.uint8)
    
    img_float = img.astype(np.float32)

    # Schleife über alle Pixel des Zielbildes (Rückwärts)
    for y_strich in range(h_neu):
        for x_strich in range(w_neu):
            # Schritt 1: Transformierte Gleitkomma-Koordinate (Folie 40)
            x = x_strich - sx * y_strich
            y = float(y_strich)
            
            # Prüfen, ob der Punkt im Quellbild liegt
            if 0 <= x < w and 0 <= y < h:
                # Schritt 2: Vier ganzzahlige Nachbar-Pixel mit np.floor bestimmen (Folie 40)
                x0 = int(np.floor(x))
                y0 = int(np.floor(y))
                x1 = min(x0 + 1, w - 1)
                y1 = min(y0 + 1, h - 1)
                
                # Schritt 3: Gewichte nach Folie 41 berechnen
                wx = x - np.floor(x)
                wy = y - np.floor(y)
                
                w00 = (1.0 - wx) * (1.0 - wy)
                w01 = wx * (1.0 - wy)
                w10 = (1.0 - wx) * wy
                w11 = wx * wy
                
                # Neue Intensität als gewichtete Summe der 4 Nachbarn (Folie 41)
                val = (w00 * img_float[y0, x0] +
                       w01 * img_float[y0, x1] +
                       w10 * img_float[y1, x0] +
                       w11 * img_float[y1, x1])
                
                img_ziel[y_strich, x_strich] = int(np.round(val))

    return img_ziel


# =============================================================
# Hauptprogramm
# =============================================================
# Bild laden
img = plt.imread('cameraman.pgm')
sx = 0.3

# Transformationen durchführen
img_vorwaerts_nn   = scherung_naechste_nachbarn(img, sx, richtung='vorwaerts')
img_rueckwaerts_nn = scherung_naechste_nachbarn(img, sx, richtung='rueckwaerts')
img_rueckwaerts_bi = scherung_bilinear(img, sx)

# Alle 4 Bilder nebeneinander plotten
fig, axs = plt.subplots(1, 4, figsize=(20, 5))

axs[0].imshow(img, cmap='gray', vmin=0, vmax=255)
axs[0].set_title("1. Originalbild")
axs[0].axis('off')

axs[1].imshow(img_vorwaerts_nn, cmap='gray', vmin=0, vmax=255)
axs[1].set_title("2a. Vorwärts (NN)\n(Löcher/Moiré)")
axs[1].axis('off')

axs[2].imshow(img_rueckwaerts_nn, cmap='gray', vmin=0, vmax=255)
axs[2].set_title("2b. Rückwärts (NN)\n(stufige Kanten)")
axs[2].axis('off')

axs[3].imshow(img_rueckwaerts_bi, cmap='gray', vmin=0, vmax=255)
axs[3].set_title("3. Rückwärts (Bilinear)\n(glatte Kanten)")
axs[3].axis('off')

plt.tight_layout()
plt.show()
