import unittest

import pygame

from pgturbo.actor import Actor
from pgturbo.loaders import set_root


TEST_DISP_W, TEST_DISP_H = (200, 100)


class WebpLoaderTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        pygame.display.quit()

    def test_loader_finds_webp(self):
        actor = Actor("alien_as_webp")

        # Just instantiating the actor shows webp image loading works
        assert actor

    def test_animation_loader_finds_webp(self):
        """Animations can be loaded from .webp files both in folders and as
        spritesheets."""
        actor = Actor("alien")
        actor.anim.add("walk_up_as_webp")

        self.assertEqual(actor.anim.animation_pool, ("walk_up_as_webp",))

        actor.anim.add_spritesheet("walk_down_as_webp", 64, 64)

        self.assertEqual(actor.anim.animation_pool, ("walk_up_as_webp",
                                                     "walk_down_as_webp"))
