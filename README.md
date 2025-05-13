🗼 Tower of Hanoi Solver (3-Peg & 4-Peg) – Streamlit App
This is an interactive Tower of Hanoi web application built using Python and Streamlit, supporting both 3-peg and 4-peg versions of the puzzle. The app features three algorithms—Recursive, Iterative, and Frame–Stewart—and stores player scores and algorithm performance statistics using Firebase.

🔧 Features
✅ Solve Tower of Hanoi with 3 or 4 pegs

🔁 Includes:
Recursive algorithm
Iterative algorithm
Frame–Stewart algorithm (for 4 pegs)

📊 Displays a scoreboard with best player performances

📈 Shows a chart comparing algorithm execution times

🎮 Interactive gameplay:

Move disks one by one (drag & drop style)
OR enter the full move sequence and submit

🎮 How to Play
Choose the number of pegs (3 or 4) and the number of disks.
The minimum number of moves required is calculated as:
moves = 2^n - 1 (for 3 pegs)

You can solve the puzzle in one of two ways:
Manually move disks, one at a time.
Submit a full sequence of moves at once.

The app will validate your solution and record your time and result in the scoreboard.

Compare the time taken by each algorithm in the performance chart.

🚀 How to Run the App
Clone the repository:
git clone https://github.com/yulaAl20/final-TOH

Navigate into the project folder:
cd tower-of-hanoi-streamlit

Install dependencies:
pip install -r requirements.txt

Run the Streamlit app:
streamlit run app.py
