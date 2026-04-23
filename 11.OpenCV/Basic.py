import cv2

img = cv2.imread("circles.jpg")
gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (9,9), 0)
resized = cv2.resize(img, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_AREA)
cv2.imshow("Original", resized)
cv2.imshow("Gray", gray)
cv2.waitKey()
cv2.destroyAllWindows()