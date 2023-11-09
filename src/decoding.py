def decode_file(image_path):
	EOF_BYTES = '\\xff\\xd9'

	with open(image_path, 'rb') as f:
		contents = str(f.read())

	text_start_index = contents.index(EOF_BYTES)+8 	

	return contents[text_start_index:-1]