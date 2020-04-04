import curses, typing, time, textwrap, math, datetime, sys

try:
    t = typing.Words(open("words.txt"))

    screen = curses.initscr()
    curses.start_color()
    curses.cbreak()
    screen.keypad(True)

    console_height, console_width = screen.getmaxyx()

    def centre_pos_x(text):
        return int((console_width / 2) - (len(text) / 2))

    def centre_pos_y(text):
        return int((console_height / 2) - (len(text.split('\n')) / 2))

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # Correctly typed text
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE) # Untyped text
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) # Incorrectly typed text
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE) # Cursor text


    message = "Welcome! Please press any key to continue"
    message2 = ""
    screen.addstr(1, centre_pos_x(message), message, curses.color_pair(1))
    screen.refresh()

    screen.getch()

    top_words = 100
    length = 10
    t.set_range(0, top_words)

    words = [t.next() for i in range(length)]
    screen.addstr(5, 1, str(words))
    screen.refresh()
    words_string = '\n'.join(textwrap.wrap(' '.join(words), console_width))

    cursor = 0
    user_input = ""

    def draw_words(words_list, user_input, std, start_time):
        std.clear()
        cursor_pos = len(user_input)

        correct_char = 0
        correct_word = 0

        for i in range(len(' '.join(words_list))):
            x = i % std.getmaxyx()[1]
            y = math.floor(i/std.getmaxyx()[1])

            if ' '.join(words_list)[i] != " ":
                if i < cursor_pos:
                    if user_input[i] == ' '.join(words_list)[i]:
                        std.addstr(y, x, ' '.join(words_list)[i], curses.color_pair(1))
                        correct_char += 1
                    else:
                        std.addstr(y, x, ' '.join(words_list)[i], curses.color_pair(3))
                if i == cursor_pos:
                    std.addstr(y, x, ' '.join(words_list)[i], curses.color_pair(4))
                if i > cursor_pos:
                    std.addstr(y, x, ' '.join(words_list)[i], curses.color_pair(2))
            else:
                try:
                    if i == cursor_pos:
                        std.addstr(y, x, ' '.join(words_list)[i], curses.color_pair(4))
                    if user_input[i] == ' '.join(words_list)[i]:
                        std.addstr(y, x, ' ')
                        correct_char += 1
                    else:
                        std.addstr(y, x, ' ', curses.color_pair(3))
                except:
                    pass
        std.refresh()
        # Find if they typed the entire word correct
        split_user_input = user_input.strip().split(' ')

        
        for f in range(len(split_user_input)):
            if split_user_input[f] == words_list[f]:
                correct_word += 1

        wpm = (correct_word / (datetime.datetime.now() - start_time).total_seconds())*60

        std.addstr(std.getmaxyx()[0]-1, 0, f">: {str(split_user_input[::-1][0])}")
        std.addstr(std.getmaxyx()[0]-1, int(std.getmaxyx()[1]/2), f"WPM: {round(wpm, 1)}")
        return {"char": correct_char, "words": correct_word}

    result = {}
    start_time = datetime.datetime.now()
    end_time = None
    while True:
        if len(user_input) < len(' '.join(words)):
            result = draw_words(words, user_input, screen, start_time)
        else:
            result = draw_words(words, user_input, screen, start_time)
            end_time = datetime.datetime.now()
            screen.clear()

            # Calculate score
            diff = (end_time - start_time)
            cpm = result["char"] / diff.total_seconds()
            wpm = result["words"] / diff.total_seconds()
            screen.addstr(1, 1, f"Time: {str((diff.seconds//60)%60).zfill(2)}:{str(diff.seconds).zfill(2)}.{str(round(diff.microseconds, 2)).zfill(2)}, CPM: {str(round(cpm*60, 1))}, WPM: {str(round(wpm*60, 1))}\n Words: {length}, Correct Words: {result['words']}, Length: {len(words_string)}, Correct chars: {result['char']}\n Accuracy: {round((result['char'] / len(words_string)) * 100, 1)}%\n\n [R]estart, [E]xit")

            screen.refresh()
            key = screen.getch()
            
            if key == ord('e') or key == ord('E'):
                break
            else:
                words = [t.next() for i in range(length)]
                words_string = '\n'.join(textwrap.wrap(' '.join(words), console_width))
                
                user_input = ""
                continue
            
        key = screen.getch()
        if len(user_input) == 0:
            start_time = datetime.datetime.now()
        if key == 263:
            user_input = user_input[:len(user_input)-1]
            user_input += ""
        else:
            user_input += chr(key)

except Exception as e:
    curses.endwin()
    print(e.with_traceback())

# Exit and return to the terminal