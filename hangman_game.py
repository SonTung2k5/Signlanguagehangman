import cv2
import random
import pickle
import numpy as np
import mediapipe as mp
import time
import pygame
import pandas as pd
import sys

pygame.mixer.init()
pygame.mixer.music.load('03. WHITE NIGHT (Japanese Ver.).mp3')
pygame.mixer.music.play(-1)

# Hangman game logic
level = sys.argv[1] if len(sys.argv) > 1 else 'easy'

words = {
    'easy': ['apple', 'ball', 'cat', 'dog', 'egg'],
    'medium': ['camera', 'python', 'guitar', 'flower', 'window'],
    'hard': ['hangman', 'difficult', 'xylophone', 'quizzical', 'juxtapose']
}

word = random.choice(words[level]).upper()
guessed = set()
wrong_guesses = set()
max_attempts = 8

# Load the trained model
model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Define labels
labels_dict = {10: 'S', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J', 20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'A', 29: 'T', 30: 'U', 31: 'W', 32: 'X', 33: 'Y', 34: 'Z', 35: 'V'}

# Read the user's name from the file
try:
    with open('user_name.txt', 'r') as f:
        user_name = f.read()
except FileNotFoundError:
    user_name = "Player"
    
# Initialize score
score = 0

def save_final_score(user_name, score):
    # Save to text file
    with open('leaderboard.txt', 'w') as f:  # Use 'w' mode to overwrite the file
        f.write(f'{user_name}: {score}\n')

def display_game_state(frame, word, guessed, wrong_guesses, max_attempts, score):
    # Display the word with guessed letters
    display_word = ' '.join([letter if letter in guessed else '_' for letter in word])
    cv2.putText(frame, display_word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display wrong guesses
    wrong_guesses_text = 'Wrong guesses: ' + ' '.join(wrong_guesses)
    cv2.putText(frame, wrong_guesses_text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
     # Display the user's name at the bottom-left corner
    height, width, _ = frame.shape
    cv2.putText(frame, f'Player: {user_name}', (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # Display remaining attempts
    attempts_left = max_attempts - len(wrong_guesses)
    attempts_text = f'Attempts left: {attempts_left}'
    cv2.putText(frame, attempts_text, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)

    # Display score at the bottom-right corner
    score_text = f'Score: {score}'
    cv2.putText(frame, score_text, (width - 200, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Draw stickman based on wrong guesses
    if len(wrong_guesses) > 0:
        cv2.line(frame, (200, 300), (200, 100), (255, 255, 255), 2)  # Pole
    if len(wrong_guesses) > 1:
        cv2.line(frame, (200, 100), (300, 100), (255, 255, 255), 2)  # Top bar
    if len(wrong_guesses) > 2:
        cv2.line(frame, (300, 100), (300, 150), (255, 255, 255), 2)  # Rope
    if len(wrong_guesses) > 3:
        cv2.circle(frame, (300, 170), 20, (255, 255, 255), 2)  # Head
    if len(wrong_guesses) > 4:
        cv2.line(frame, (300, 190), (300, 250), (255, 255, 255), 2)  # Body
    if len(wrong_guesses) > 5:
        cv2.line(frame, (300, 210), (270, 230), (255, 255, 255), 2)  # Left arm
    if len(wrong_guesses) > 6:
        cv2.line(frame, (300, 210), (330, 230), (255, 255, 255), 2)  # Right arm
    if len(wrong_guesses) > 7:
        cv2.line(frame, (300, 250), (270, 290), (255, 255, 255), 2)  # Left leg
    if len(wrong_guesses) > 8:
        cv2.line(frame, (300, 250), (330, 290), (255, 255, 255), 2)  # Right leg

    # Check for win or lose
    if set(word) == guessed:
        cv2.putText(frame, 'You Win!', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        save_final_score(user_name, score)
        cv2.putText(frame, f'Your Score: {score}', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    elif attempts_left == 0:
        cv2.putText(frame, f'You Lose! The word was {word}', (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        save_final_score(user_name, score)
        cv2.putText(frame, f'Your Score: {score}', (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

# Start video capture
cap = cv2.VideoCapture(0)
last_update_time = time.time()
gesture_detected_time = None  # Initialize the gesture detected time
background = cv2.imread('thanhngu.jpg')
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_resized = cv2.resize(frame, (200, 150))
    # Display the game state on the frame
    display_game_state(frame, word, guessed, wrong_guesses, max_attempts, score)

    # Hand gesture recognition
    data_aux = []
    x_ = []
    y_ = []

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        prediction = model.predict([np.asarray(data_aux)])
        gesture = labels_dict[int(prediction[0])]

        if gesture == 'A':
            letter = 'A'  # Example: map upward gesture to 'A'
        elif gesture == 'B':
            letter = 'B'  
        elif gesture == 'C':
            letter = 'C' 
        elif gesture == 'D':
            letter = 'D'
        elif gesture == 'E':
            letter = 'E'
        elif gesture == 'F':
            letter = 'F'
        elif gesture == 'G':
            letter = 'G'
        elif gesture == 'H':
            letter = 'H'
        elif gesture == 'I':
            letter = 'I'
        elif gesture == 'J':
            letter = 'J'
        elif gesture == 'K':
            letter = 'K'
        elif gesture == 'L':
            letter = 'L'
        elif gesture == 'M':
            letter = 'M'
        elif gesture == 'N':
            letter = 'N'
        elif gesture == 'O':
            letter = 'O'
        elif gesture == 'P':
            letter = 'P'
        elif gesture == 'Q':
            letter = 'Q'
        elif gesture == 'R':
            letter = 'R'
        elif gesture == 'S':
            letter = 'S'
        elif gesture == 'T':
            letter = 'T'
        elif gesture == 'U':
            letter = 'U'
        elif gesture == 'V':
            letter = 'V'
        elif gesture == 'W':
            letter = 'W'
        elif gesture == 'X':
            letter = 'X'
        elif gesture == 'Y':
            letter = 'Y'
        elif gesture == 'Z':
            letter = 'Z'
        else:
            letter = None

        current_time = time.time()
        if letter:
            if gesture_detected_time is None:
                gesture_detected_time = current_time  # Record the time when the gesture is first detected
            elif current_time - gesture_detected_time >= 6:  # Check if 2 seconds have passed since the gesture was first detected
                gesture_detected_time = None  # Reset the gesture detected time
                last_update_time = current_time  # Update the last update time
                if letter in word:
                    guessed.add(letter)
                    score += 10  # Increment score by 10 for each correct guess
                else:
                    wrong_guesses.add(letter)
                    score -= 5  # Decrement score by 5 for each wrong guess
        else:
            gesture_detected_time = None
            
    background[10:160, 10:210] = frame_resized  # Adjust the position as needed
    cv2.imshow('Hangman Game', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()