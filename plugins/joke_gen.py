# plugins/joke_gen.py

PLUGIN_ID = "joke_gen"
PLUGIN_NAME = "Joke Generator"
PLUGIN_DESC = "Get a random joke to lighten your day"

def run(stdscr):
    import curses
    import random

    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "I told my computer I needed a break... it crashed.",
        "Why do Java developers wear glasses? Because they don't C#."
    ]

    curses.curs_set(0)
    stdscr.clear()
    stdscr.addstr(0, 0, "😂 Joke Generator", curses.A_BOLD)
    stdscr.addstr(2, 0, random.choice(jokes))
    stdscr.addstr(4, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
