import that

# the 'to be interpreted' file's path is either the input one or the default one
default_path = r'C:\Users\Stas\Desktop\test.bf'
input_path = input('Which file do you want me to interpret (press Enter to use the default path): ')
if input_path:
    file_path = input_path
else:
    file_path = default_path
# whether to print numbers or unicode symbols
symbols_mode = False
# creating the memory list and giving it some space
memory = []
current_index = 0
for _ in range(30000):
    memory.append(0)
# valid symbols
symbols = '<>.,[]+-'
# uniting all the strings in one
script = [s.strip() for s in open(file_path, 'r').readlines()]
script = ''.join(script)


def find_the_end_of_the_cycle_index(code, start_index):
    """Returns the index of cycle's end"""
    # counting the number of  enclosed cycles
    enclosed = 0
    for i in range(start_index + 1, len(code)):
        # the cycle starts
        if code[i] == '[':
            enclosed += 1
        # when there are no enclosed cycles
        if code[i] == ']' and enclosed == 0:
            return i
        # some cycle ends
        elif code[i] == ']' and enclosed != 0:
            enclosed -= 1


def interpret(code):
    """Interprets brainfuck code"""
    # including global variables
    global current_index
    global memory
    i = 0
    # going through each symbol of the brainfuck script (parsing)
    # (we use while instead of for because when the cycle is being recursively interpreted
    # parsing continues from the the exact same place and interprets it one extra time)
    while i < len(code):
        # checking if code is valid and doesn't have any unexpected symbols
        if code[i] not in symbols:
            raise ValueError
        # goes to the next cell
        elif code[i] == '>':
            current_index += 1
            current_index %= 30000
        # goes to the previous cell
        elif code[i] == '<':
            current_index -= 1
            if current_index == -1:
                current_index = 29999
        # increases value of a current cell by one
        elif code[i] == '+':
            memory[current_index] += 1
        # decreases value of a current cell by one
        elif code[i] == '-':
            memory[current_index] -= 1
            if memory[current_index] < 0:
                memory[current_index] = 0
        # prints the unicode symbol numbered by current cell's value
        # or exactly the number
        elif code[i] == '.':
            if symbols_mode:
                print(chr(memory[current_index]), end='')
            else:
                print(memory[current_index])
        # puts the input value to the current cell or the unicode number of
        # the input symbol if it's in symbol mode (empty input equals 0)
        elif code[i] == ',':
            if symbols_mode:
                inputs = input()
                memory[current_index] = ord(inputs[0]) if inputs else 0
            memory[current_index] = int(input())
        # parses the code inside [] while current cell's value isn't 0
        elif code[i] == '[':
            while memory[current_index]:
                interpret(code[i + 1:find_the_end_of_the_cycle_index(code, i)])
            i += find_the_end_of_the_cycle_index(code, i) - i
        # we don't actually need to do something with this particular symbol as we have already reached
        # the end of the cycle (check find_the_end_of_the_cycle_index function)
        elif code[i] == ']':
            continue
        i += 1


# let's run the code
interpret(script)

# resetting all the parameters
current_index = 0
for k in range(30000):
    memory[k] = 0
    
