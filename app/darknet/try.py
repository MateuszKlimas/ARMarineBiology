import cv2


out = cv2.VideoWriter("output-TEST.avi", cv2.VideoWriter_fourcc(*"MJPG"), 50.0,
        (960,544))



cap = cv2.VideoCapture("output-test3.avi")
cap.set(cv2.CAP_PROP_FPS, 5)
while True: 
    ret, frame_read = cap.read()
    cv2.imshow('Demos', frame_read)
    out.write(frame_read)
    cv2.waitKey(1)

out.set(cv2.CAP_PROP_FPS,50)
cap.release()
out.release()