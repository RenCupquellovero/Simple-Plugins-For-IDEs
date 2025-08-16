import curses
import subprocess

COMMAND_HISTORY = []
SUGGESTIONS = []

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"

def update_suggestions(prefix):
    return [cmd for cmd in COMMAND_HISTORY if cmd.startswith(prefix)]

def main(stdscr):
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)  # Theme 1
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)  # Theme 2

    theme = 1
    max_y, max_x = stdscr.getmaxyx()
    input_win = curses.newwin(1, max_x, max_y - 1, 0)
    output_win = curses.newwin(max_y - 2, max_x, 0, 0)
    suggestion_win = curses.newwin(1, max_x, max_y - 2, 0)

    cmd = ""
    output_lines = []

    while True:
        stdscr.clear()
        output_win.clear()
        suggestion_win.clear()
        input_win.clear()

        # Display output
        for i, line in enumerate(output_lines[-(max_y - 2):]):
            output_win.addstr(i, 0, line[:max_x - 1])

        # Display suggestions
        SUGGESTIONS = update_suggestions(cmd)
        if SUGGESTIONS:
            suggestion_win.addstr(0, 0, "Suggestions: " + ", ".join(SUGGESTIONS[:3]), curses.color_pair(theme))

        # Display input
        input_win.addstr(0, 0, f">> {cmd}", curses.color_pair(theme))

        stdscr.refresh()
        output_win.refresh()
        suggestion_win.refresh()
        input_win.refresh()

        key = stdscr.getch()

        if key in (curses.KEY_ENTER, 10, 13):
            if cmd == "exit":
                break
            elif cmd.startswith("theme "):
                theme = 2 if cmd.split(" ")[1] == "dark" else 1
                output_lines.append(f"Switched to theme: {cmd.split(' ')[1]}")
            else:
                COMMAND_HISTORY.append(cmd)
                result = run_command(cmd)
                output_lines.extend(result.splitlines())
            cmd = ""
        elif key == curses.KEY_BACKSPACE or key == 127:
            cmd = cmd[:-1]
        elif key == curses.KEY_RESIZE:
            max_y, max_x = stdscr.getmaxyx()
            input_win.resize(1, max_x)
            output_win.resize(max_y - 2, max_x)
            suggestion_win.resize(1, max_x)
        else:
            cmd += chr(key)

if __name__ == "__main__":
    curses.wrapper(main)
