#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import argparse
import reedsolo
reedsolo.init_tables(0x11d)

# Alignment pattern locations
alignment_pattern_array = [
[],
[6, 18],
[6, 22],
[6, 26],
[6, 30],
[6, 34],
[6, 22, 38],
[6, 24, 42],
[6, 26, 46],
[6, 28, 50],
[6, 30, 54],
[6, 32, 58],
[6, 34, 62],
[6, 26, 46, 66],
[6, 26, 48, 70],
[6, 26, 50, 74],
[6, 30, 54, 78],
[6, 30, 56, 82],
[6, 30, 58, 86],
[6, 34, 62, 90],
[6, 28, 50, 72, 94],
[6, 26, 50, 74, 98],
[6, 30, 54, 78, 102],
[6, 28, 54, 80, 106],
[6, 32, 58, 84, 110],
[6, 30, 58, 86, 114],
[6, 34, 62, 90, 118],
[6, 26, 50, 74, 98, 122],
[6, 30, 54, 78, 102, 126],
[6, 26, 52, 78, 104, 130],
[6, 30, 56, 82, 108, 134],
[6, 34, 60, 86, 112, 138],
[6, 30, 58, 86, 114, 142],
[6, 34, 62, 90, 118, 146],
[6, 30, 54, 78, 102, 126, 150],
[6, 24, 50, 76, 102, 128, 154],
[6, 28, 54, 80, 106, 132, 158],
[6, 32, 58, 84, 110, 136, 162],
[6, 26, 54, 82, 110, 138, 166],
[6, 30, 58, 86, 114, 142, 170]
]

# Version information table (version 7 and up)
version_information_table = [
0x07C94,
0x085BC,
0x09A99,
0x0A4D3,
0x0BBF6,
0x0C762,
0x0D847,
0x0E60D,
0x0F928,
0x10B78,
0x1145D,
0x12A17,
0x13532,
0x149A6,
0x15683,
0x168C9,
0x177EC,
0x18EC4,
0x191E1,
0x1AFAB,
0x1B08E,
0x1CC1A,
0x1D33F,
0x1ED75,
0x1F250,
0x209D5,
0x216F0,
0x228BA,
0x2379F,
0x24B0B,
0x2542E,
0x26A64,
0x27541,
0x28C69
]

# Format information table
format_information_table = [
'000000000000000',
'000010100110111',
'000101001101110',
'000111101011001',
'001000111101011',
'001010011011100',
'001101110000101',
'001111010110010',
'010001111010110',
'010011011100001',
'010100110111000',
'010110010001111',
'011001000111101',
'011011100001010',
'011100001010011',
'011110101100100',
'100001010011011',
'100011110101100',
'100100011110101',
'100110111000010',
'101001101110000',
'101011001000111',
'101100100011110',
'101110000101001',
'110000101001101',
'110010001111010',
'110101100100011',
'110111000010100',
'111000010100110',
'111010110010001',
'111101011001000',
'111111111111111'
]

# Data codeword table (M(00), L(01), H(10), Q(11))
data_code_num_table = [
[  16,   19,    9,   13],
[  28,   34,   16,   22],
[  44,   55,   26,   34],
[  64,   80,   36,   48],
[  86,  108,   46,   62],
[ 108,  136,   60,   76],
[ 124,  156,   66,   88],
[ 154,  194,   86,  110],
[ 182,  232,  100,  132],
[ 216,  274,  122,  154],
[ 254,  324,  140,  180],
[ 290,  370,  158,  206],
[ 334,  428,  180,  244],
[ 365,  461,  197,  261],
[ 415,  523,  223,  295],
[ 453,  589,  253,  325],
[ 507,  647,  283,  367],
[ 563,  721,  313,  397],
[ 627,  795,  341,  445],
[ 669,  861,  385,  485],
[ 714,  932,  406,  512],
[ 782, 1006,  442,  568],
[ 860, 1094,  464,  614],
[ 914, 1174,  514,  664],
[1000, 1276,  538,  718],
[1062, 1370,  596,  754],
[1128, 1468,  628,  808],
[1193, 1531,  661,  871],
[1267, 1631,  701,  911],
[1373, 1735,  745,  985],
[1455, 1843,  793, 1033],
[1541, 1955,  845, 1115],
[1631, 2071,  901, 1171],
[1725, 2191,  961, 1231],
[1812, 2306,  986, 1286],
[1914, 2434, 1054, 1354],
[1992, 2566, 1096, 1426],
[2102, 2702, 1142, 1502],
[2216, 2812, 1222, 1582],
[2334, 2956, 1276, 1666]
]

