import cv2

img = cv2.imread('image_2026-10-22_10-10-27.png')

# In OpenCV/NumPy ist die Reihenfolge: (Höhe, Breite, Farbkanäle)
h, w = img.shape[:2]

print(f"Breite: {w} Pixel")
print(f"Höhe:   {h} Pixel")