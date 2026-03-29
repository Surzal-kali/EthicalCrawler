import time
def pspace(message, char_delay=0.03, line_delay=0.5):
        print("\n")
        for char in message:
            print(char, end='', flush=True)
            time.sleep(char_delay)
            time.sleep(line_delay)
        print("\n")
def pprint(message, char_delay=0.03, line_delay=0.5):
    print ("\n")
    for char in message:
        print(char, end='', flush=True)
        time.sleep(char_delay)
    time.sleep(line_delay)
    print ("\n")