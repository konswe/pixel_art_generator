from PIL import Image
import random
import os

image_width = 100
image_height = 100

i = 0
while os.path.exists("pixel_art_{}.png".format(i)):
    i += 1

image = Image.new("RGB", (image_width, image_height))


for x in range(image_width):
    for y in range(image_height):
        distance_from_center = ((x - image_width/2)**2 + (y - image_height/2)**2)**0.5

        if x > 0:
            left_pixel = image.getpixel((x-1, y))
        else:
            left_pixel = (0, 0, 0)

        if y > 0:
            above_pixel = image.getpixel((x, y-1))
        else:
            above_pixel = (0, 0, 0)

        intensity = int(255 * (1 - distance_from_center / (image_width/2)))
        r = int(left_pixel[0] * 0.9 + random.uniform(intensity, 255) * 0.1)
        g = int(above_pixel[1] * 0.9 + random.uniform(intensity, 255) * 0.1)
        b = int(left_pixel[2] * 0.9 + random.uniform(intensity, 255) * 0.1)
        image.putpixel((x, y), (r, g, b))

image.save("pixel_art_{}.png".format(i))