from PIL import Image
import random
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QProgressBar

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


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.width_label = QLabel("Width:")
        self.width_edit = QLineEdit()
        self.height_label = QLabel("Height:")
        self.height_edit = QLineEdit()
        self.color_scheme_label = QLabel("Color Scheme:")
        self.color_scheme_combo_box = QComboBox()
        self.color_scheme_combo_box.addItems(["random", "monochromatic", "gradient"])
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_pixel_art)

        self.progress_bar = QProgressBar()
        layout = QVBoxLayout()
        layout.addWidget(self.width_label)
        layout.addWidget(self.width_edit)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_edit)
        layout.addWidget(self.color_scheme_label)
        layout.addWidget(self.color_scheme_combo_box)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

    def generate_pixel_art(self):
        image_width = int(self.width_edit.text())
        image_height = int(self.height_edit.text())
        max_dimension = max(image_width, image_height)
        color_scheme = self.color_scheme_combo_box.currentText()

        i = 0
        while os.path.exists(os.path.join("pictures", "pixel_art_{}.png".format(i))):
            i += 1

        image = Image.new("RGB", (image_width, image_height))

        start_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        end_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(image_width * image_height)
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
                self.progress_bar.setValue((x * image_height) + y)
                

        image.save(os.path.join("pictures", "pixel_art_{}.png".format(i)))
        self.progress_bar.setValue(0)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
