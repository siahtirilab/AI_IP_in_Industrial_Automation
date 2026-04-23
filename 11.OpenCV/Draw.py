import cv2

img = cv2.imread("cars.jpg")
cv2.line(img, (10, 100), (400, 100), (0,255,0), 5)
cv2.circle(img, (10, 100), 20, (0,0,255), -1)
cv2.rectangle(img, (30, 200), (500, 100), (0,255,0), -1)
cv2.imshow("Gray", img)
cv2.waitKey(0)
cv2.destroyAllWindows()