# plugins/quick_notes.py

PLUGIN_ID = "quick_notes"
PLUGIN_NAME = "Quick Notes"
PLUGIN_DESC = "Write and save short notes"

def run(stdscr):
    import curses

    curses.echo()
    stdscr.clear()
    stdscr.addstr(0, 0, "📝 Enter your note:")
    note = stdscr.getstr(2, 0, 100).decode("utf-8").strip()
    curses.noecho()

    if note:
        with open("notes.txt", "a") as f:
            f.write(note + "\n")
        stdscr.addstr(4, 0, "✅ Note saved to notes.txt")
    else:
        stdscr.addstr(4, 0, "⚠️ No note entered.")
    stdscr.addstr(6, 0, "Press any key to return.")
    stdscr.refresh()
    stdscr.getch()
