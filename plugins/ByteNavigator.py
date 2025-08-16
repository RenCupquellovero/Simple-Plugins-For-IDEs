import curses
import os


# Plugin Metadata
PLUGIN_ID = "ByteNavigator"
PLUGIN_NAME = "ByteNavigator"
PLUGIN_DESC = "A curses-based file explorer with clipboard and navigation history"




clipboard = {"path": None, "mode": None}  # mode = "copy" or "cut"

def list_dir(path):
    try:
        return sorted(os.listdir(path))
    except Exception:
        return ["<error reading directory>"]

def draw_ui(stdscr, path, files, selected_index):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(0, 0, f"ByteNavigator — {path}")
    for i, file in enumerate(files):
        prefix = "→ " if i == selected_index else "  "
        line = f"{prefix}{file}"
        if i + 2 < h - 3:
            stdscr.addstr(i + 2, 2, line[:w-4])

    # Keybind legend
    legend = "[↑↓] Navigate  [Enter] Open  [←] Back  [c] Copy  [x] Cut  [v] Paste  [d] Delete  [q] Quit"
    stdscr.addstr(h - 2, 0, legend[:w-1])
    stdscr.refresh()

def run(stdscr):
    current_path = os.getcwd()
    selected_index = 0
    history = []

    curses.curs_set(0)

    while True:
        files = list_dir(current_path)
        draw_ui(stdscr, current_path, files, selected_index)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN:
            selected_index = min(len(files) - 1, selected_index + 1)
        elif key == curses.KEY_LEFT:
            if history:
                current_path = history.pop()
                selected_index = 0
        elif key == ord('q'):
            break
        elif key == 10:  # Enter
            selected_file = files[selected_index]
            new_path = os.path.join(current_path, selected_file)
            if os.path.isdir(new_path):
                history.append(current_path)
                current_path = new_path
                selected_index = 0
        elif key == ord('c'):
            clipboard["path"] = os.path.join(current_path, files[selected_index])
            clipboard["mode"] = "copy"
        elif key == ord('x'):
            clipboard["path"] = os.path.join(current_path, files[selected_index])
            clipboard["mode"] = "cut"
        elif key == ord('v') and clipboard["path"]:
            src = clipboard["path"]
            dst = os.path.join(current_path, os.path.basename(src))
            try:
                if os.path.isdir(src):
                    os.system(f"cp -r '{src}' '{dst}'") if clipboard["mode"] == "copy" else os.system(f"mv '{src}' '{dst}'")
                else:
                    os.system(f"cp '{src}' '{dst}'") if clipboard["mode"] == "copy" else os.system(f"mv '{src}' '{dst}'")
                clipboard["path"] = None
                clipboard["mode"] = None
            except Exception:
                pass
        elif key == ord('d'):
            target = os.path.join(current_path, files[selected_index])
            try:
                if os.path.isdir(target):
                    os.system(f"rm -r '{target}'")
                else:
                    os.system(f"rm '{target}'")
            except Exception:
                pass