# RS block count table (M(00), L(01), H(10), Q(11))
RS_block_num_table = [
[1, 1, 1, 1],
[1, 1, 1, 1],
[1, 1, 2, 2],
[2, 1, 4, 2],
[2, 1, 4, 4],
[4, 2, 4, 4],
[4, 2, 5, 6],
[4, 2, 6, 6],
[5, 2, 8, 8],
[5, 4, 8, 8],
[5, 4, 11, 8],
[8, 4, 11, 10],
[9, 4, 16, 12],
[9, 4, 16, 16],
[10, 6, 18, 12],
[10, 6, 16, 17],
[11, 6, 19, 16],
[13, 6, 21, 18],
[14, 7, 25, 21],
[16, 8, 25, 20],
[17, 8, 25, 23],
[17, 9, 34, 23],
[18, 9, 30, 25],
[20, 10, 32, 27],
[21, 12, 35, 29],
[23, 12, 37, 34],
[25, 12, 40, 34],
[26, 13, 42, 35],
[28, 14, 45, 38],
[29, 15, 48, 40],
[31, 16, 51, 43],
[33, 17, 54, 45],
[35, 18, 57, 48],
[37, 19, 60, 51],
[38, 19, 63, 53],
[40, 20, 66, 56],
[43, 21, 70, 59],
[45, 22, 74, 62],
[47, 24, 77, 65],
[49, 25, 81, 68]
]

# Alphanumeric mode table
alphanumeric_table = [
'0', '1', '2', '3', '4', '5',
'6', '7', '8', '9', 'A', 'B',
'C', 'D', 'E', 'F', 'G', 'H',
'I', 'J', 'K', 'L', 'M', 'N',
'O', 'P', 'Q', 'R', 'S', 'T',
'U', 'V', 'W', 'X', 'Y', 'Z',
' ', '$', '%', '*', '+', '-',
'.', '/', ':']

# Colorized text output
def stdoutColor(text, color):
	dic = {'red': 31, 'green': 32, 'blue': 34}
	sys.stdout.write('\x1b[1m\x1b[{0}m{1}\x1b[0m'.format(dic[color], text))

# QR module pretty-print
def printModule(c):
	if c == 0:
		sys.stdout.write('\x1b[47m  \x1b[0m')
	elif c == 1:
		sys.stdout.write('\x1b[40m  \x1b[0m')
	elif c == 2:
		sys.stdout.write('\x1b[44m  \x1b[0m')
	else:
		sys.stderr.write(u'error: 不正な色です\n')
		sys.exit(1)

# QR code pretty-print
def showData(data):
	for y in range(len(data)):
		for x in range(len(data)):
			printModule(data[x][y])
		print ''

# Check if the finder pattern is valid
def checkFinder(data, xoffset, yoffset):
	for x in range(7):
		for y in range(7):
			if x == 0 or y == 0 or x == 6 or y == 6 or ((2 <= x <= 4) and (2 <= y <= 4)):
				if data[xoffset + x][yoffset + y] == 0:
					return False
			else:
				if data[xoffset + x][yoffset + y] == 1:
					return False
	return True

# Hamming distance computation (bytewise)
def hammingDistance(s1, s2):
	if len(s1) != len(s2):
		sys.stderr.write(u'error: 文字列の長さが違います\n')
		sys.exit(1)
	r = 0
	for i in range(len(s1)):
		if s1[i] != s2[i]:
			r += 1
	return r

