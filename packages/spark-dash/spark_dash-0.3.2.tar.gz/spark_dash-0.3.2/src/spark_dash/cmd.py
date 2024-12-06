import os


def run():
    os.system(f"docker compose -f {os.path.dirname(os.path.abspath(__file__))}/conf/docker-compose.yml up -d")
    os.system(f"streamlit run {os.path.dirname(os.path.abspath(__file__))}/main.py")