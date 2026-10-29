import numpy as np
import matplotlib.pyplot as plt
img = plt.imread('boats_low_contrast.pgm')

def show_image_and_histogram(img):
    # Erstellt ein Fenster mit 2 Spalten (links Bild, rechts Histogramm)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left: Bild anzeigen
    ax1.imshow(img, cmap='gray', vmin=0, vmax=255)
    ax1.set_title("Bild")
    ax1.axis('off')
    
    # img.ravel() macht aus dem 2D-Bild ein 1D-Array, damit plt.hist es verarbeiten kann
    ax2.hist(img.ravel(), bins=256, range=(0, 256), color='black', histtype='stepfilled')
    ax2.set_title("Histogramm (Häufigkeitsverteilung)")
    ax2.set_xlabel("Grauwert-Intensität")
    ax2.set_ylabel("Pixel-Anzahl")
    ax2.set_xlim([0, 255])
    
    plt.tight_layout()
    plt.show()

# Aufgabe 1
#show_image_and_histogram(img) #//brauche ich nur wenn ich ich A3 nicht laufen lasse
# result: 92 bis 170

# Aufgabe 2: Kontrastanpassung
def adjust_contrast(img):
    img_float = img.astype(np.float32)
    I_min = 92.0
    I_max = 170.0
    a1 = 255/(I_max-I_min)
    b1 = -255/(I_max-I_min)*I_min
    print("Wert a")
    print(a1)
    print("Wert b")
    print(b1)

    
    img_adjusted = 255.0 * (img_float - I_min) / (I_max - I_min)
    
    img_adjusted = np.clip(img_adjusted, 0, 255)
    return img_adjusted.astype(np.uint8)

img_enhanced = adjust_contrast(img)



# Beide Bilder und Histogramme zusammen in einem einzigen Fenster anzeigen (2 Zeilen, 2 Spalten)
fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Erste Zeile: Originalbild und Original-Histogramm
axs[0, 0].imshow(img, cmap='gray', vmin=0, vmax=255)
axs[0, 0].set_title("Originalbild")
axs[0, 0].axis('off')

axs[0, 1].hist(img.ravel(), bins=256, range=(0, 256), color='black', histtype='stepfilled')
axs[0, 1].set_title("Histogramm (Original)")
axs[0, 1].set_xlim([0, 255])

# Zweite Zeile: Angepasstes Bild und neues Histogramm
axs[1, 0].imshow(img_enhanced, cmap='gray', vmin=0, vmax=255)
axs[1, 0].set_title("Kontrastangepasstes Bild")
axs[1, 0].axis('off')

axs[1, 1].hist(img_enhanced.ravel(), bins=256, range=(0, 256), color='black', histtype='stepfilled')
axs[1, 1].set_title("Histogramm (Kontrastangepasst)")
axs[1, 1].set_xlim([0, 255])

plt.tight_layout()
plt.show()
