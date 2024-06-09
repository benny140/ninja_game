import os
import pygame
import math

BASE_IMG_PATH = "data/images/"


def load_image(path, background_colour=(0, 0, 0)):
    # convert improves performance
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(background_colour)
    return img


def load_images(path, background_colour=(0, 0, 0)):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        # the function above will include the base path.
        img = load_image(path + "/" + img_name, background_colour)
        images.append(img)
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True) -> None:
        self.images = images
        self.img_dur = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_dur * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_dur * len(self.images) - 1)
            if self.frame >= self.img_dur * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[math.floor(int(self.frame) / self.img_dur)]
