# plugins/system_pulse.py

PLUGIN_ID = "system_pulse"
PLUGIN_NAME = "System Pulse"
PLUGIN_DESC = "Monitor CPU, RAM, and disk usage"

def run(stdscr):
    import curses
    import psutil
    import time

    curses.curs_set(0)
    stdscr.nodelay(True)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "🧠 System Pulse Monitor", curses.A_BOLD)

        # CPU
        cpu = psutil.cpu_percent(interval=0.1)
        stdscr.addstr(2, 0, f"⚙️ CPU Usage: {cpu:.1f}%")

        # RAM
        mem = psutil.virtual_memory()
        stdscr.addstr(3, 0, f"🧵 RAM Usage: {mem.percent:.1f}% ({mem.used // (1024**2)}MB / {mem.total // (1024**2)}MB)")

        # Disk
        disk = psutil.disk_usage('/')
        stdscr.addstr(4, 0, f"💾 Disk Usage: {disk.percent:.1f}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")

        stdscr.addstr(6, 0, "Press Q to quit.")
        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            break
        time.sleep(0.5)
