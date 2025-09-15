import curses
import random
from curses import wrapper
from curses.textpad import rectangle

def main(stdscr):
    def play_game():
        SCREEN_Y, SCREEN_X = stdscr.getmaxyx()
        curses.curs_set(0)

        top, left = 1, 1
        bottom, right = SCREEN_Y - 3, SCREEN_X - 3

        # Initial apple location
        apple_y = SCREEN_Y // 2
        apple_x = SCREEN_X // 2 + 5

        # Snake setup
        facing = "east"
        snake = [(SCREEN_Y // 2, SCREEN_X // 2)]
        size = 1

        def generate_apple():
            nonlocal apple_y, apple_x
            while True:
                apple_y = random.randint(top + 1, bottom - 1)
                apple_x = random.randint(left + 1, right - 1)
                if (apple_y, apple_x) not in snake:
                    break

        while True:
            stdscr.clear()

            # Set tick based on direction (horizontal faster)
            tick = 50 if facing in ["east", "west"] else 100
            stdscr.timeout(tick)

            # Draw play area
            rectangle(stdscr, top, left, bottom, right)

            # Draw apple
            stdscr.addstr(apple_y, apple_x, "O")

            # Draw snake
            for idx, (sy, sx) in enumerate(snake):
                char = "@" if idx == 0 else "#"
                stdscr.addstr(sy, sx, char)

            # Display score
            stdscr.addstr(SCREEN_Y - 2, SCREEN_X // 2 - 20, f"Size: {size}")

            # Show quit hint
            stdscr.addstr(0, 2, "Press 'q' to quit")

            # Handle input
            key = stdscr.getch()
            if key == ord("q"):
                return False
            elif key == curses.KEY_LEFT and facing != "east":
                facing = "west"
            elif key == curses.KEY_RIGHT and facing != "west":
                facing = "east"
            elif key == curses.KEY_UP and facing != "south":
                facing = "north"
            elif key == curses.KEY_DOWN and facing != "north":
                facing = "south"

            # Current head
            head_y, head_x = snake[0]

            # Move head
            if facing == "north":
                head = (head_y - 1, head_x)
            elif facing == "south":
                head = (head_y + 1, head_x)
            elif facing == "west":
                head = (head_y, head_x - 1)
            elif facing == "east":
                head = (head_y, head_x + 1)

            # Check collisions
            if (head[0] <= top or head[0] >= bottom or
                head[1] <= left or head[1] >= right or
                head in snake):
                break  # Game over

            # Move snake
            snake.insert(0, head)

            # Check apple
            if head[0] == apple_y and head[1] == apple_x:
                size += 1
                generate_apple()  # grow
            else:
                snake.pop()  # remove tail

            stdscr.refresh()

        # Game Over Screen
        stdscr.clear()
        msg1 = "GAME OVER!"
        msg2 = f"Final Size: {size}"
        msg3 = "Press 'r' to restart or 'q' to quit"
        stdscr.addstr(SCREEN_Y // 2 - 1, SCREEN_X // 2 - len(msg1)//2, msg1)
        stdscr.addstr(SCREEN_Y // 2, SCREEN_X // 2 - len(msg2)//2, msg2)
        stdscr.addstr(SCREEN_Y // 2 + 1, SCREEN_X // 2 - len(msg3)//2, msg3)
        stdscr.refresh()

        # Wait for input
        while True:
            key = stdscr.getch()
            if key == ord("r"):
                return True
            elif key == ord("q"):
                return False

    # Main loop to allow restart
    while True:
        restart = play_game()
        if not restart:
            break

wrapper(main)
