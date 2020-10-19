# Tkinter - For GUI
# Opencv
# PIL


import cv2
cap= cv2.VideoCapture(0)
while True:
    ret, frame =cap.read()

    cv2.imshow("My cam", frame)
    if cv2.waitKey(20) == 27: #escape 
        break
cap.release()
cv2.destroyAllWindows()
