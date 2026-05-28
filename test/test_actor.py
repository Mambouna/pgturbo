import unittest
from unittest.mock import patch

import pygame

from pgturbo.actor import calculate_anchor, Actor
from pgturbo.loaders import set_root
from pgturbo.loaders import images


TEST_MODULE = "pgturbo.actor"
TEST_DISP_W, TEST_DISP_H = (200, 100)


class ModuleTest(unittest.TestCase):
    def test_calculate_anchor_with_float(self):
        self.assertEqual(
            calculate_anchor(1.23, "x", 12345),
            1.23
        )

    def test_calculate_anchor_centre(self):
        self.assertEqual(
            calculate_anchor("center", "x", 100),
            50
        )

    def test_calculate_anchor_bottom(self):
        self.assertEqual(
            calculate_anchor("bottom", "y", 100),
            100
        )


class ActorTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pygame.init()
        pygame.display.set_mode((TEST_DISP_W, TEST_DISP_H))
        set_root(__file__)

    @classmethod
    def tearDownClass(self):
        pygame.display.quit()

    def test_sensible_init_defaults(self):
        a = Actor("alien")

        self.assertEqual(a.image, "alien")
        self.assertEqual(a.topleft, (0, 0))

    def test_setting_absolute_initial_pos(self):
        a = Actor("alien", pos=(100, 200), anchor=("right", "bottom"))

        self.assertEqual(
            a.topleft,
            (100 - a.width, 200 - a.height),
        )

    def test_setting_relative_initial_pos_topleft(self):
        a = Actor("alien", topleft=(500, 500))
        self.assertEqual(a.topleft, (500, 500))

    def test_setting_relative_initial_pos_center(self):
        a = Actor("alien", center=(500, 500))
        self.assertEqual(a.center, (500, 500))

    def test_setting_relative_initial_pos_bottomright(self):
        a = Actor("alien", bottomright=(500, 500))
        self.assertEqual(a.bottomright, (500, 500))

    def test_setting_absolute_pos_and_relative_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", pos=(0, 0), bottomright=(500, 500))

    def test_setting_multiple_relative_pos_raises_typeerror(self):
        with self.assertRaises(TypeError):
            Actor("alien", topleft=(500, 500), bottomright=(600, 600))

    def test_unexpected_kwargs(self):
        with self.assertRaises(TypeError) as cm:
            Actor("alien", toplift=(0, 0))

        self.assertEqual(
            cm.exception.args[0],
            "Unexpected keyword argument 'toplift' (did you mean 'topleft'?)",
        )

    def test_set_pos_relative_to_anchor(self):
        a = Actor("alien", anchor=(10, 10))
        a.pos = (100, 100)
        self.assertEqual(a.topleft, (90, 90))

    def test_right_angle(self):
        a = Actor("alien")
        self.assertEqual(a.image, "alien")
        self.assertEqual(a.topleft, (0, 0))
        self.assertEqual(a.pos, (33.0, 46.0))
        self.assertEqual(a.width, 66)
        self.assertEqual(a.height, 92)
        a.angle += 90.0
        self.assertEqual(a.angle, 90.0)
        self.assertEqual(a.topleft, (-13, 13))
        self.assertEqual(a.pos, (33.0, 46.0))
        self.assertEqual(a.width, 92)
        self.assertEqual(a.height, 66)

    def test_rotation(self):
        """An actor's pos must not drift with continued small rotation."""
        a = Actor('alien', pos=(100.0, 100.0))
        for _ in range(360):
            a.angle += 1.0
        self.assertEqual(a.pos, (100.0, 100.0))

    def test_total_scale_number_no_scaling(self):
        """No scaling means the image is unchanged."""
        a = Actor("alien", (100, 100))
        original_size = (a.width, a.height)
        a.scale = 1
        self.assertEqual((a.width, a.height) + a.pos, original_size + a.pos)
        self.assertEqual(a.topleft, (67, 54))

    def test_total_scale_tuple_no_scaling(self):
        """Using tuple values also leaves the image unchanged at scale 1."""
        a = Actor("alien", (100, 100))
        original_size = (a.width, a.height)
        a.scale = (1, 1)
        self.assertEqual((a.width, a.height) + a.pos, original_size + a.pos)
        self.assertEqual(a.topleft, (67, 54))

    def test_total_scale_number_scaling_down(self):
        """Shrinking an actor works as expected, with the image changing."""
        a = Actor("alien", (100, 100))
        scale = 0.25
        exp_size = (a.width * scale, a.height * scale)
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (91.75, 88.5))

    def test_total_scale_tuple_scaling_down(self):
        """Shrinking with same values as a tuple also works."""
        a = Actor("alien", (100, 100))
        scale = (0.25, 0.25)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (91.75, 88.5))

    def test_total_scale_number_scaling_up(self):
        a = Actor("alien", (100, 100))
        scale = 2.5
        exp_size = (a.width * scale, a.height * scale)
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (17.5, -15.0))

    def test_total_scale_tuple_scaling_up(self):
        a = Actor("alien", (100, 100))
        scale = (2.5, 2.5)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (17.5, -15.0))

    def test_total_scale_scaling_x_down(self):
        """Scaling individual dimensions also works."""
        a = Actor("alien", (100, 100))
        scale = (0.25, 1.0)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (91.75, 54.0))

    def test_total_scale_scaling_y_down(self):
        a = Actor("alien", (100, 100))
        scale = (1.0, 0.25)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (67.0, 88.5))

    def test_total_scale_scaling_x_up(self):
        a = Actor("alien", (100, 100))
        scale = (2.5, 1.0)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (17.5, 54.0))

    def test_total_scale_scaling_y_up(self):
        a = Actor("alien", (100, 100))
        scale = (1.0, 2.5)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (67.0, -15.0))

    def test_total_scale_scaling_x_down_y_up(self):
        a = Actor("alien", (100, 100))
        scale = (0.25, 2.5)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (91.75, -15.0))

    def test_total_scale_scaling_x_up_y_down(self):
        a = Actor("alien", (100, 100))
        scale = (2.5, 0.25)
        exp_size = (a.width * scale[0], a.height * scale[1])
        a.scale = scale
        self.assertEqual((a.width, a.height) + a.pos, exp_size + a.pos)
        self.assertEqual(a.topleft, (17.5, 88.5))

    def test_scale_x_no_scaling(self):
        a = Actor("alien", (100, 100))
        orig_size = (a.width, a.height)
        a.scale_x = 1
        self.assertEqual((a.width, a.height), orig_size)
        self.assertEqual(a.left, 67.0)
        self.assertEqual(a.right, 133.0)

    def test_scale_x_scaling_down(self):
        a = Actor("alien", (100, 100))
        scale = 0.25
        exp_size = (a.width * scale, a.height)
        a.scale_x = scale
        self.assertEqual((a.width, a.height), exp_size)
        self.assertEqual(a.left, 91.75)
        self.assertEqual(a.right, 108.25)

    def test_scale_x_scaling_up(self):
        a = Actor("alien", (100, 100))
        scale = 2.5
        exp_size = (a.width * scale, a.height)
        a.scale_x = scale
        self.assertEqual((a.width, a.height), exp_size)
        self.assertEqual(a.left, 17.5)
        self.assertEqual(a.right, 182.5)

    def test_scale_y_no_scaling(self):
        a = Actor("alien", (100, 100))
        orig_size = (a.width, a.height)
        a.scale_y = 1
        self.assertEqual((a.width, a.height), orig_size)
        self.assertEqual(a.top, 54.0)
        self.assertEqual(a.bottom, 146.0)

    def test_scale_y_scaling_down(self):
        a = Actor("alien", (100, 100))
        scale = 0.25
        exp_size = (a.width, a.height * scale)
        a.scale_y = scale
        self.assertEqual((a.width, a.height), exp_size)
        self.assertEqual(a.top, 88.5)
        self.assertEqual(a.bottom, 111.5)

    def test_scale_y_scaling_up(self):
        a = Actor("alien", (100, 100))
        scale = 2.5
        exp_size = (a.width, a.height * scale)
        a.scale_y = scale
        self.assertEqual((a.width, a.height), exp_size)
        self.assertEqual(a.top, -15.0)
        self.assertEqual(a.bottom, 215.0)

    def test_scaling_with_rotation_total_scale_original(self):
        a = Actor("alien", (100, 100))
        a.scale = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 43.66, delta=0.02)
        self.assertAlmostEqual(a.top, 48.42, delta=0.02)

    def test_scaling_with_rotation_total_scale_up(self):
        a = Actor("alien", (100, 100))
        a.scale = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 281.69, delta=0.02)
        self.assertAlmostEqual(a.height, 257.89, delta=0.02)
        self.assertAlmostEqual(a.left, -40.84, delta=0.02)
        self.assertAlmostEqual(a.top, -28.95, delta=0.02)

    def test_scaling_with_rotation_total_scale_down(self):
        a = Actor("alien", (100, 100))
        a.scale = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 28.17, delta=0.02)
        self.assertAlmostEqual(a.height, 25.79, delta=0.02)
        self.assertAlmostEqual(a.left, 85.92, delta=0.02)
        self.assertAlmostEqual(a.top, 87.11, delta=0.02)

    def test_scaling_with_rotation_and_anchor_total_scale_original(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 3.83, delta=0.02)
        self.assertAlmostEqual(a.top, 25.42, delta=0.02)

    def test_scaling_with_rotation_and_anchor_total_scale_up(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 281.69, delta=0.02)
        self.assertAlmostEqual(a.height, 257.89, delta=0.02)
        self.assertAlmostEqual(a.left, -140.44, delta=0.02)
        self.assertAlmostEqual(a.top, -86.45, delta=0.02)

    def test_scaling_with_rotation_and_anchor_total_scale_down(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 28.17, delta=0.02)
        self.assertAlmostEqual(a.height, 25.79, delta=0.02)
        self.assertAlmostEqual(a.left, 75.96, delta=0.02)
        self.assertAlmostEqual(a.top, 81.34, delta=0.02)

    def test_scaling_with_rotation_x_original(self):
        a = Actor("alien", (100, 100))
        a.scale_x = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 43.66, delta=0.02)
        self.assertAlmostEqual(a.top, 48.42, delta=0.02)

    def test_scaling_with_rotation_x_up(self):
        a = Actor("alien", (100, 100))
        a.scale_x = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 162.17, delta=0.02)
        self.assertAlmostEqual(a.height, 188.89, delta=0.02)
        self.assertAlmostEqual(a.left, 18.91, delta=0.02)
        self.assertAlmostEqual(a.top, 5.55, delta=0.02)

    def test_scaling_with_rotation_x_down(self):
        a = Actor("alien", (100, 100))
        a.scale_x = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 87.92, delta=0.02)
        self.assertAlmostEqual(a.height, 60.29, delta=0.02)
        self.assertAlmostEqual(a.left, 56.04, delta=0.02)
        self.assertAlmostEqual(a.top, 69.86, delta=0.02)

    def test_scaling_with_rotation_and_anchor_x_original(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_x = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 3.83, delta=0.02)
        self.assertAlmostEqual(a.top, 25.42, delta=0.02)

    def test_scaling_with_rotation_and_anchor_x_up(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_x = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 162.17, delta=0.02)
        self.assertAlmostEqual(a.height, 188.89, delta=0.02)
        self.assertAlmostEqual(a.left, -20.92, delta=0.02)
        self.assertAlmostEqual(a.top, -17.45, delta=0.02)

    def test_scaling_with_rotation_and_anchor_x_down(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_x = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 87.92, delta=0.02)
        self.assertAlmostEqual(a.height, 60.29, delta=0.02)
        self.assertAlmostEqual(a.left, 16.20, delta=0.02)
        self.assertAlmostEqual(a.top, 46.86, delta=0.02)

    def test_scaling_with_rotation_y_original(self):
        a = Actor("alien", (100, 100))
        a.scale_y = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 43.66, delta=0.02)
        self.assertAlmostEqual(a.top, 48.42, delta=0.02)

    def test_scaling_with_rotation_y_up(self):
        a = Actor("alien", (100, 100))
        a.scale_y = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 232.19, delta=0.02)
        self.assertAlmostEqual(a.height, 172.16, delta=0.02)
        self.assertAlmostEqual(a.left, -16.09, delta=0.02)
        self.assertAlmostEqual(a.top, 13.92, delta=0.02)

    def test_scaling_with_rotation_y_down(self):
        a = Actor("alien", (100, 100))
        a.scale_y = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 52.92, delta=0.02)
        self.assertAlmostEqual(a.height, 68.66, delta=0.02)
        self.assertAlmostEqual(a.left, 73.54, delta=0.02)
        self.assertAlmostEqual(a.top, 65.67, delta=0.02)

    def test_scaling_with_rotation_and_anchor_y_original(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_y = 1
        a.angle = 60
        self.assertAlmostEqual(a.width, 112.67, delta=0.02)
        self.assertAlmostEqual(a.height, 103.16, delta=0.02)
        self.assertAlmostEqual(a.left, 3.83, delta=0.02)
        self.assertAlmostEqual(a.top, 25.42, delta=0.02)

    def test_scaling_with_rotation_and_anchor_y_up(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_y = 2.5
        a.angle = 60
        self.assertAlmostEqual(a.width, 232.19, delta=0.02)
        self.assertAlmostEqual(a.height, 172.16, delta=0.02)
        self.assertAlmostEqual(a.left, -115.69, delta=0.02)
        self.assertAlmostEqual(a.top, -43.58, delta=0.02)

    def test_scaling_with_rotation_and_anchor_y_down(self):
        a = Actor("alien", (100, 100), anchor=("center", "bottom"))
        a.scale_y = 0.25
        a.angle = 60
        self.assertAlmostEqual(a.width, 52.92, delta=0.02)
        self.assertAlmostEqual(a.height, 68.66, delta=0.02)
        self.assertAlmostEqual(a.left, 63.58, delta=0.02)
        self.assertAlmostEqual(a.top, 59.92, delta=0.02)

    def test_opacity_default(self):
        """Ensure opacity is initially set to its default value."""
        a = Actor('alien')

        self.assertEqual(a.opacity, 1.0)

    def test_opacity_value(self):
        """Ensure opacity gives the value it was set to."""
        a = Actor('alien')
        expected_opacity = 0.54321

        a.opacity = expected_opacity

        self.assertEqual(a.opacity, expected_opacity)

    def test_opacity_min_boundry(self):
        """Ensure opacity is not set below minimum allowable level."""
        a = Actor('alien')

        a.opacity = -0.1

        self.assertEqual(a.opacity, 0.0)

    def test_opacity_max_boundry(self):
        """Ensure opacity is not set above maximum allowable level."""
        a = Actor('alien')

        a.opacity = 1.1

        self.assertEqual(a.opacity, 1.0)

    def test_dir_correct(self):
        """Everything returned by dir should be indexable as an attribute."""
        a = Actor("alien")
        for attribute in dir(a):
            a.__getattr__(attribute)

    # Since the tests don't create the proper screen, it must be mocked for
    # these test functions.
    @patch("pgturbo.actor.game.screen.get_height")
    @patch("pgturbo.actor.game.screen.get_width")
    @patch("pgturbo.actor.game.screen")
    def test_onscreen(self, mock_screen, mock_get_width, mock_get_height):
        """We can check if the Actor is in the screen bounds."""
        mock_get_width.return_value = 200
        mock_get_height.return_value = 100
        a = Actor("alien", (10, 10))
        self.assertTrue(a.is_onscreen())

    @patch("pgturbo.actor.game.screen.get_height")
    @patch("pgturbo.actor.game.screen.get_width")
    @patch("pgturbo.actor.game.screen")
    def test_not_onscreen(self, mock_screen, mock_get_width, mock_get_height):
        """We can check if the Actor is not within the screen bounds."""
        a = Actor("alien", (10, 1000))
        mock_get_width.return_value = 200
        mock_get_height.return_value = 100
        self.assertFalse(a.is_onscreen())

    def test_move_to_angle(self):
        """Ensure moving towards an arbitrary angle works."""
        # We set the anchor to topleft for easier math.
        a = Actor("alien", anchor=("left", "top"))
        # Pythagoras for necessary distance to reach the target point.
        distance = (50**2 + 50**2)**0.5
        a.move_towards_angle(-45, distance)
        # After moving we always have to round to match the int target point.
        # In actual games, having the position be floats is no problem.
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_to_point(self):
        """Ensure moving towards a point works."""
        a = Actor("alien", anchor=("left", "top"))
        position = (50, 50)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (25, 25))

    def test_move_to_point_no_overshoot(self):
        """Ensure moving towards point won't overshoot if distance to target
        is smaller than the given distance to move."""
        a = Actor("alien", anchor=("left", "top"))
        position = (10, 10)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (10, 10))

    def test_move_to_point_with_overshoot(self):
        """Ensure position overshoots correctly if given the parameter."""
        a = Actor("alien", anchor=("left", "top"))
        position = (10, 10)
        distance = ((50**2 + 50**2)**0.5)/2
        a.move_towards_point(position, distance, overshoot=True)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (25, 25))

    def test_move_forward(self):
        """Test whether moving forward by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = -45
        distance = (50**2 + 50**2)**0.5
        a.move_forward(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_backward(self):
        """Test whether moving backwards by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = 135
        distance = (50**2 + 50**2)**0.5
        a.move_backward(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_left(self):
        """Test whether moving left by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = -135
        distance = (50**2 + 50**2)**0.5
        a.move_left(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_move_right(self):
        """Test whether moving right by the actor angle works."""
        a = Actor("alien", anchor=("left", "top"))
        a.angle = 45
        distance = (50**2 + 50**2)**0.5
        a.move_right(distance)
        a.pos = (round(a.x), round(a.y))
        self.assertEqual(a.pos, (50, 50))

    def test_actor_square(self):
        """The square image is created correctly and the result is a valid
        actor."""
        square = Actor.Rectangle(10, 10, "red")
        name = "__SHAPE_RECTANGLE__10x10_red"
        self.assertIn((name, (), ()), images._cache)
        surf = images.load(name)
        width, height = surf.get_size()
        self.assertEqual(width, 10)
        self.assertEqual(height, 10)
        self.assertEqual(
            surf.get_at((width//2, height//2)), (255, 0, 0, 255)
        )
        self.assertEqual(type(square), Actor)

    def test_actor_rectangle(self):
        """The rectangle image is created correctly and the result is a valid
        actor."""
        square = Actor.Rectangle(10, 5, "green")
        name = "__SHAPE_RECTANGLE__10x5_green"
        self.assertIn((name, (), ()), images._cache)
        surf = images.load(name)
        width, height = surf.get_size()
        self.assertEqual(width, 10)
        self.assertEqual(height, 5)
        self.assertEqual(
            surf.get_at((width//2, height//2)), (0, 255, 0, 255)
        )
        self.assertEqual(type(square), Actor)

    def test_actor_circle(self):
        """The circular image is created correctly and the result is a valid
        actor."""
        square = Actor.Ellipse(5, 5, "blue")
        name = "__SHAPE_ELLIPSE__5x5_blue"
        self.assertIn((name, (), ()), images._cache)
        surf = images.load(name)
        width, height = surf.get_size()
        self.assertEqual(width, 5)
        self.assertEqual(height, 5)
        self.assertEqual(
            surf.get_at((width//2, height//2)), (0, 0, 255, 255)
        )
        self.assertEqual(type(square), Actor)

    def test_actor_ellipse(self):
        """The elliptical image is created correctly and the result is a valid
        actor."""
        square = Actor.Ellipse(5, 10, "yellow")
        name = "__SHAPE_ELLIPSE__5x10_yellow"
        self.assertIn((name, (), ()), images._cache)
        surf = images.load(name)
        width, height = surf.get_size()
        self.assertEqual(width, 5)
        self.assertEqual(height, 10)
        self.assertEqual(
            surf.get_at((width//2, height//2)), (255, 255, 0, 255)
        )
        self.assertEqual(type(square), Actor)

    def test_actor_triangle(self):
        """The triangular image is created correctly and the result is a valid
        actor."""
        square = Actor.Triangle(15, 15, "fuchsia")
        name = "__SHAPE_TRIANGLE__15x15_fuchsia"
        self.assertIn((name, (), ()), images._cache)
        surf = images.load(name)
        width, height = surf.get_size()
        self.assertEqual(width, 15)
        self.assertEqual(height, 15)
        self.assertEqual(
            surf.get_at((width//2, height//2)), (255, 0, 255, 255)
        )
        self.assertEqual(type(square), Actor)

    def test_velocity_starts_at_Zero(self):
        """An Actors velocity starts at zero in both axes."""
        a = Actor("alien")
        self.assertEqual(a.vel, (0, 0))

    def test_velocity_components(self):
        """We can use the Actors velocity by individual components."""
        a = Actor("alien")
        a.vx = 15
        a.vy = -5
        self.assertEqual(a.vx, 15)
        self.assertEqual(a.vy, -5)
        self.assertEqual(a.vel, (15, -5))

    def test_velocity_together(self):
        """We can use the Actors velocity as a tuple."""
        a = Actor("alien")
        a.vel = (15, -5)
        self.assertEqual(a.vx, 15)
        self.assertEqual(a.vy, -5)
        self.assertEqual(a.vel, (15, -5))

    def test_move_by_vel(self):
        """We can move an actor by its velocity."""
        a = Actor("alien", (10, 10))
        a.vel = (15, -5)
        a.move_by_vel()
        self.assertEqual(a.pos, (25, 5))

    def test_interception_velocity(self):
        """We can get a valid interception vector from a starting Actor to
        a moving target Actor."""
        a = Actor("alien", (0, 10))
        b = Actor("alien", (10, 0))
        b.vy = 5
        # Due to floating point inaccuracy, if we simply give 5 as the speed,
        # no intersection will be found even though it should be.
        a.vel = a.intercept_velocity(b, 5.0001)
        # For the same reason, the result must be rounded to compare.
        self.assertEqual((round(a.vx), round(a.vy)), (5, 0))

    def test_no_interception(self):
        """If no valid interception vector exists, None is returned."""
        a = Actor("alien", (0, 10))
        b = Actor("alien", (10, 0))
        b.vy = 5
        v = a.intercept_velocity(b, 1)
        self.assertIsNone(v)

    def test_mask_collision(self):
        """Collisions are detected with masks in use."""
        a1 = Actor("alien")
        # For some reason, this is necessary if actors are not drawn but
        # collisions should be checked.
        a1.pos = (0, 0)
        a2 = Actor("alien")
        a2.angle = 180
        # Since nothing is drawn, the surface has to be updated manually to
        # reflect rotation.
        a2._build_transformed_surf()
        # Collision is detected.
        self.assertIsNotNone(a1.collidemask(a2))

    def test_mask_no_collision(self):
        """Even if rects overlap, masks correctly report no collision if no
        pixels overlap."""
        a1 = Actor("alien")
        a1.pos = (0, 0)
        a2 = Actor("alien")
        a2.angle = 180
        a2._build_transformed_surf()
        a2.pos = (10, 87)
        # No collision is detected.
        self.assertIsNone(a1.collidemask(a2))
