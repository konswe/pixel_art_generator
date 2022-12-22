from PIL import Image
import random
import os

if not os.path.exists("pictures"):
    os.makedirs("pictures")


def interpolate_color(start_color, end_color, steps):
    r_step = (end_color[0] - start_color[0]) / steps
    g_step = (end_color[1] - start_color[1]) / steps
    b_step = (end_color[2] - start_color[2]) / steps

    gradient = []
    for i in range(steps):
        r = int(start_color[0] + r_step * i)
        g = int(start_color[1] + g_step * i)
        b = int(start_color[2] + b_step * i)
        gradient.append((r, g, b))

    return gradient


def gradient_function(start_color, end_color, steps):
    num_interpolation_steps = 100
    interpolated_colors = interpolate_color(start_color, end_color, num_interpolation_steps)

    gradient = []
    for i in range(steps):
        interpolated_index = int(i * num_interpolation_steps / steps)
        gradient.append(interpolated_colors[interpolated_index])

    return gradient


image_width = int(input("Enter the width of the image: "))
image_height = int(input("Enter the height of the image: "))
max_dimension = max(image_width, image_height)

color_scheme = input("Enter the color scheme (random, monochromatic, gradient): ")
for x in range(0, 10):
    i = 0
    while os.path.exists(os.path.join("pictures", "pixel_art_{}.png".format(i))):
        i += 1

    image = Image.new("RGB", (image_width, image_height))

    start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    for x in range(image_width):
        for y in range(image_height):
            distance_from_center = ((x - image_width / 2) ** 2 + (y - image_height / 2) ** 2) ** 0.5

            intensity = int(255 * (1 - distance_from_center / (max_dimension / 2)))

            r = int(random.uniform(intensity, 255))
            g = int(random.uniform(intensity, 255))
            b = int(random.uniform(intensity, 255))

            if color_scheme == "monochromatic":
                r = g = b = random.randint(0, 255)
            elif color_scheme == "gradient":
                gradient = gradient_function(start_color, end_color, 100)

                gradient_index = int(distance_from_center / (max_dimension / 2) * len(gradient))

                if 0 <= gradient_index < len(gradient):
                    r, g, b = gradient[gradient_index]
                else:

                    r, g, b = (0, 0, 0)

            image.putpixel((x, y), (r, g, b))

    image.save(os.path.join("pictures", "pixel_art_{}.png".format(i)))
