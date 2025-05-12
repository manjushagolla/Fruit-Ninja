
# **🍉 Gesture-Controlled Fruit Ninja Game 🎮 (Pygame + OpenCV + MediaPipe)**





A fun and interactive version of the classic Fruit Ninja game built with Python, using Pygame for graphics, OpenCV for webcam input, and MediaPipe for real-time hand tracking. Slice fruits by moving your finger on camera — no mouse or touch required!

---

**✨ Features**

1.🎥 Gesture Control: Slice fruits with your index finger using real-time hand tracking.

2.💣 Bombs & Explosions: Avoid bombs or it's game over!

3.⏱️ Timer: 2-minute game time with score tracking.

4.🔊 Sound Effects & Music: Includes background music, fruit cut sound, and explosion effect.

5.📈 Levels & Combo System: Progressive levels based on score and combo bonus.

6.🍓 Multiple Fruits: Apples, bananas, oranges, strawberries, and watermelons.


---

**🛠️ Installation**

**Prerequisites**

1.Python 3.7 or above

2.Webcam

# **Install Dependencies**

git clone https://github.com/your-username/gesture-fruit-ninja.git

cd gesture-fruit-ninja

**Create a virtual environment (optional)**

python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

**Install required packages**

pip install -r requirements.txt

**▶️ Running the Game**

python sound.py

---


# **⌛ Game Mechanics**

1.🎮 Start Screen:  Press Enter to begin the game.

2.🄹️ Gameplay:  Slice fruits using your finger tracked via webcam (MediaPipe + OpenCV).

3.💣 Bombs: If your finger touches a bomb, the game ends with an explosion.

4.🕐 Timer:  120 seconds of gameplay.

5.🔢 Levels:  Unlock higher levels when your score crosses 100, 200, 300, etc.

6.💥 Combos:  Cutting multiple fruits increases your combo score.

