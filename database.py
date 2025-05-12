import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize Firebase
@st.cache_resource
def init_firestore():
     firebase_config = dict(st.secrets["firebase"])
     cred = credentials.Certificate(firebase_config)
    
     if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
     return firestore.client()

db = init_firestore()

def save_user_game(player_name, disk_count, moves_count, move_sequence):
    doc_ref = db.collection("user_games").document()
    doc_ref.set({
        "player_name": player_name,
        "disk_count": disk_count,
        "moves_count": moves_count,
        "move_sequence": move_sequence,
        "timestamp": datetime.now()
    })

def save_algorithm_performance(algorithm, disk_count, execution_time, moves_count, parameters=None, notes=None):
    doc_ref = db.collection("algorithm_performance").document()
    doc_ref.set({
        "algorithm": algorithm,
        "disk_count": disk_count,
        "execution_time": execution_time,
        "moves_count": moves_count,
        "timestamp": datetime.now(),
        "parameters": parameters,
        "notes": notes
    })

def get_user_leaderboard():
    results = db.collection("user_games").order_by("moves_count").order_by("timestamp").limit(10).stream()
    leaderboard = [{
        "player_name": doc.to_dict()["player_name"],
        "disk_count": doc.to_dict()["disk_count"],
        "moves_count": doc.to_dict()["moves_count"],
        "timestamp": doc.to_dict()["timestamp"]
    } for doc in results]
    return pd.DataFrame(leaderboard)

def get_algorithm_benchmarks():
    results = db.collection("algorithm_performance").order_by("disk_count").order_by("execution_time").stream()
    benchmarks = [{
        "algorithm": doc.to_dict()["algorithm"],
        "disk_count": doc.to_dict()["disk_count"],
        "execution_time": doc.to_dict()["execution_time"],
        "moves_count": doc.to_dict()["moves_count"],
        "timestamp": doc.to_dict()["timestamp"],
        "parameters": doc.to_dict().get("parameters"),
        "notes": doc.to_dict().get("notes")
    } for doc in results]
    return pd.DataFrame(benchmarks)
