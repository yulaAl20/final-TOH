# 🗼 Tower of Hanoi Solver (3-Peg & 4-Peg) – Streamlit App


This is an interactive **Tower of Hanoi** web application built using **Python** and **Streamlit**, supporting both **3-peg** and **4-peg** versions of the puzzle. The app features **three algorithms**—**Recursive**, **Iterative**, and **Frame–Stewart**—and stores player scores and algorithm performance statistics using **Firebase**.


✅ Solve Tower of Hanoi with **3 or 4 pegs**  
🔁 Includes:
- Recursive algorithm
- Iterative algorithm
- Frame–Stewart algorithm (for 4 pegs)  
📊 Displays a **scoreboard** with best player performances  
📈 Shows a **chart comparing algorithm execution times**  
🎮 Interactive gameplay:
- Move disks one by one (drag & drop style)
- OR enter the full move sequence and submit

---

## 🎮 How to Play

1. Choose the number of pegs (3 or 4) and the number of disks.
2. The minimum number of moves required is calculated as:
moves = 2^n - 1 (for 3 pegs)

3. You can solve the puzzle in one of two ways:
- **Manually move disks**, one at a time.
- **Submit a full sequence of moves** at once.
4. The app will validate your solution and record your time and result in the **scoreboard**.
5. Compare the time taken by each algorithm in the **performance chart**.

---


## 💾 Tech Stack
Frontend: Streamlit
Backend Algorithms: Python (Recursive, Iterative, Frame–Stewart)
Database: Firebase Realtime Database
Visualization: Streamlit charts and data tables

---

## 🚀 How to Run the App

1. **Clone the repository**:
```bash
git clone https://github.com/yulaAl20/final-TOH

Navigate into the project folder:
cd tower-of-hanoi-streamlit

Install dependencies:
pip install -r requirements.txt

Run the Streamlit app:
streamlit run app.py


