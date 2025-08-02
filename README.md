<<<<<<< HEAD
<div align="center">

# 📰 RetroFake-Hunter
**📰 Real Time Fake News Detector - Retro design. Sharp ML. Instant Verdict.**

🪟 A retro styled Windows XP GUI app to detect real vs fake news in real time!  
Branded with 💗 by [Y7X-bit](https://github.com/Y7X-bit)

<img src="assets/1.png" alt="Manual Tab UI" width="600"/>

<img src="assets/2.png" alt="Live News Tab Preview" width="600"/>

</div>
=======
# 📰 Real-Time Fake News Detector v1.0

🪟 *A retro-styled Windows 2000 GUI app to detect real vs fake news — in real-time!*

> Uses machine learning (PassiveAggressiveClassifier + TF-IDF) to classify news headlines from manual input or live sources via NewsAPI.
>>>>>>> fb4a3ef (🌀 First commit — RetroFakeHunter v1.0 with full retro UI)

---

## ⚡ Features
<<<<<<< HEAD

- 🧠 Manual text based analysis with confidence scores
- 📰 Live news feed scanning (CNN, BBC, Reuters & more)
- ❗ Clickbait detection + suspicious links handling
- 📊 Visual feedback via retro treeview & status bars
- 🪟 Windows XP GUI with tabs, beveled frames & nostalgia
- 💾 Save & bookmark results as `.txt` logs
- 🚀 Runs offline for manual mode (no NewsAPI required)

---

## 🖥️ Installation

> Python 3.9 or later required

```bash
git clone https://github.com/Y7X-bit/RetroFake-Hunter.git
cd RetroFake-Hunter
pip install -r requirements.txt
python RetroFake-Hunter.py GUI
=======
- Manual text-based analysis with confidence scores.
- Live news feed analysis from top sources like CNN, BBC, Reuters.
- Sensationalism & link detection to boost analysis.
- Classic Windows 2000 GUI style for max nostalgia 🖥️

---

## 📸 UI Preview  
> Windows 2000 style with retro tab layout, treeview, beveled frames, and status bars.

### 🔹 Manual Analysis Tab
![Manual Tab](assets/1.png)

---

### 🔹 Live News Analysis Tab
![Live Tab](assets/2.png)

---

## 🧠 How It Works

- Converts text into vectors using `TfidfVectorizer`  
- Trains a `PassiveAggressiveClassifier` on sample fake/real news  
- Predicts with a probability-based confidence level  
- Highlights suspicious headlines and clickbait words

---

## 🛠️ Setup & Run

📦 Install dependencies:
```bash
pip install -r requirements.txt
>>>>>>> fb4a3ef (🌀 First commit — RetroFakeHunter v1.0 with full retro UI)
