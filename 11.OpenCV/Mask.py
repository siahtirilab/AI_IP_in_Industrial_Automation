import cv2

img = cv2.imread("cars.jpg")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_color = (20, 100, 100)
upper_color = (30, 255, 255)

lower_green = (35, 50, 50)
upper_green = (85, 255, 255)
mask_yellow = cv2.inRange(hsv, lower_color, upper_color)
mask_green = cv2.inRange(hsv, lower_green, upper_green)


cv2.imshow("Green", mask_green)
cv2.imshow("Yellow", mask_yellow)
cv2.waitKey(0)
cv2.destroyAllWindows()
