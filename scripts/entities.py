import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.e_type + "/" + self.action].copy()

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        frame_movement = (
            movement[0] + self.velocity[0],
            movement[1] + self.velocity[1],
        )

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions["right"] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions["left"] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions["down"] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions["up"] = True
                self.pos[1] = entity_rect.y

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        else:
            self.velocity[1] = min(5, self.velocity[1] + 0.1)

        # animation logics
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            (
                self.pos[0] - offset[0] + self.anim_offset[0],
                self.pos[1] - offset[1] + self.anim_offset[1],
            ),
        )
        # surf.blit(self.game.assets[self.e_type], (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jump_count = 2
        self.wall_slide = False
        self.dashing = 0

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)
        self.air_time += 1

        if self.collisions["down"]:
            self.air_time = 0
            self.jump_count = 2
            self.velocity[0] = 0

        if self.wall_slide is False:
            self.velocity[0] = 0
            if self.air_time > 4:
                self.set_action("jump")
                if self.collisions["left"]:
                    self.wall_slide = True
                    self.velocity[0] = -1
                if self.collisions["right"]:
                    self.wall_slide = True
                    self.velocity[0] = 1
                if self.jump_count == 2:
                    self.jump_count = 1
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")
        else:
            self.set_action("wall_slide")
            self.velocity[1] = min(0.5, self.velocity[1])
            if self.collisions["down"] or not (
                self.collisions["left"] or self.collisions["right"]
            ):
                self.wall_slide = False

        if self.dashing > 0:
            self.dashing = max(self.dashing - 1, 0)
        if self.dashing < 0:
            self.dashing = min(self.dashing + 1, 0)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        # try a wall slde timer for this ...
        # if self.collisions["left"] and self.air_time > 4:
        #     self.velocity = [2, -3]
        # elif self.collisions["right"] and self.air_time > 4:
        #     self.velocity = [-2, -3]

        if not self.wall_slide:
            if self.jump_count > 0:
                self.jump_count -= 1
                self.velocity[1] = -3
                self.set_action("jump")
        else:
            self.velocity[1] = -3
            self.set_action("jump")
            self.wall_slide = False

    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)
