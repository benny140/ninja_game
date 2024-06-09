import random


class Cloud:
    def __init__(self, pos, img, speed, depth) -> None:
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )
        surf.blit(
            self.img,
            (
                render_pos[0] % (surf.get_width() + self.img.get_width())
                - self.img.get_width(),
                render_pos[1] % (surf.get_height() + self.img.get_height())
                - self.img.get_height(),
            ),
        )


class Clouds:
    def __init__(self, cloud_images, count=16) -> None:
        self.clouds = []
        for i in range(count):
            pos = (9999 * random.random(), 9999 * random.random())
            img = random.choice(cloud_images)
            speed = 0.05 * random.random() + 0.05
            depth = 0.6 * random.random() + 0.2
            self.clouds.append(Cloud(pos, img, speed, depth))
        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