# Mask pattern generator
def mask(pat, x, y):
	if pat == 0:
		return (x + y) % 2 == 0
	if pat == 1:
		return y % 2 == 0
	if pat == 2:
		return x % 3 == 0
	if pat == 3:
		return (x + y) % 3 == 0
	if pat == 4:
		return ((x // 3) + (y // 2)) % 2 == 0
	if pat == 5:
		return (x * y) % 2 + (x * y) % 3 == 0
	if pat == 6:
		return ((x * y) % 2 + (x * y) % 3) % 2 == 0
	if pat == 7:
		return ((x * y) % 3 + (x + y) % 2) % 2 == 0
	sys.stderr.write(u'error: invalid mask pattern\n')
	sys.exit(1)

TO_STR = '01?' # convert 0,1,2 -> 0,1,?

def try_merge(s1, s2):
	if len(s1) != len(s2):
		raise ValueError("attempted to merge different-length strings")
	out = ''
	differ = False
	for c1, c2 in zip(s1, s2):
		if c1 == '?' and c2 == '?':
			out += '?'
		elif c1 == '?':
			out += c2
		elif c2 == '?':
			out += c1
		elif c1 == c2:
			out += c1
		else:
			differ = True
			out += c1
	return out, differ

if __name__ == '__main__':
	#--------------------------------Setup--------------------------------
	# Command-line parsing
	parser = argparse.ArgumentParser(description = 'sqrd - Strong QR Decoder')
	parser.add_argument('-e', '--error-correction', help = u'エラー訂正レベル(1:L 0:M 3:Q 2:H)')
	parser.add_argument('-m', '--mask', help = u'マスクパターン(0〜7)')
	parser.add_argument('-n', '--no-correction', action = 'store_true', help = u'データブロックの誤り訂正をしない')
	parser.add_argument('-v', '--verbose', action = 'store_true', help = u'詳細な情報を表示')
	parser.add_argument('FILE', nargs = '?', default = '-', help = u'入力ファイル(デフォルトは標準入力)')
	args = parser.parse_args()

	#--------------------------------Input reading--------------------------------
	# Read text file
	if args.FILE == '-':
		text = sys.stdin.read()
	else:
		stream = open(args.FILE, 'r')
		text = stream.read()
		stream.close()
	lines = text.split('\n')
	width = len(lines[0])
	for i in range(width):
		if len(lines[i]) != width:
			sys.stderr.write(u'error: Input data is not square\n')
			sys.exit(1)
	# Compute QR code version
	if (width - 21) % 4 != 0 or width < 21 or 177 < width:
		sys.stderr.write(u'error: Invalid QR code size\n')
		sys.exit(1)
	version = (width - 21) // 4 + 1
	if args.verbose:
		print u'Size:\t{0} ({1} x {1})'.format(version, width)
	# Create 2D array "data"
	data = []
	for i in range(width):
		data.append([])
	for line in lines:
		for i in range(len(line)):
			if line[i] in 'XxOo#1': #暗モジュール
				data[i].append(1)
			elif line[i] in '_- 0': #明モジュール
				data[i].append(0)
			elif line[i] in '?': #不明
				data[i].append(2)
			else:
				sys.stderr.write(u'error: 不正な文字が含まれています\n')
				sys.exit(1)
	# Show the input data
	if args.verbose:
		print u'Input QR code:'
		showData(data)

	#--------------------------------Check fixed patterns--------------------------------
	# Check finder pattern
	if checkFinder(data, 0, 0) and checkFinder(data, width - 7, 0) and checkFinder(data, 0, width - 7):
		valid_finder_pattern = True
	else:
		valid_finder_pattern = False
	if args.verbose:
		print ''
		if valid_finder_pattern:
			stdoutColor('[ OK ]', 'green')
		else:
			stdoutColor('[ NG ]', 'red')
		print u' Finder pattern'
	# Check separator pattern
	valid_separator = True
	for i in range(8):
		if data[i][7] == 1 or data[7][i] == 1 or data[width - 8 + i][7] == 1 or data[width - 8][i] == 1 or data[i][width - 8] == 1 or data[7][width - 8 + i] == 1:
			valid_separator = False
	if args.verbose:
		if valid_separator:
			stdoutColor('[ OK ]', 'green')
		else:
			stdoutColor('[ NG ]', 'red')
		print u' Separator pattern'
	# Check timing pattern
	valid_timing_pattern = True
	for i in range(width - 16):
		if data[8 + i][6] == i % 2 or data[6][8 + i] == i % 2:
			valid_timing_pattern = False
	if args.verbose:
		if valid_timing_pattern:
			stdoutColor('[ OK ]', 'green')
		else:
			stdoutColor('[ NG ]', 'red')
		print u' Timing pattern'
	# Check alignment pattern
	valid_alignment_pattern = True
	array = alignment_pattern_array[version - 1]
	for x in array:
		for y in array:
			if not ((x < 9 and y < 9) or (width - 10 < x and y < 9) or (x < 9 and width - 10 < y)): #位置検出パターンと重なる場合は除外する
				for i in range(-2, -2 + 5):
					for j in range(-2, -2 + 5):
						if max(abs(i), abs(j)) == 1:
							if data[x + i][y + j] == 1:
								valid_alignment_pattern = False
						else:
							if data[x + i][y + j] == 0:
								valid_alignment_pattern = False
	if args.verbose:
		if valid_alignment_pattern:
			stdoutColor('[ OK ]', 'green')
		else:
			stdoutColor('[ NG ]', 'red')
		print u' Alignment pattern'
	# Create is_data_module[x][y]
	is_data_module = []
	for x in range(width):
		t = []
		for y in range(width):
			if (x <= 8 and y <= 8) or (width - 8 <= x and y <= 8) or (x <= 8 and width - 8 <= y) or x == 6 or y == 6:
				t.append(False)
			else:
				t.append(True)
		is_data_module.append(t)
	for x in array:	# Remove alignment pattern
		for y in array:
			if not ((x < 9 and y < 9) or (width - 10 < x and y < 9) or (x < 9 and width - 10 < y)): #位置検出パターンと重なる場合は除外する
				for i in range(-2, -2 + 5):
					for j in range(-2, -2 + 5):
						is_data_module[x + i][y + j] = False
	if 7 <= version:
		for i in range(6): # Remove lower left version information
			for j in range(3):
				is_data_module[i][-11 + j] = False
		for j in range(6): # Remove upper right version information
			for i in range(3):
				is_data_module[-11 + i][j] = False

	#--------------------------------Version information check--------------------------------
	if 7 <= version:
		# Lower left block
		left_bottom = ''
		for i in range(6):
			for j in range(3):
				left_bottom += TO_STR[data[i][-11 + j]]
		left_bottom = left_bottom[::-1]
		if args.verbose:
			print u'\nVersion information (lower left):\t\t{0}'.format(left_bottom)
		# Upper right block
		right_top = ''
		for j in range(6):
			for i in range(3):
				right_top += TO_STR[data[-11 + i][j]]
		right_top = right_top[::-1]
		if args.verbose:
			print u'Version information (top right):\t\t{0}'.format(right_top)
		# Combine the two blocks
		composed, diff_format = try_merge(left_bottom, right_top)
		if args.verbose:
			if diff_format:
				stdoutColor('[ NG ]', 'red')
			else:
				stdoutColor('[ OK ]', 'green')
			print u' Check version information match'
			print u'Version information (combined):\t\t{0}'.format(composed)
		# Fix errors
		version_information = composed.replace('?', '0') # replace unknown modules with 0
		min_hamming_distance = 18
		index = -1
		for i in range(32):
			d = hammingDistance(version_information, '{0:018b}'.format(version_information_table[i]))
			if d < min_hamming_distance and d <= 3:
				index = i
		if index == -1: # Failed to fix errors
			if args.verbose:
				stdoutColor('[ NG ]', 'red')
				print u' Version information repair'
		else:
			if args.verbose:
				stdoutColor('[ OK ]', 'green')
				print u' Version information repair'
			version_information = '{0:018b}'.format(version_information_table[index])
			if args.verbose:
				print u'Version information (after repair):\t{0}'.format(version_information)

	#--------------------------------Format information check--------------------------------
	#常に暗であるモジュールが間違っていないかどうか
	if data[8][4 * version + 9] == 0:
		valid_always_black = False
	else:
		valid_always_black = True
	if args.verbose:
		print ''
		if valid_always_black:
			stdoutColor('[ OK ]', 'green')
		else:
			stdoutColor('[ NG ]', 'red')
		print u' 常暗モジュール'
	#形式情報(format information)の取得
	format_mask = '101010000010010'
	#横方向の形式情報
	yoko = ''
	for i in range(15):
		if i <= 5:
			yoko += TO_STR[data[i][8]]
		elif i == 6:
			yoko += TO_STR[data[i+1][8]]
		else:
			yoko += TO_STR[data[width - 8 + i - 7][8]]
	if args.verbose:
		print u'形式情報(横):\t\t\t{0}'.format(yoko)
	#縦方向の形式情報
	tate = ''
	for i in range(15):
		if i <= 6:
			tate += TO_STR[data[8][width - 1 - i]]
		elif i <= 8:
			tate += TO_STR[data[8][8 - (i - 7)]]
		else:
			tate += TO_STR[data[8][5 - (i - 9)]]
	if args.verbose:
		print u'形式情報(縦):\t\t\t{0}'.format(tate)
	#縦横の形式情報の合成
	composed, diff_format = try_merge(yoko, tate)
	if args.verbose:
		if diff_format:
			stdoutColor('[ NG ]', 'red')
		else:
			stdoutColor('[ OK ]', 'green')
		print u' 縦横の形式情報の整合性'
		print u'形式情報(合成):\t\t{0}'.format(composed)
	composed_unmask = ''.join(['0' if x == y else '1' if x in '01' and y in '01' else '?' for (x, y) in zip(composed, format_mask)])
	if args.verbose:
		print u'形式情報(マスク解除):\t{0}'.format(composed_unmask)
	#誤り訂正
	format_information = composed_unmask#.replace('?', '0') #不明モジュールを0で埋める
	min_hamming_distance = 15
	index = -1
	for i in range(32):
		d = hammingDistance(format_information, format_information_table[i])
		if d < min_hamming_distance and d <= 3:
			index = i
	if index == -1: #誤り訂正失敗
		if args.verbose:
			stdoutColor('[ NG ]', 'red')
			print u' 形式情報の誤り訂正'
		if '?' in composed_unmask[:5] and not (args.error_correction != None and args.mask != None): #データ部が全て不明で、引数指定もなし
			sys.stderr.write(u'error: 形式情報のデータ部が不明、かつ誤り訂正に失敗しました\n')
			sys.exit(1)
		elif '?' in composed_unmask[:2] and args.error_correction == None: #エラー訂正レベルが不明で、引数指定もなし
			sys.stderr.write(u'error: 形式情報のデータ部が不明、かつ誤り訂正に失敗しました\n')
			sys.exit(1)
		elif '?' in composed_unmask[2:5] and args.mask == None: #マスクパターンが不明で、引数指定もなし
			sys.stderr.write(u'error: 形式情報のデータ部が不明、かつ誤り訂正に失敗しました\n')
			sys.exit(1)
		else: #誤り訂正には失敗したがデータ部は無事、もしくは自分で設定した
			format_information = composed_unmask
	else:
		if args.verbose:
			stdoutColor('[ OK ]', 'green')
			print u' 誤り訂正'
		format_information = format_information_table[index]
		if args.verbose:
			print u'形式情報(誤り訂正後):\t{0}'.format(format_information)
	#誤り訂正レベル(error correction level)の取得
	if args.error_correction != None:
		error_correction_level = int(args.error_correction, 0)
	else:
		error_correction_level = int(format_information[:2], 2)
	if error_correction_level == 0b01:
		m = 'L'
	if error_correction_level == 0b00:
		m = 'M'
	if error_correction_level == 0b11:
		m = 'Q'
	if error_correction_level == 0b10:
		m = 'H'
	if args.verbose:
		print u'\n誤り訂正レベル:\t{0:02b}\t({1})'.format(error_correction_level, m)
	#マスクパターン(mask pattern)の取得
	if args.mask != None:
		mask_pattern = int(args.mask, 0)
	else:
		mask_pattern = int(format_information[2:5], 2)
	if args.verbose:
		if mask_pattern == 0:
			m = '(x + y) mod 2 = 0'
		if mask_pattern == 1:
			m = 'y mod 2 = 0'
		if mask_pattern == 2:
			m = 'x mod 3 = 0'
		if mask_pattern == 3:
			m = '(x + y) mod 3 = 0'
		if mask_pattern == 4:
			m = '((x // 3) + (y // 2)) mod 2 = 0'
		if mask_pattern == 5:
			m = '(x * y) mod 2 + (x * y) mod 3 = 0'
		if mask_pattern == 6:
			m = '((x * y) mod 2 + (x * y) mod 3) mod 2 = 0'
		if mask_pattern == 7:
			m = '((x * y) mod 3 + (x + y) mod 2) mod 2 = 0'
		print u'マスクパターン:\t{0}\t[ {1} ]'.format(mask_pattern, m)

	#--------------------------------マスク解除--------------------------------
	#マスク(mask)を解除
	for y in range(width):
		for x in range(width):
			if is_data_module[x][y] and mask(mask_pattern, x, y):
				if data[x][y] == 0:
					data[x][y] = 1
				elif data[x][y] == 1:
					data[x][y] = 0
	if args.verbose:
		print u'\nマスク解除後のデータ:'
		showData(data)

	#--------------------------------コード語列読み込み--------------------------------
	#コード語列読み込み
	blocks = []
	block = ''
	count = 0
	x = width - 1
	y = width - 1
	while True:
		if x < 0 or y < 0:
			break
		if is_data_module[x][y]:
			block += '?' if data[x][y] == 2 else str(data[x][y])
			count += 1
			if count == 8:
				blocks.append(block)
				block = ''
				count = 0
		tx = x if x < 7 else x - 1 #タイミングパターンを考慮
		if tx % 2 == 1:
			x -= 1
		else:
			if (tx // 2) % 2 == 1:
				#上へ行く
				if y == 0:
					x -= 1
				else:
					y -= 1
					x += 1
			else:
				#下へ行く
				if y == width - 1:
					if (tx // 2) == 3: #縦のタイミングパターンをとばす
						x -= 1
					x -= 1
				else:
					y += 1
					x += 1
	if args.verbose:
		print u'\nTotal codewords: {0}'.format(len(blocks))
		print u'Raw data blocks: {0}'.format(repr(blocks))
	#RSブロックに分割する
	RS_blocks = []
	block_num = RS_block_num_table[version - 1][error_correction_level]
	offset = data_code_num_table[version - 1][error_correction_level]
	for i in range(block_num):
		t = []
		for j in range(offset // block_num): #データ部
			t.append(blocks[j * block_num + i])
		if offset % block_num != 0: #端数のある場合
			remain = offset % block_num
			if (block_num - remain) <= i:
				t.append(blocks[(offset // block_num) * block_num + (i - (block_num - remain))])
		for j in range((len(blocks) - offset) // block_num): #誤り訂正符号部
			t.append(blocks[offset + j * block_num + i])
		RS_blocks.append(t)
	if args.verbose:
		print u'RS block count:\t{0}'.format(len(RS_blocks))
		print u'RS block dump:'
		for i in range(len(RS_blocks)):
			print '{0}'.format(repr(RS_blocks[i]))

	#誤り訂正
	# (最大)誤り訂正数を求める
	if version == 1:
		if error_correction_level == 0b01: #L
			ecc_block_count = 7
		elif error_correction_level == 0b00: #M
			ecc_block_count = 10
		elif error_correction_level == 0b11: #Q
			ecc_block_count = 13
		elif error_correction_level == 0b10: #H
			ecc_block_count = 17
	elif version == 2 and error_correction_level == 0b01:
		ecc_block_count = 10
	elif version == 3 and error_correction_level == 0b01:
		ecc_block_count = 15
	else:
		ecc_block_count = (len(blocks) - offset) // block_num

	if args.verbose:
		print "Error correction blocks: ", ecc_block_count
	data_bytes = []
	for i in range(block_num):
		if args.verbose:
			print "Decoding RS block ", i
			print "\tCurrent block:", RS_blocks[i]
		erasures = [j for j,r in enumerate(RS_blocks[i]) if '?' in r]
		normblock = [int(r.replace('?','0'),2) for r in RS_blocks[i]]
		if args.verbose:
			print "\tErasure positions:", erasures
		mes, ecc = reedsolo.rs_correct_msg(normblock, ecc_block_count, erase_pos=erasures)
		mes = bytearray(mes)
		if args.verbose:
			print "\tDecoded bytes:", ' '.join('%02x' % b for b in mes)
		data_bytes += mes

	if args.verbose:
		print u'\n最終的なデータバイト列: {0} ({1}バイト)'.format(' '.join('%02x' % b for b in data_bytes), len(data_bytes))
	data_bits = ''
	for block in data_bytes:
		data_bits += '{0:08b}'.format(block)
	if args.verbose:
		print u'最終的なデータビット列: {0}'.format(data_bits)
	#データを読み終えるまで繰り返し
	data = []
	while len(data_bits) != 0:
		#モード指示子(mode indicator)の取得
		if len(data_bits[:4]) != 4:
			sys.stderr.write(u'\n残りビット数が4ビット未満のため終了\n')
			break
		mode = int(data_bits[:4], 2)
		m = ''
		if mode == 0b0001:
			m = u'数字'
		elif mode == 0b0010:
			m = u'英数字'
		elif mode == 0b0100:
			m = u'8ビットバイト'
		elif mode == 0b1110:
			m = u'埋め草コード語'
		elif mode == 0b0000:
			m = u'終端パターン'
		else:
			sys.stderr.write(u'error: 未対応のモード指示子です\n')
			sys.exit(1)
		if args.verbose:
			print u'\nモード指示子:\t{0} ({1})'.format('{0:04b}'.format(mode), m)
		data_bits = data_bits[4:]
		#数字のとき
		if mode == 0b0001:
			#文字数指示子を取得
			if version <= 9:
				length_indicator_length = 10
			elif version <= 26:
				length_indicator_length = 12
			else:
				length_indicator_length = 16
			length = int(data_bits[:length_indicator_length], 2)
			data_bits = data_bits[length_indicator_length:]
			if args.verbose:
				print u'文字数:\t{0}'.format(length)
			#データを読む
			for i in range((length + 2) // 3):
				if i == (length + 2) // 3 - 1: #最後の1または2けた
					if length % 3 == 0:
						num = int(data_bits[:10], 2)
						data_bits = data_bits[10:]
						data.extend(map(ord, '{0:03d}'.format(num)))
					elif length % 3 == 1:
						num = int(data_bits[:4], 2)
						data_bits = data_bits[4:]
						data.extend(map(ord, '{0:01d}'.format(num)))
					else:
						num = int(data_bits[:7], 2)
						data_bits = data_bits[7:]
						data.extend(map(ord, '{0:02d}'.format(num)))
				else:
					num = int(data_bits[:10], 2)
					data_bits = data_bits[10:]
					data.extend(map(ord, str(num)))
			if args.verbose:
				print u'デコードされたデータ: {0}'.format(repr(map(hex, data)))
		#英数字のとき
		if mode == 0b0010:
			#文字数指示子を取得
			if version <= 9:
				length_indicator_length = 9
			elif version <= 26:
				length_indicator_length = 11
			else:
				length_indicator_length = 13
			length = int(data_bits[:length_indicator_length], 2)
			data_bits = data_bits[length_indicator_length:]
			if args.verbose:
				print u'文字数:\t{0}'.format(length)
			#データを読む
			for i in range((length + 1) // 2):
				if i == (length + 1) // 2 - 1: #最後の1または2けた
					if length % 2 == 0:
						num = int(data_bits[:11], 2)
						data_bits = data_bits[11:]
						data.extend([ord(alphanumeric_table[num // 45]), ord(alphanumeric_table[num % 45])])
					else:
						num = int(data_bits[:6], 2)
						data_bits = data_bits[6:]
						data.extend([ord(alphanumeric_table[num])])
				else:
					num = int(data_bits[:11], 2)
					data_bits = data_bits[11:]
					data.extend([ord(alphanumeric_table[num // 45]), ord(alphanumeric_table[num % 45])])
			if args.verbose:
				print u'デコードされたデータ: {0}'.format(repr(map(hex, data)))
		#8ビットバイトのとき
		if mode == 0b0100:
			#文字数指示子を取得
			if version <= 9:
				length_indicator_length = 8
			else:
				length_indicator_length = 16
			length = int(data_bits[:length_indicator_length], 2)
			data_bits = data_bits[length_indicator_length:]
			if args.verbose:
				print u'文字数:\t{0}'.format(length)
			#データを読む
			for i in range(length):
				data.append(int(data_bits[:8], 2))
				data_bits = data_bits[8:]
			if args.verbose:
				print u'デコードされたデータ: {0}'.format(repr(map(hex, data)))
		#終端パターンのとき
		if mode == 0b0000:
			break
		if args.verbose:
			print '残りのビット列: {0}'.format(data_bits)
			print 'デコード済み文字列: {0}'.format(''.join(map(chr, data)))
	if args.verbose:
		print ''
	print ''.join(map(chr, data))
	

