import cv2
cap = cv2.VideoCapture("Video.mp4")

while True:
    ret, frame = cap.read()
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xff == ord('s'):
        break
cv2.destroyAllWindows()

