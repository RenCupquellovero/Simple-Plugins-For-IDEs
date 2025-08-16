# plugins/terminal_snake.py

PLUGIN_ID = "terminal_snake"
PLUGIN_NAME = "Terminal Snake"
PLUGIN_DESC = "Classic snake game in the terminal"

def run(stdscr):
    import curses
    import random
    import time

    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]

    snake = [[sh//2, sw//2 + i] for i in range(3)]
    direction = curses.KEY_LEFT
    score = 0

    food = [random.randint(box[0][0]+1, box[1][0]-1),
            random.randint(box[0][1]+1, box[1][1]-1)]

    while True:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(1, 2, f"🐍 Terminal Snake | Score: {score}")
        stdscr.addstr(2, 2, "Press Q to quit")

        # Draw food
        stdscr.addch(food[0], food[1], "🍎")

        # Draw snake
        for y, x in snake:
            stdscr.addch(y, x, "█")

        stdscr.refresh()

        key = stdscr.getch()
        if key in [ord('q'), ord('Q')]:
            break
        elif key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 1]
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 1]

        # Collision with wall
        if (new_head[0] in [box[0][0], box[1][0]] or
            new_head[1] in [box[0][1], box[1][1]] or
            new_head in snake):
            stdscr.nodelay(False)
            stdscr.clear()
            stdscr.addstr(sh//2, sw//2 - 5, f"💀 Game Over! Score: {score}")
            stdscr.addstr(sh//2 + 2, sw//2 - 10, "Press any key to return")
            stdscr.refresh()
            stdscr.getch()
            break

        snake.insert(0, new_head)

        # Eat food
        if new_head == food:
            score += 1
            food = [random.randint(box[0][0]+1, box[1][0]-1),
                    random.randint(box[0][1]+1, box[1][1]-1)]
        else:
            snake.pop()

    # Cleanup
    stdscr.nodelay(False)
    curses.curs_set(1)
    stdscr.clear()
    stdscr.refresh()
