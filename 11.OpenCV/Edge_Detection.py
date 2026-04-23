import cv2

img = cv2.imread("cars.jpg")

edged = cv2.Canny(img, 100, 200)
edges = cv2.Laplacian(img, cv2.CV_8U)

cv2.imshow("Laplacian", edges)
cv2.imshow("Canny", edged)
cv2.waitKey(0)
cv2.destroyAllWindows()