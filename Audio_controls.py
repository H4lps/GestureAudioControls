#Libraries
import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
# Open webcam
cap = cv2.VideoCapture(0)
#Counters
up_counter,down_counter,pause_counter,skip_counter = 0,0,0,0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip for mirror view
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        #Picking the first hand and drawing nodes
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Get all of the essential nodes
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
        index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
        ring_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
        thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

        #Getting specific distances and correcting with the relative dimensions of the camera
        h, w, _ = frame.shape
        x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
        x2, y2 = int(index_tip.x * w), int(index_tip.y * h)
        x3,y3 = int(middle_tip.x * w), int(middle_tip.y *h)
        x4, y4 = int(pinky_tip.x * w), int(pinky_tip.y * h)

        #Conditions for a fist
        skip_condition = (
                            ring_tip.y > ring_mcp.y and
                            middle_tip.y >middle_mcp.y and
                            index_tip.y>index_mcp.y and
                            pinky_tip.y>pinky_mcp.y 
        )          
        #Conditions to tell if certain fingers are folded
        fingers_folded = (ring_tip.y > ring_mcp.y and
                            middle_tip.y >middle_mcp.y and
                            pinky_tip.y>pinky_mcp.y )

        #index finger pointing up for volume up
        if index_tip.y < index_mcp.y and fingers_folded:
            up_counter+= 1
            if up_counter>15:
                pyautogui.press("volumeup")
                up_counter = 12
        else:
            up_counter=0
        #Pinching thumb with index and middle finger
        down_distance = ((x2-x1)**2 + (y2-y1)**2)**.5 + ((x3-x1)**2+ (y3-y1)**2)**.5
        if down_distance <80:
            down_counter+= 1
            if down_counter>15:
                pyautogui.press("volumedown")
                down_counter = 10
        else:
            down_counter=0
        #Pinching pinky and thumb to pause
        pause_distnace = ((x4-x1)**2 + (y4 -y1)**2)**0.5
        if pause_distnace<30:
            pause_counter+=1
            if pause_counter>20:
                pyautogui.press("playpause")
                pause_counter = -20
        else:
            pause_counter=0
        
        #Fist for skipping the song
        if skip_condition:
            skip_counter+=1
            if skip_counter >20:
                pyautogui.press("nexttrack")
                skip_counter=-20
        else:
            skip_counter =0
    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        

cap.release()
cv2.destroyAllWindows()
 


