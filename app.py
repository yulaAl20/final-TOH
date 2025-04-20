import streamlit as st
import time
import random
import pandas as pd

# Import from local modules
from database import init_db, save_result, get_leaderboard
from algorithms import solve_hanoi_recursive, solve_hanoi_iterative, solve_frame_stewart
from game_logic import init_game_state, is_valid_move, apply_move, is_solved
from ui_components import render_game_board

# Helper function to check if game is solved and handle winning state
def check_game_solved():
    if is_solved(st.session_state.game_state, st.session_state.disk_count):
        st.balloons()
        st.success(f"Congratulations! You solved the puzzle in {st.session_state.move_count} moves!")
        
        # Get player name from session state
        player_name = st.session_state.get("player_name", "Player")
        
        # Compare with algorithms
        compare_algorithms(player_name, st.session_state.disk_count, 
                         st.session_state.move_count, ",".join(st.session_state.moves_made))
        
        # Reset game
        st.session_state.game_active = False
        return True
    return False

# Helper function to compare algorithms and save results
def compare_algorithms(player_name, disk_count, moves_count, move_sequence):
    # Compare with algorithms
    recursive_moves, recursive_time = solve_hanoi_recursive(disk_count, 'A', 'B', 'C')
    iterative_moves, iterative_time = solve_hanoi_iterative(disk_count, 'A', 'B', 'C')
    
    st.write(f"Recursive algorithm solved it in {len(recursive_moves)} moves in {recursive_time:.6f} seconds")
    st.write(f"Iterative algorithm solved it in {len(iterative_moves)} moves in {iterative_time:.6f} seconds")
    
    # Save results for 3 pegs
    save_result(player_name, disk_count, moves_count, move_sequence, 
               "Player Solution (3 pegs)", 0)
    save_result("Algorithm", disk_count, len(recursive_moves), 
               ",".join(recursive_moves), "Recursive", recursive_time)
    save_result("Algorithm", disk_count, len(iterative_moves), 
               ",".join(iterative_moves), "Iterative", iterative_time)
    
    # If 4 pegs were used, also compare with Frame-Stewart
    if st.session_state.peg_count == 4:
        fs_moves, fs_time = solve_frame_stewart(disk_count, 'A', 'B', 'C', 'D')
        st.write(f"Frame-Stewart algorithm (4 pegs) solved it in {len(fs_moves)} moves in {fs_time:.6f} seconds")
        
        # Save results for 4 pegs
        save_result(player_name, disk_count, moves_count, move_sequence, 
                   "Player Solution (4 pegs)", 0)
        save_result("Algorithm", disk_count, len(fs_moves), 
                   ",".join(fs_moves), "Frame-Stewart (4 pegs)", fs_time)

