from PIL import Image
import numpy as np
import os

def image_to_csharp_comments(image_path, language):
	"""
	Converts a PNG image into C# ASCII art comment lines
	:param image_path: path to the PNG image
	:param output_width: desired output width (in characters)
	:param threshold: threshold for black/white conversion (0-255)
	:return: string with C# comments
	"""
	try:
		# Open the image and convert to grayscale
		img = Image.open(image_path).convert('L')

		# Convert to numpy array and analyze pixels, evaluating the correct output_width
		complete_img_array = np.array(img)
		threshold = ((complete_img_array.max() - complete_img_array.min())/2) + complete_img_array.min()
		complete_img_array = np.where(complete_img_array > threshold, 255, 0)
		
		 # Calculate proportions for resizing
		original_width, original_height = img.size
		
		result_with_ratio = find_min_feature_size(complete_img_array)
		output_width = result_with_ratio["suggested_width"]
		output_height = result_with_ratio["suggested_height"]

		 # Resize the image
		img = img.resize((output_width, output_height))
		img_array = np.array(img)
		threshold = ((img_array.max() - img_array.min())/2) + img_array.min()
		img_array = np.where(img_array > threshold, 255, 0)
		
		ascii_art = generate_comment_given_language(img_array, language)
		
		 # Join lines and add header/footer
		csharp_code = "// Automatically generated from PNG image\n"
		csharp_code += "// Original size: {}x{} pixels\n".format(original_width, original_height)
		csharp_code += "\n".join(ascii_art)
		csharp_code += "\n// End of ASCII representation"
		
		return csharp_code
	
	except Exception as e:
		return f"// Error during processing: {str(e)}"

	

def get_comment_prefix(language):
	"""
	Returns the comment prefix for the chosen language.
	
	Args:
		language (str): Target language (e.g. c#, python, c, cpp, csharp, java, rust, js, go, ... )
	
	Returns:
		str: Prefix in the specified language
	"""
	comment_prefixes = {
		'python': '# ',
		'c': '// ',
		'cpp': '// ',
		'c#': '// ',
		'csharp': '// ',
		'java': '// ',
		'rust': '// ',
		'js': '// ',
		'go': '// ',
		'arduino': '// ',
		'ruby': '# ',
		'bash': '# ',
		'swift': '// ',
		'kotlin': '// '
	}
	
	return comment_prefixes.get(language.lower(),
								'#') # Default to Python-style comment if language not recognized


def generate_comment_given_language(img_array, language):
	"""
	Generates ASCII art comment for different programming languages.
	
	Args:
		img_array (np.array): 2D numpy array (0-255)
		language (str): Target language (python, c, cpp, csharp, java, rust, js, go)
	
	Returns:
		str: Comment formatted in the specified language
	"""
	# Generate ASCII art
	ascii_art = []

	for row in img_array:
		line = get_comment_prefix(language)
		for pixel in row:
			line += ' ' if pixel == 255 else '*'
		ascii_art.append(line)

	return ascii_art


def find_min_feature_size(img_array):
	"""
	Finds the minimum size (width/height) of black (0) and white (255) pixel features.
	
	Args:
		img_array: np.array of the image (0-255).
	
	Returns:
		suggested_width, suggested_height: Suggested sizes (with aspect ratio).
	"""
	# Initialize minimums
	min_width_black = min_height_black = float('inf')
	min_width_white = min_height_white = float('inf')
	
	# HORIZONTAL analysis (widths)
	for row in img_array:
		# For black (0)
		black_pixels = np.where(row == 0)[0]
		if len(black_pixels) > 0:
			sequences = np.split(black_pixels, np.where(np.diff(black_pixels) != 1)[0] + 1)
			min_width_black = min(min_width_black, min(len(seq) for seq in sequences))
		
		# For white (255)
		white_pixels = np.where(row == 255)[0]
		if len(white_pixels) > 0:
			sequences = np.split(white_pixels, np.where(np.diff(white_pixels) != 1)[0] + 1)
			min_width_white = min(min_width_white, min(len(seq) for seq in sequences))
	
	# VERTICAL analysis (heights)
	for col in img_array.T:  # Transposed for columns
		# For black (0)
		black_pixels = np.where(col == 0)[0]
		if len(black_pixels) > 0:
			sequences = np.split(black_pixels, np.where(np.diff(black_pixels) != 1)[0] + 1)
			min_height_black = min(min_height_black, min(len(seq) for seq in sequences))
		
		# For white (255)
		white_pixels = np.where(col == 255)[0]
		if len(white_pixels) > 0:
			sequences = np.split(white_pixels, np.where(np.diff(white_pixels) != 1)[0] + 1)
			min_height_white = min(min_height_white, min(len(seq) for seq in sequences))
	
	# Calculate global minimums (black and white)
	global_min_width = min(min_width_black, min_width_white)
	global_min_height = min(min_height_black, min_height_white)
	global_min = min(global_min_width, global_min_height)

	suggested_width = img_array.shape[1] / (global_min)
	suggested_height = img_array.shape[0] / (global_min)
	
	# Compensate for character height
	suggested_width = suggested_width / 2
	suggested_height = suggested_height / 2

	return {
		"suggested_width": int(suggested_width),
		"suggested_height": int(suggested_height) 
	}

def str_to_bool(s):
	if isinstance(s, str):
		return s.lower() in ('true', 't', 'yes', 'y', '1')
	return bool(s)

def str_to_int(s, default=None):
	"""Convert string to double with proper error handling"""
	try:
		return int(s.strip())
	except (ValueError, TypeError, AttributeError):
		return default

# MAIN
if __name__ == "__main__":

	input_image = input("Enter the path to the PNG image: ")
	language = input("Enter the target language (e.g. c#, python, c, cpp, java, rust, js, go, ...): ").strip().lower()

	output_file_name = "output_comments.txt"
	output_file = os.path.join(os.path.dirname(input_image), output_file_name)
	
	result = image_to_csharp_comments(input_image, language)
	
	with open(output_file, "w") as f:
		f.write(result)
	
	print(f"C# comment file successfully generated: {output_file}")
	
	openFile = str_to_bool(input("Do you want to open it?"))

	if(openFile):
		os.startfile(output_file)
	
