import numpy as np
import cv2

img = cv2.imread("BespielFeld.png")
cv2.imshow("BespielFeld.png", img)

cv2.waitKey(0)
cv2.destroyAllWindows()