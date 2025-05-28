from fastmcp import FastMCP
import json

import threading
import pygame

SOUNDS = {
    "say_hello": "audio/say_hello.mp3",
    "say_rating_10": "audio/say_rating_10.mp3",
    "say_rating_7": "audio/say_rating_7.mp3",
    "say_rating_3": "audio/say_rating_3.mp3",
    "say_rating_1": "audio/say_rating_1.mp3",
    "say_goodbye": "audio/say_goodbye.mp3"
}

pygame.mixer.init()

def play_sound(file_path):
    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        # Detach playback — don't block thread. Let it finish on its own.
    except Exception as e:
        print(f"[ERROR] Failed to play sound: {e}")

# Create a new MCP server
app = FastMCP(
    title="GiggleBot Toy MCP",
    description="A joke evaluator toy that speaks based on structured commands.",
)

@app.tool()
def say_hello() -> str:
    """Say a friendly greeting"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_hello"],)).start()
    return "Hi there, I'm GiggleBot! Tell me a joke!"

@app.tool()
def say_rating_10() -> str:
    """Say a very positive joke rating (10/10)"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_rating_10"],)).start()
    return "That joke was hilarious! A perfect 10!"

@app.tool()
def say_rating_7() -> str:
    """Say a decent joke rating (7/10)"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_rating_7"],)).start()
    return "Nice one! I give that a 7 out of 10!"

@app.tool()
def say_rating_3() -> str:
    """Say a weak joke rating (3/10)"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_rating_3"],)).start()
    return "Hmm... I’ve heard better. That's a 3 out of 10."

@app.tool()
def say_rating_1() -> str:
    """Say a bad joke rating (1/10)"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_rating_1"],)).start()
    return "Yikes! That joke gets a 1."

@app.tool()
def say_goodbye() -> str:
    """Say goodbye"""
    threading.Thread(target=play_sound, args=(SOUNDS["say_goodbye"],)).start()
    return "Bye-bye! Come back with more jokes soon."

def load_action_list(path="actionlist.json"):
    """Load the Furby action list from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.tool()
def list_furby_actions() -> list:
    """List all available Furby actions and their descriptions/values."""
    return load_action_list()

if __name__ == "__main__":
    app.run()
else:
    pass
