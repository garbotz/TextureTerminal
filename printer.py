#!/usr/bin/python

import random, sys, struct, termios, fcntl, os, time

c0 = 	['a', 'b', 'c', 'd', 'f', 'g', 'i', 'j', 'l', 'm', 'o', 'p', 'q', 'r', 't', 'v', 'w', 'x', '.']
c1 = 	['\\', '/'] # slants
c2 = 	['<', '>', 'v', '^'] # directional
c3 = 	['f', 'x', 'J', 'l', 'l', 'l', 'L', 'u'] # the jungle
c4 = 	['N', 'M', 'D', 'A', 'A', 'n', 't', 'T', 'k', 'a', 'z', 'Z', 'X', 'x', 'u', '_', '_', '_', '_'] # the city
c5 = 	['[', ']', '|', '-', '{', '}', '#', '(', ')', ',']
c6 = 	[']', '[', '+', '-']
c7 = 	[',', '.', '.', '.', '.']
c8 = 	['}', '{', ':', '.', ')', '(', '[', ']']
c9 = 	['.', ',', '\'', 'l', ':', ';', '~', '`', '*', '-', '+', '$', ']', '\\', '/']
c10 = 	['_', '-', '|']
c11 = 	['_', '-']
c12 = 	['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
c13 = 	['!', '@', '#', '$', '%', '^', '&', '*']
c14 = 	['!', '|', 'l', 'I', '1']
c15 =	['0', 'O', 'o', 'c', 'u', '@']
c16 = 	['~', '`', '-', '=', '+']

# chars = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16]
# chars = [c16, c14, c7, c10, c1]

chars = [c0, c12, c11]

currentcolor = '\033[30m\033[47m'
previouscolor = '\033[37m\033[40m'
# currentcolor = '\033[31m'
# previouscolor = '\033[34m'
# currentcolor = '\033[37m'
# previouscolor = '\033[34m'

phrase = ""
previous_set = chars[0]
current_set = chars[1]
transitioning = False
line_counts = 50
line_count = line_counts
transition_length = 300
transition_iter = transition_length
blank_chance = 0.3

def loop():
	while True:
		add_line()

def add_line():
	global phrase, chars, line_count, line_counts, current_set, previous_set
	global transitioning, transition_iter, transition_length, previouscolor
	global currentcolor, blank_chance

	time.sleep(0.0001);
	# Reset phrase
	phrase = ""

	# Get console width and height
	lines, cols = struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))

	if transitioning:
		x = 0
		while x < cols:
			if random.random() < blank_chance:
				phrase += " "
			elif random.random() < translate(transition_iter, 0, transition_length, 0, 1):
				phrase += "{}{}".format(previouscolor, random.choice(previous_set))
			else:
				phrase += "{}{}".format(currentcolor, random.choice(current_set))
			x += 1
		if transition_iter <= 0:
			transition_iter = transition_length
			transitioning = False
		else:
			transition_iter -= 1
	else:
		x = 0
		while x < cols:
			if random.random() < blank_chance:
				phrase += " "
			else:
				phrase += "{}{}".format(currentcolor, random.choice(current_set))
			x += 1
		if line_count <= 0:
			line_count = line_counts
			previous_set = current_set
			current_set = random.choice(chars)
			tmp = previouscolor
			previouscolor = currentcolor
			currentcolor = tmp
			transitioning = True
		else:
			line_count -= 1

	# Print phrase
	print('{}'.format(phrase))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

loop()