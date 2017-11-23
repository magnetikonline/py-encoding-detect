# Encoding detect
Python module for detecting the following encodings of a text file:
- `ASCII`
- `UTF-8`
- `UTF-16BE`
- `UTF-16LE`

Will validate `UTF-8/16` files both with/without a [byte order mark](https://en.wikipedia.org/wiki/Byte_order_mark) (BOM) present.

- [Usage](#usage)
- [Detection methods](#detection-methods)
	- [Byte order mark (BOM)](#byte-order-mark-bom)
	- [ASCII/UTF-8](#asciiutf-8)
	- [UTF-16BE/UTF-16LE](#utf-16beutf-16le)
- [Test](#test)
- [Reference](#reference)

## Usage
Module [`encdect.py`](encdect.py) provides a single `EncodingDetectFile` class and a [`load()`](encdect.py#L144) method:
- Successful detection returns a tuple of `(encoding,bom_marker,file_unicode)`.
- Failure (unable to determine) returns `False`.

Example:

```python
from encdect import EncodingDetectFile

detect = EncodingDetectFile()
result = detect.load('./test/file/utf-8-bom.txt')

if (result):
	print(result)
	# ('utf_8', '\xef\xbb\xbf', u'Test string \U0001f44d\u263a\n')
```

Updating a text file, preserving encoding/BOM (if present):

```python
from encdect import EncodingDetectFile
UPPERCASE_WORD = 'string'

detect = EncodingDetectFile()
result = detect.load('./test/file/utf-8.txt')

if (result):
	encoding,bom_marker,file_decode = result

	print(type(file_decode))
	# <type 'unicode'>

	file_decode = file_decode.replace(
		UPPERCASE_WORD,
		UPPERCASE_WORD.upper()
	)

	fh = open('./output.txt','w')

	if (bom_marker):
		fh.write(bom_marker)

	fh.write(file_decode.encode(encoding))
	fh.close()
```

## Detection methods
Routines used are based on the work of the C++/C# library https://github.com/AutoIt/text-encoding-detect, with minor tweaks/optimizations.

If _all steps_ are passed without a positive result then detection is considered _not possible_.

An overview of detection steps follows:

### Byte order mark (BOM)
First step looks for a byte order mark in the first 2-3 bytes of the file, specifically (in this order):
- `UTF-16BE` (2 bytes)
- `UTF-16LE` (2 bytes)
- `UTF-8` (3 bytes, fairly rare)

If a BOM is found it is assumed to be valid for the file and detection finishes.

### ASCII/UTF-8
If no BOM found, step determines if file is either `ASCII` or `UTF-8`. Process overview:
- Single byte is read from the file.
- Value determines how many additional bytes [define the character](https://en.wikipedia.org/wiki/UTF-8#Codepage_layout):
	- `1 -> 127` no additional (ASCII).
	- `194 -> 223` 1 additional.
	- `224 -> 239` 2 additional.
	- `240 -> 244` 3 additional.
- Additional bytes are walked over - each must be within the bounds of `128 -> 191`.
- Return to first step and repeat until end of file.

If end of file reached and above rules remain true:
- With all bytes between ranges of `1 -> 127` return result of `ASCII`.
- Else result if `UTF-8`.

### UTF-16BE/UTF-16LE
Final step for `UTF-16` involves two methods.

#### Method 1
End of line (EOL) characters (`\r\n`) are counted in odd/even positions of the file stream:
- If all EOL characters are in _even_ file positions return result of `UTF-16BE`.
- Alternatively if all EOL characters are in _odd_ file positions return result of `UTF-16LE`.

#### Method 2
Relying on the fact that text files generally have a high ratio of characters in the `1 -> 127` range, two byte sequences of `[0,1 -> 127]` or `[1 -> 127,0]` should be common.
- Total of null bytes are counted in both odd and even positions.
- If odd count _above_ positive threshold and even count _below_ negative threshold, return result of `UTF-16BE`.
- If odd count _below_ negative threshold and even count _above_ positive threshold, return result of `UTF-16LE`.

## Test
A detection of sample files with various encoding formats can be run via [`test/detect.py`](test/detect.py).

## Reference
- https://docs.python.org/2/howto/unicode.html
- https://docs.python.org/2/library/codecs.html
- https://github.com/AutoIt/text-encoding-detect
- https://en.wikipedia.org/wiki/Endianness
