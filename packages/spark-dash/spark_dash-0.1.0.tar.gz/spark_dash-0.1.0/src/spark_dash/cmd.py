import os


def run():
    os.system(f"streamlit run {os.path.dirname(os.path.abspath(__file__))}/main.py")