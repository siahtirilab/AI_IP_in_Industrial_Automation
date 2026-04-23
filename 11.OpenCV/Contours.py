import cv2

img = cv2.imread("coins.jpg")

edges = cv2.Canny(img, 100, 200)

contours, hierarchy = cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

counts = []
for contour in contours:
    if cv2.contourArea(contour) > 700:
        counts.append(cv2.contourArea(contour))

print(len(counts))




cv2.imshow("Lena", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()