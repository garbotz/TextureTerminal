#!/usr/bin/python

import random, sys, struct, termios, fcntl, os

c0 = ['a','b','c','d','f','g','i','j','l','m','o','p','q','r','t','v','w','x',' ','.']
c1 = [' ','\\','/',' ']
c2 = ['\\','/']
c3 = ['<','>','v','^']
c4 = ['f','x','J','l','l','l','L','u'] # the jungle
c5 = ['N','M','D','A','A','n','t','T','k','a','z','Z','X','x','u','_','_','_','_'] # the city
c6 = ['[',']','|','-','{','}','#','(',')',' ',',']
c7 = [']','[',' ','+','-']
c8 = [',','.',' ','.','.','.',' ',' ',' ',' ',' ',' ',' ',' ',' ']
c9 = ['}','{',':','.',')','(','[',']']
c10 = [' ', '.', ',', '\'', 'l', ':', ';', '~', '`', '*', '-', '+', '$', ']', '\\', '/']
c11 = ['_','-','|']
c12 = ['_',' ', '-']
c13 = ['0','1','2','3','4','5','6','7','8','9']
c14 = ['i ', 'me ', 'you ','us ', 'them ']
c15 = ['a8',' ', 'b4',' ','n3',' ', 'o2', ' ', 'p7', ' ']

chars = [c0, c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13]
# chars = [c1, c2, c3, c6, c7, c8, c9, c10, c11, c12]

currentcolor = '\033[36m'
previouscolor = '\033[36m'

phrase = ""
previous_set = chars[0]
current_set = chars[1]
transitioning = False
line_counts = 100
line_count = line_counts
transition_length = 100
transition_iter = transition_length
blank_chance = 0.9
# raw_input()

def loop():
	while True:
		add_line()

def add_line():
	global phrase, chars, line_count, line_counts, current_set, previous_set
	global transitioning, transition_iter, transition_length, previouscolor
	global currentcolor, blank_chance

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