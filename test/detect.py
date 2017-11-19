#!/usr/bin/env python

import sys

sys.path.insert(0,'..')
from encdect import EncodingDetectFile

TEST_FILE_DIR = './file'


def main():
	encoding_detect_file = EncodingDetectFile()

	def detect(filename):
		# build path to test file
		filepath = '{0}/{1}'.format(TEST_FILE_DIR,filename)
		print(filepath)

		# detect and load file
		result = encoding_detect_file.load(filepath)

		if (result):
			# report results
			encoding,bom_marker,file_content = result
			print((encoding,bom_marker))
			print(file_content + '\n')

	detect('utf-8-bom.txt')
	detect('utf-16be-bom.txt')
	detect('utf-16le-bom.txt')

	detect('ascii.txt')
	detect('utf-8.txt')

	detect('utf-16be-oneline.txt')
	detect('utf-16be-multiline.txt')

	detect('utf-16le-oneline.txt')
	detect('utf-16le-multiline.txt')


if (__name__ == '__main__'):
	main()
