import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import StringIO
from settings import STATIC_ROOT

numbers = ''.join(map(str, range(10)))
chars = ''.join((numbers))

def create_validate_code(size=(70, 20), chars=chars, mode="RGB", bg_color=(255, 255, 255), fg_color=(255, 0, 0), font_size=18, font_type=os.path.join(STATIC_ROOT, 'fonts/Arial.ttf'),length=4, draw_points=True, point_chance=2):
	width, height = size
	img = Image.new(mode, size, bg_color) 
	draw = ImageDraw.Draw(img)
	print font_type
	def get_chars():
		return random.sample(chars, length)
	def create_points():
		chance = min(50, max(0, int(point_chance)))
		for w in xrange(width):
			for h in xrange(height):
				tmp = random.randint(0, 50)
				if tmp > 50 - chance:
					draw.point((w, h), fill=(0, 0, 0))

	def create_strs():
		c_chars = get_chars()
		strs = ''.join(c_chars)
		font = ImageFont.truetype(font_type, font_size)
		font_width, font_height = font.getsize(strs)
		draw.text(((width - font_width) / 3, (height - font_height) / 4),strs, font=font, fill=fg_color)
		return strs
	if draw_points:create_points()
	strs = create_strs()
	params = [1 - float(random.randint(1, 2)) / 100, 0, 0, 0, 1 - float(random.randint(1, 10)) / 100, float(random.randint(1, 2)) / 500, 0.001, float(random.randint(1, 2)) / 500]
	img = img.transform(size, Image.PERSPECTIVE, params)
	img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
	return img,strs


