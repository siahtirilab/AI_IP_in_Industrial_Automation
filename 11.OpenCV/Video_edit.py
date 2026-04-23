import cv2

cap = cv2.VideoCapture(0)
lower_green = (35, 50, 50)
upper_green = (85, 255, 255)
count = []
while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    contours, hierarchy = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        if cv2.contourArea(contour) > 100:
            count.append(cv2.contourArea(contour))
    text = str(len(count))
    cv2.putText(frame, text, (20,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 5)
    cv2.imshow('frame', frame)
    #print(cap.get(3), cap.get(4))
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()