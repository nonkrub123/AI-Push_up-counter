import datetime
import cv2
import numpy as np
import cvzone
from cvzone.PoseModule import PoseDetector
import math

counter = 0
direction = 0
recording = False

cap = cv2.VideoCapture(0)
pd = PoseDetector(trackCon=0.70, detectionCon=0.70)

#frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frameWidth = 1280
frameHeight = 720
frameRate = int(cap.get(cv2.CAP_PROP_FPS))
def angles(lmlist, p1, p2, p3, p4, p5, p6, drawpoints):
    global counter
    global direction

    if len(lmlist) >= 17:  # Check if there are enough landmarks
        point1 = lmlist[p1]
        point2 = lmlist[p2]
        point3 = lmlist[p3]
        point4 = lmlist[p4]
        point5 = lmlist[p5]
        point6 = lmlist[p6]

        x1, y1, _ = point1  # Sho3ulder
        x2, y2, _ = point2  # Elbow
        x3, y3, _ = point3  # Wrist
        x4, y4, _ = point4  # Shoulder
        x5, y5, _ = point5  # Elbow
        x6, y6, _ = point6  # Wrist

        if drawpoints:
            # Draw circles and lines for visualization
            cv2.circle(image, (x1, y1), 10, (255, 0, 255), 5)
            cv2.circle(image, (x1, y1), 15, (0, 255, 0), 5)
            cv2.circle(image, (x2, y2), 10, (255, 0, 255), 5)
            cv2.circle(image, (x2, y2), 15, (0, 255, 0), 5)
            cv2.circle(image, (x3, y3), 10, (255, 0, 255), 5)
            cv2.circle(image, (x3, y3), 15, (0, 255, 0), 5)
            cv2.circle(image, (x4, y4), 10, (255, 0, 255), 5)
            cv2.circle(image, (x4, y4), 15, (0, 255, 0), 5)
            cv2.circle(image, (x5, y5), 10, (255, 0, 255), 5)
            cv2.circle(image, (x5, y5), 15, (0, 255, 0), 5)
            cv2.circle(image, (x6, y6), 10, (255, 0, 255), 5)
            cv2.circle(image, (x6, y6), 15, (0, 255, 0), 5)

            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 6)
            cv2.line(image, (x2, y2), (x3, y3), (0, 0, 255), 6)
            cv2.line(image, (x4, y4), (x5, y5), (0, 0, 255), 6)
            cv2.line(image, (x5, y5), (x6, y6), (0, 0, 255), 6)
            cv2.line(image, (x1, y1), (x4, y4), (0, 0, 255), 6)

        lefthandangle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                                      math.atan2(y1 - y2, x1 - x2))

        righthandangle = math.degrees(math.atan2(y6 - y5, x6 - x5) -
                                       math.atan2(y4 - y5, x4 - x5))

        leftHandAngle = int(np.interp(lefthandangle, [-30, 180], [100, 0]))
        rightHandAngle = int(np.interp(righthandangle, [34, 173], [100, 0]))

        left, right = leftHandAngle, rightHandAngle

        # Additional condition: Check if nose (landmark 0) is below knees (landmarks 25 and 26)
        if lmlist[0][1] > lmlist[25][1] and lmlist[0][1] > lmlist[26][1]:
            if left >= 70 and right >= 70:
                if direction == 0:
                    counter += 0.5
                    direction = 1
            if left <= 70 and right <= 70:
                if direction == 1:
                    counter += 0.5
                    direction = 0

        cv2.rectangle(image, (0, 0), (120, 120), (255, 0, 0), -1)
        cv2.putText(image, str(int(counter)), (20, 70), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1.6, (0, 0, 255), 7)

        leftval = np.interp(right, [0, 100], [400, 200])
        rightval = np.interp(right, [0, 100], [400, 200])

        cv2.putText(image, 'R', (24, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 4)
        cv2.rectangle(image, (8, 200), (50, 400), (0, 255, 0), 5)
        cv2.rectangle(image, (8, int(rightval)), (50, 400), (255, 0, 0), -1)

        cv2.putText(image, 'L', (962, 195), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 4)
        cv2.rectangle(image, (952, 200), (995, 400), (0, 255, 0), 5)
        cv2.rectangle(image, (952, int(leftval)), (995, 400), (255, 0, 0), -1)

        if left > 70:
            cv2.rectangle(image, (952, int(leftval)), (995, 400), (0, 0, 255), -1)

        if right > 70:
            cv2.rectangle(image, (8, int(leftval)), (50, 400), (0, 0, 255), -1)

while True:
    ret, frame = cap.read()
    if not ret:
        cap = cv2.VideoCapture('push_up.mp4')
        continue

    image = cv2.resize(frame, (frameWidth, frameHeight))
    cvzone.putTextRect(image, 'AI Push Up Counter', [345, 30], colorT=(255,91, 31),colorR=(255,255, 120),colorB=(255,174, 31), thickness=2, border=2, scale=2.5)
    pd.findPose(image, draw=0)
    lmlist, bbox = pd.findPosition(image, draw=0, bboxWithHands=0)

    angles(lmlist, 11, 13, 15, 12, 14, 16, drawpoints=1)

    if recording:
        out.write(image)

    cv2.imshow('frame', image)
    
    # Check for key press 'q' to quit
    if cv2.waitKey(1) == ord('q'):
        break

    # Start recording if push-up is detected
    if counter > 0 and not recording:
        recording = True
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'C:\\Users\\ticha\\Videos\\{current_time}.mov'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for saving video as MP4
        out = cv2.VideoWriter(filename, fourcc, 20.0, (frameWidth, frameHeight))  # Output file name, codec, frame rate, frame size

# Release resources
cap.release()
cv2.destroyAllWindows()
