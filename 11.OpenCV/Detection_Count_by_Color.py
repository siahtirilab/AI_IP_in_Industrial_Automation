import cv2

img = cv2.imread("allcircels.png")

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_green = (35, 50, 50)
upper_green = (85, 255, 255)
mask_green = cv2.inRange(hsv, lower_green, upper_green)

contours, res = cv2.findContours(mask_green,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
green_count = []
for contour in contours:
    if cv2.contourArea(contour) > 200:
        green_count.append(contour)

print(len(green_count))

cv2.imshow("img",mask_green)
cv2.waitKey(0)
cv2.destroyAllWindows()