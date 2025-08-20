from src.core.auth import login, logout
from src.utils.main_graph import draw_graph

def run():
    user = login("test_user", "password")
    draw_graph(user)
    logout(user)