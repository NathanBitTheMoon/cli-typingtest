import curses, typing, time, textwrap, math, datetime, sys, argparse

def init_screen():
    screen = curses.initscr()
    curses.start_color()
    curses.cbreak()
    screen.keypad(True)

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE) # Correctly typed text
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE) # Untyped text
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_RED) # Incorrectly typed text
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE) # Cursor text

    return screen

def create_random_words(length, words, minimum_length):
    words.cursor = 0
    words = [words.next(shortest = minimum_length - 1) for i in range(length)]
    return words

def get_args(args):
    parser = argparse.ArgumentParser(description = "Start the typing test with different options")
    parser.add_argument("-rs", "--range-start", help = "Start of the range from the word list", default = 0, type = int)
    parser.add_argument("-re", "--range-end", help = "End of the range from the word list", default = 100, type = int)
    parser.add_argument("-l", "--length", help = "The length of the typing test in words", default = 100, type = int)
    parser.add_argument("-tf", "--text-file", help = "The text file that will be used", default = "texts/words.txt", type = str)
    parser.add_argument("-dr", "--disable-random", help = "Don't randomise the list of words", default = "no", type = str)
    parser.add_argument("-sw", "--shortest-word", help = "The shortest a word can be", default = 3, type = int)
    parser.add_argument("-sc", "--split-char", help = "Where the words will be split in the text", default = "\n", type = str)
    parser.add_argument("-rp", "--remove-punctuation", help = "The shortest a word can be", default = True, type = bool)

    args = parser.parse_args(args)
    return_value = {
        "range_start": args.range_start,
        "range_end": args.range_end,
        "length": args.length,
        "text_file": args.text_file,
        "disable_random": args.disable_random,
        "minimum_length": args.shortest_word,
        "split_char": args.split_char
    }

    return return_value

def welcome_message(args):
    message = "Welcome! Please press any key to continue"
    screen.addstr(1, centre_pos_x(message), message, curses.color_pair(1))
    screen.addstr(0, 0, f'File: {args["text_file"]}')

    info = f"Length: {args['length']}, File: {args['text_file']}{', Random' if not args['disable_random'] else ''}"
    screen.addstr(2, centre_pos_x(info), info)
    screen.refresh()

    screen.getch()

def draw_words(words_list, user_input, std, start_time, args):
    std.clear()
    cursor_pos = len(user_input)

    correct_char = 0
    correct_word = 0

    f = open("debug.log", "w")
    f.close()

    for i in range(len(' '.join(words_list))):
        x = i % std.getmaxyx()[1]
        y = math.floor(i/std.getmaxyx()[1])
        f = open("debug.log", "a")
        f.write(f"X: {x}, Y: {y}, S: {' '.join(words_list)[i]}, I: {i}\n")
        f.close()

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

try:
    # Init screen and some functions for text
    screen = init_screen()

    console_height, console_width = screen.getmaxyx()

    def centre_pos_x(text):
        return int((console_width / 2) - (len(text) / 2))

    def centre_pos_y(text):
        return int((console_height / 2) - (len(text.split('\n')) / 2))

    # Pass command line functions
    command_line_arguments = get_args(sys.argv[1:])

    length = command_line_arguments["length"]

    # Create words list
    t = typing.Words(open(
        command_line_arguments["text_file"],
    ), split_char = command_line_arguments["split_char"])
    t.set_range(
        command_line_arguments["range_start"],
        command_line_arguments["range_end"]
    )

    if (command_line_arguments["disable_random"] == "no"):
        t.random()

    welcome_message(command_line_arguments)

    words = create_random_words(command_line_arguments["length"], t, command_line_arguments["minimum_length"])

    cursor = 0
    user_input = ""

    result = {}
    start_time = datetime.datetime.now()
    end_time = None
    while True:
        if len(user_input) < len(' '.join(words)):
            result = draw_words(words, user_input, screen, start_time, command_line_arguments)
        else:
            result = draw_words(words, user_input, screen, start_time, command_line_arguments)
            end_time = datetime.datetime.now()
            screen.clear()

            # Calculate score
            diff = (end_time - start_time)
            cpm = result["char"] / diff.total_seconds()
            wpm = result["words"] / diff.total_seconds()
            filename = command_line_arguments["text_file"].split('.')
            filename = '.'.join(filename[::-1][1:][::-1])
            screen.addstr(1, centre_pos_x("Results"), "Results", curses.color_pair(4))
            screen.addstr(2, 1, f"Text: {filename}")
            screen.addstr(3, 1, f"Time: {str((diff.seconds//60)%60).zfill(2)}:{str(diff.seconds).zfill(2)}.{str(round(diff.microseconds, 2)).zfill(2)}, CPM: {str(round(cpm*60, 1))}, WPM: {str(round(wpm*60, 1))}\n Words: {len(words)}\n\n [E]xit [R]estart")

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
        if key == 27:
            break

except KeyboardInterrupt:
    curses.endwin()
except Exception as e:
    curses.endwin()
    print(e.with_traceback())
finally:
    curses.endwin()
# Exit and return to the terminal