# Main application
def main():
    st.set_page_config(page_title="Tower of Hanoi Game", layout="wide")
    
    # Initialize database
    init_db()
    
    # App title
    st.title("Tower of Hanoi Game")
    
    # Initialize session state
    if 'game_active' not in st.session_state:
        st.session_state.game_active = False
    if 'disk_count' not in st.session_state:
        st.session_state.disk_count = 0
    if 'game_state' not in st.session_state:
        st.session_state.game_state = {}
    if 'move_count' not in st.session_state:
        st.session_state.move_count = 0
    if 'moves_made' not in st.session_state:
        st.session_state.moves_made = []
    if 'optimal_moves' not in st.session_state:
        st.session_state.optimal_moves = []
    if 'peg_count' not in st.session_state:
        st.session_state.peg_count = 3
    if 'move_sequence' not in st.session_state:
        st.session_state.move_sequence = ""
    
    # Sidebar for game options
    st.sidebar.header("Game Options")
    
    # Menu options
    menu = st.sidebar.selectbox("Menu", ["Play Tower of Hanoi", "Leaderboard", "Algorithm Comparison"])
    
    # Check for drag and drop move submission
    if 'source' in st.query_params and 'destination' in st.query_params:
        source = st.query_params['source'][0]
        destination = st.query_params['destination'][0]
        
        if source and destination and st.session_state.game_active:
            if apply_move(st.session_state.game_state, source, destination):
                st.session_state.move_count += 1
                st.session_state.moves_made.append(f"{source}->{destination}")
                st.session_state.move_sequence = ",".join(st.session_state.moves_made)
                
                # Check if game is solved
                check_game_solved()

    if menu == "Play Tower of Hanoi":
        st.header("Play Tower of Hanoi")
        
        # Game setup
        col1, col2, col3 = st.columns(3)
        
        with col1:
            player_name = st.text_input("Your Name", key="player_name")
        
        with col2:
            peg_count = st.radio("Number of Pegs", [3, 4], key="peg_selection")
        
        with col3:
            if st.button("Start New Game"):
                # Generate random disk count between 5 and 10
                disk_count = random.randint(5, 10)
                st.session_state.disk_count = disk_count
                st.session_state.peg_count = peg_count
                st.session_state.game_state = init_game_state(disk_count)
                st.session_state.game_active = True
                st.session_state.move_count = 0
                st.session_state.moves_made = []
                st.session_state.move_sequence = ""
                
                # Calculate optimal moves
                if peg_count == 3:
                    st.session_state.optimal_moves, _ = solve_hanoi_recursive(disk_count, 'A', 'B', 'C')
                else:
                    st.session_state.optimal_moves, _ = solve_frame_stewart(disk_count, 'A', 'B', 'C', 'D')
                
                st.success(f"Started a new game with {disk_count} disks and {peg_count} pegs!")
        
        if st.session_state.game_active:
            st.write(f"Current game: {st.session_state.disk_count} disks with {st.session_state.peg_count} pegs")
            st.write(f"Minimum moves required: {len(st.session_state.optimal_moves)}")
            st.write(f"Moves made so far: {st.session_state.move_count}")
            
            # Display the move sequence
            if st.session_state.moves_made:
                st.write("Move sequence: " + ", ".join(st.session_state.moves_made))
            
            # Display the game board with drag and drop enabled
            render_game_board(st.session_state.game_state, st.session_state.disk_count, st.session_state.peg_count)
            
            # Move input (as alternative to drag and drop)
            st.subheader("Make a Move")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                source = st.selectbox("From Peg", ['A', 'B', 'C', 'D'][:st.session_state.peg_count])
            
            with col2:
                destination = st.selectbox("To Peg", ['A', 'B', 'C', 'D'][:st.session_state.peg_count])
            
            with col3:
                if st.button("Make Move"):
                    if source == destination:
                        st.error("Source and destination pegs cannot be the same!")
                    elif apply_move(st.session_state.game_state, source, destination):
                        st.session_state.move_count += 1
                        st.session_state.moves_made.append(f"{source}->{destination}")
                        st.session_state.move_sequence = ",".join(st.session_state.moves_made)
                        
                        # Check if the game is solved
                        check_game_solved()
                    else:
                        st.error("Invalid move! Remember, you cannot place a larger disk on a smaller one.")
            
            # Option to enter full move sequence
            st.subheader("Enter Full Solution")
            col1, col2 = st.columns(2)
            
            with col1:
                move_count = st.number_input("Number of Moves", min_value=1, value=len(st.session_state.optimal_moves))
            
            with col2:
                # Use the generated sequence as a default if available
                default_sequence = st.session_state.move_sequence if st.session_state.move_sequence else ""
                move_sequence = st.text_input("Move Sequence (e.g., A->B,B->C,A->C)", value=default_sequence)
            
            if st.button("Submit Solution"):
                moves = move_sequence.split(',')
                if len(moves) != move_count:
                    st.error(f"You specified {move_count} moves but provided {len(moves)} moves!")
                else:
                    # Reset game state and apply moves
                    test_state = init_game_state(st.session_state.disk_count)
                    valid_solution = True
                    
                    for move in moves:
                        if '->' not in move:
                            st.error(f"Invalid move format: {move}. Use 'Source->Destination' format.")
                            valid_solution = False
                            break
                        
                        source, destination = move.split('->')
                        if not apply_move(test_state, source, destination):
                            st.error(f"Invalid move: {move}. Check your solution.")
                            valid_solution = False
                            break
                    
                    if valid_solution:
                        if is_solved(test_state, st.session_state.disk_count):
                            st.balloons()
                            st.success("Your solution is correct!")
                            
                            # Compare with algorithms
                            compare_algorithms(player_name, st.session_state.disk_count, len(moves), move_sequence)
                            
                            # Reset game
                            st.session_state.game_active = False
                        else:
                            st.error("Your solution does not solve the puzzle!")
            
            # Get a hint
            if st.button("Get Hint"):
                if st.session_state.move_count < len(st.session_state.optimal_moves):
                    hint = st.session_state.optimal_moves[st.session_state.move_count]
                    st.info(f"Hint: Try moving from {hint.split('->')[0]} to {hint.split('->')[1]}")
                else:
                    st.info("You've already made more moves than the optimal solution!")
    
    elif menu == "Leaderboard":
        st.header("Leaderboard")
        leaderboard = get_leaderboard()
        st.dataframe(leaderboard)
    
    elif menu == "Algorithm Comparison":
        st.header("Algorithm Comparison")
        
        # Compare algorithms for different disk counts
        st.subheader("Comparison by Disk Count")
        
        disk_count = st.slider("Number of Disks", min_value=3, max_value=20, value=10)
        
        if st.button("Run Comparison"):
            st.write("Running comparison...")
            
            # 3 pegs
            recursive_moves, recursive_time = solve_hanoi_recursive(disk_count, 'A', 'B', 'C')
            iterative_moves, iterative_time = solve_hanoi_iterative(disk_count, 'A', 'B', 'C')
            
            # 4 pegs
            fs_moves, fs_time = solve_frame_stewart(disk_count, 'A', 'B', 'C', 'D')
            
            # Results
            data = {
                'Algorithm': ['Recursive (3 pegs)', 'Iterative (3 pegs)', 'Frame-Stewart (4 pegs)'],
                'Move Count': [len(recursive_moves), len(iterative_moves), len(fs_moves)],
                'Execution Time (s)': [recursive_time, iterative_time, fs_time]
            }
            
            df = pd.DataFrame(data)
            st.dataframe(df)
            
            # Visualization
            st.subheader("Move Count Comparison")
            st.bar_chart(df.set_index('Algorithm')['Move Count'])
            
            st.subheader("Execution Time Comparison")
            st.bar_chart(df.set_index('Algorithm')['Execution Time (s)'])

if __name__ == "__main__":
    main()