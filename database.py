import pymysql
import pandas as pd
from datetime import datetime

# Initialize the database
def init_db():
    conn = pymysql.connect(
        host='localhost',
        user='root',  # default WAMP MySQL username
        password='',  # default WAMP MySQL password is empty
        charset='utf8mb4'
    )
    c = conn.cursor()
    
    # Create the database if it doesn't exist
    c.execute('CREATE DATABASE IF NOT EXISTS tower_of_hanoi')
    c.execute('USE tower_of_hanoi')
    
    # Create the table
    c.execute('''
    CREATE TABLE IF NOT EXISTS game_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        player_name VARCHAR(255),
        disk_count INT,
        moves_count INT,
        move_sequence TEXT,
        algorithm VARCHAR(255),
        execution_time FLOAT,
        timestamp DATETIME
    )
    ''')
    conn.commit()
    conn.close()

# Save game results to the database
def save_result(player_name, disk_count, moves_count, move_sequence, algorithm, execution_time):
    conn = pymysql.connect(
        host='localhost',
        user='root',  # default WAMP MySQL username
        password='',  # default WAMP MySQL password is empty
        database='tower_of_hanoi',
        charset='utf8mb4'
    )
    c = conn.cursor()
    c.execute('''
    INSERT INTO game_results (player_name, disk_count, moves_count, move_sequence, algorithm, execution_time, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ''', (player_name, disk_count, moves_count, move_sequence, algorithm, execution_time, datetime.now()))
    conn.commit()
    conn.close()

# Get leaderboard data
def get_leaderboard():
    conn = pymysql.connect(
        host='localhost',
        user='root',  # default WAMP MySQL username
        password='',  # default WAMP MySQL password is empty
        database='tower_of_hanoi',
        charset='utf8mb4'
    )
    query = '''
    SELECT player_name, disk_count, moves_count, algorithm, execution_time 
    FROM game_results 
    ORDER BY execution_time ASC
    LIMIT 10
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df