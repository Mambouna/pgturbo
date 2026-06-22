import pygame
from math import radians, sin, cos, atan2, degrees, sqrt

from . import game
from . import loaders
from . import rect
from . import spellcheck
from .clock import ReadyTimerSystem
from .validation import validate_position_tuple, validate_limit_tuple
from .actor_animation import ActorAnimationSystem


ANCHORS = {
    'x': {
        'left': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'right': 1.0,
    },
    'y': {
        'top': 0.0,
        'center': 0.5,
        'middle': 0.5,
        'bottom': 1.0,
    }
}


def calculate_anchor(value, dim, total):
    if isinstance(value, str):
        try:
            return total * ANCHORS[dim][value]
        except KeyError:
            raise ValueError(
                '%r is not a valid %s-anchor name' % (value, dim)
            )
    return float(value)


# These are methods (of the same name) on pygame.Rect
SYMBOLIC_POSITIONS = set((
    "topleft", "bottomleft", "topright", "bottomright",
    "midtop", "midleft", "midbottom", "midright",
    "center",
))
SYMBOLIC_SIDES = set(("left", "right", "top", "bottom"))

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None

MAX_ALPHA = 255  # Based on pygame's max alpha.


def transform_anchor(ax, ay, w, h, angle, scale_x, scale_y):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

    sintheta = sin(theta)
    costheta = cos(theta)

    # Width and height of the original after scaling is applied.
    sw = w * scale_x
    sh = h * scale_y

    # Width and height of the bounding box after the scaled rect rotation.
    tw = abs(sw * costheta) + abs(sh * sintheta)
    th = abs(sw * sintheta) + abs(sh * costheta)

    # Offset of the anchor from the center taking scaling into account.
    cax = (ax - w * 0.5) * scale_x
    cay = (ay - h * 0.5) * scale_y

    # Rotated offset of the anchor from the center
    rax = cax * costheta - cay * sintheta
    ray = cax * sintheta + cay * costheta

    return (
        tw * 0.5 + rax,
        th * 0.5 + ray
    )


def _set_angle(actor, current_surface):
    if actor._angle % 360 == 0:
        # No changes required for default angle.
        return current_surface
    return pygame.transform.rotate(current_surface, actor._angle)


def _set_scale(actor, current_surface):
    if actor._scale_x == 1.0 and actor._scale_y == 1.0:
        return current_surface
    return pygame.transform.scale_by(current_surface,
                                     (actor._scale_x, actor._scale_y))


def _set_flip(actor, current_surface):
    if (not actor._flip_x) and (not actor._flip_y):
        return current_surface
    return pygame.transform.flip(current_surface, actor._flip_x, actor._flip_y)


def _set_opacity(actor, current_surface):
    alpha = int(actor.opacity * MAX_ALPHA + 0.5)  # +0.5 for rounding up.

    if alpha == MAX_ALPHA:
        # No changes required for fully opaque surfaces (corresponds to the
        # default opacity of the current_surface).
        return current_surface

    alpha_img = pygame.Surface(current_surface.get_size(), pygame.SRCALPHA)
    alpha_img.fill((255, 255, 255, alpha))
    alpha_img.blit(
        current_surface,
        (0, 0),
        special_flags=pygame.BLEND_RGBA_MULT
    )
    return alpha_img


class Actor:
    EXPECTED_INIT_KWARGS = SYMBOLIC_POSITIONS
    DELEGATED_ATTRIBUTES = [
        a for a in dir(rect.ZRect) if (not a.startswith("_")
                                       and a not in ("width", "height"))
    ]

    function_order = [_set_opacity, _set_scale, _set_flip, _set_angle]
    _anchor = _anchor_value = (0, 0)
    _scale_x = 1.0
    _scale_y = 1.0
    _flip_x = False
    _flip_y = False
    # TODO: Is this solution too ugly? Only needed to correct animation frame
    # offsets in _calc_anchor() when actor was flipped over the anchor.
    _flipped_x_over_anchor = False
    _flipped_y_over_anchor = False
    _angle = 0.0
    _opacity = 1.0

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        # Note if the surface to be displayed has changed.
        surf_changed = False
        if cache_len == 0:
            # If there is no cache and the actor is in an animation,
            # the last drawn surface is the animation image.
            if self._anim._current_animation:
                last = self._a_image
            # Otherwise, it's the static image.
            else:
                last = self._orig_surf
        # If there is a cache, it reflects the correct image either way.
        else:
            last = self._surface_cache[-1]
        for f in self.function_order[cache_len:]:
            surf_changed = True  # We note that we have to change the mask.
            new_surf = f(self, last)
            self._surface_cache.append(new_surf)
            last = new_surf
        # If the actor has a mask, it is updated.
        if self._mask and surf_changed:
            self._mask = pygame.mask.from_surface(self._surface_cache[-1])
        return self._surface_cache[-1]

    def __init__(self, image, pos=POS_TOPLEFT, anchor=ANCHOR_CENTER, **kwargs):
        self._handle_unexpected_kwargs(kwargs)

        self._surface_cache = []
        self.__dict__["_rect"] = rect.ZRect((0, 0), (0, 0))
        # Initialise it at (0, 0) for size (0, 0).
        # We'll move it to the right place and resize it later

        # If a value is provided for pos, check if it's a valid positional.
        # Only done here to not incur performance costs, though it could be
        # moved to the pos.setter for better coverage.
        if pos:
            validate_position_tuple(pos)

        # Initialize any actor with a new animation system. This needs to be
        # done here so all Actors don't share the same animation system.
        self._anim = ActorAnimationSystem()
        # Image variable to hold the currently displayed animation frame.
        # This image is separate from the static image so that falling back to
        # it is possible if something goes wrong with the animations.
        self._a_image = None

        # Object that allows actors to use the same kind of ready tracking as
        # clock has.
        self._ready_timer_system = ReadyTimerSystem()

        # Limits for actor movements if set by the user.
        self._left_limit = None
        self._right_limit = None
        self._top_limit = None
        self._bottom_limit = None

        self.image = image
        self._init_position(pos, anchor, **kwargs)
        self._vx = 0
        self._vy = 0

    def _clamp_value(self, value, lower_limit, upper_limit):
        if lower_limit and value < lower_limit:
            value = lower_limit
        elif upper_limit and value > upper_limit:
            value = upper_limit
        return value

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """Assign rect attributes to the underlying rect."""
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            # If we set a position, we set it first and then set it back
            # afterwards if the movement exceeded the set limits.
            if attr in SYMBOLIC_POSITIONS or attr in SYMBOLIC_SIDES:
                return_value = setattr(self._rect, attr, value)

                self._enforce_position_limits()

                return return_value

            return setattr(self._rect, attr, value)
        else:
            # Ensure data descriptors are set normally
            return object.__setattr__(self, attr, value)

    def __iter__(self):
        return iter(self._rect)

    def __repr__(self):
        return '<{} {!r} pos={!r}>'.format(
            type(self).__name__,
            self._image_name,
            self.pos
        )

    def __dir__(self):
        standard_attributes = [
            key
            for key in self.__dict__.keys()
            if not key.startswith("_")
        ]
        return standard_attributes + self.__class__.DELEGATED_ATTRIBUTES

    def _handle_unexpected_kwargs(self, kwargs):
        unexpected_kwargs = set(kwargs.keys()) - self.EXPECTED_INIT_KWARGS
        if not unexpected_kwargs:
            return

        typos, _ = spellcheck.compare(
            unexpected_kwargs, self.EXPECTED_INIT_KWARGS)
        for found, suggested in typos:
            raise TypeError(
                "Unexpected keyword argument '{}' (did you mean '{}'?)".format(
                    found, suggested))

    def _init_position(self, pos, anchor, **kwargs):
        if anchor is None:
            anchor = ("center", "center")
        self.anchor = anchor

        symbolic_pos_args = {
            k: kwargs[k] for k in kwargs if k in SYMBOLIC_POSITIONS}

        if not pos and not symbolic_pos_args:
            # No positional information given, use sensible top-left default
            self.topleft = (0, 0)
        elif pos and symbolic_pos_args:
            raise TypeError(
                "'pos' argument cannot be mixed with 'topleft', "
                "'topright' etc. argument."
            )
        elif pos:
            self.pos = pos
        else:
            self._set_symbolic_pos(symbolic_pos_args)

    def _set_symbolic_pos(self, symbolic_pos_dict):
        if len(symbolic_pos_dict) == 0:
            raise TypeError(
                "No position-setting keyword arguments ('topleft', "
                "'topright' etc) found."
            )
        if len(symbolic_pos_dict) > 1:
            raise TypeError(
                "Only one 'topleft', 'topright' etc. argument is allowed."
            )

        setter_name, position = symbolic_pos_dict.popitem()
        setattr(self, setter_name, position)

    def _update_transform(self, function):
        if function in self.function_order:
            i = self.function_order.index(function)
            del self._surface_cache[i:]
        else:
            raise IndexError(
                "function {!r} does not have a registered order."
                "".format(function))

    @classmethod
    def _make_shape_image(self, kind, width, height, color):
        """Creates a new shape image and loads it into resources. If an image
        of the exact parameters already exists, creation is not repeated."""
        # Create image name and resource cache key from parameters.
        name = kind + str(width) + "x" + str(height) + "_" + str(color)
        key = (name, (), ())
        # Return without costly image creation if image already exists.
        if key in loaders.images._cache:
            return name
        # If a color was given as a string, spellcheck it.
        if isinstance(color, str):
            spellcheck.check_color_name(color)
        # Creates the image with transparency (for non-rects) and fills them
        # with the appropriate shape.
        s = pygame.Surface((width, height), pygame.SRCALPHA)
        match kind:
            case "__SHAPE_ELLIPSE__":
                pygame.draw.ellipse(s, color,
                                    pygame.Rect((0, 0), (width, height)))
            case "__SHAPE_TRIANGLE__":
                pygame.draw.polygon(s, color,
                                    ((0, 0), (width, height / 2), (0, height)))
            case _:
                s.fill(color)
        # Saves the created image in the resource cache for use. This ensures
        # smooth interoperability with the normal Actor construction.
        loaders.images._cache[key] = s
        # Returns the name for use in the Actor construction.
        return name

    @classmethod
    def Rectangle(self, width, height, color, pos=POS_TOPLEFT,
                  anchor=ANCHOR_CENTER, **kwargs):
        """Creates an actor with a rectangle as an image."""
        name = self._make_shape_image("__SHAPE_RECTANGLE__", width, height,
                                      color)
        return Actor(name, pos, anchor, **kwargs)

    @classmethod
    def Ellipse(self, width, height, color, pos=POS_TOPLEFT,
                anchor=ANCHOR_CENTER, **kwargs):
        """Creates an actor with an ellipse as an image."""
        name = self._make_shape_image("__SHAPE_ELLIPSE__", width, height,
                                      color)
        return Actor(name, pos, anchor, **kwargs)

    @classmethod
    def Triangle(self, width, height, color, pos=POS_TOPLEFT,
                 anchor=ANCHOR_CENTER, **kwargs):
        """Creates an actor with a triangle as an image."""
        name = self._make_shape_image("__SHAPE_TRIANGLE__", width, height,
                                      color)
        return Actor(name, pos, anchor, **kwargs)

    @property
    def anchor(self):
        return self._anchor_value

    @anchor.setter
    def anchor(self, val):
        self._anchor_value = val
        self._calc_anchor()

    def _calc_anchor(self):
        # Values are "left", "center", etc.
        ax, ay = self._anchor_value
        # We always use the base image size here since animation frame offsets
        # are entered in relation to it.
        ow, oh = self._orig_surf.get_size()
        # calculate_anchor() returns the x and y coords
        # of the anchor in relation to the topleft of
        # the image. (e.g. if img. is 200x150 and anchor
        # is centered, ax and ay would be 100 and 75
        # after the operation)
        ax = calculate_anchor(ax, 'x', ow)
        ay = calculate_anchor(ay, 'y', oh)
        # If an animation is playing, change the anchor coordinates
        # based on animation frame offsets.
        if self._anim._current_animation:
            # Quick access to the current animation.
            anim = self._anim._current_animation
            # Offsets for the current frame of the running animation.
            offset_x = anim.offset_x
            offset_y = anim.offset_y
            # If the actor was flipped on an axis, we need to calculate new
            # offsets based on the original ones and the difference in image
            # sizes of the base image and the current animation frame.
            if self._flipped_x_over_anchor:
                offset_x = -1 * offset_x + ow - anim.frame.width
            if self._flipped_y_over_anchor:
                offset_y = -1 * offset_y + oh - anim.frame.height
            # For some reason this works correctly with - instead of + ...
            ax -= offset_x
            ay -= offset_y
        # The untransformed anchor assumes the image isn't
        # rotated. If it is, the anchor position has to be
        # recalculated because the rotated image has a different
        # size and topleft, so the position of the anchor
        # in relation to topleft must also change.
        self._untransformed_anchor = ax, ay
        if self._angle == 0.0:
            u_anchor = self._untransformed_anchor
            self._anchor = (u_anchor[0] * self._scale_x,
                            u_anchor[1] * self._scale_y)
        else:
            self._anchor = transform_anchor(ax, ay, ow, oh, self._angle,
                                            self._scale_x, self._scale_y)

    # Calculates the new width and height of the actors bounding box and then
    # recalculates the proper anchor position for the new dimensions, resetting
    # the position afterwards to realign the image properly.
    def _transform(self):
        if self._anim._current_animation:
            w, h = self._a_image.get_size()
        else:
            w, h = self._orig_surf.get_size()
        # Scale the dimensions of the original surface.
        sw = w * self._scale_x
        sh = h * self._scale_y

        ra = radians(self._angle)
        sin_a = sin(ra)
        cos_a = cos(ra)
        # Get the dimensions of the new bounding box after scale and rotation.
        self._width = abs(sw * cos_a) + abs(sh * sin_a)
        # We need to set the internal rect as well when total dimensions
        # change as width and height are now properties on actor as well.
        setattr(self._rect, "width", self._width)
        self._height = abs(sw * sin_a) + abs(sh * cos_a)
        setattr(self._rect, "height", self._height)
        # Anchor coordinates without any scaling or rotating done.
        ax, ay = self._untransformed_anchor
        # Remember the current position.
        p = self.pos
        # Calculate the actual anchor offset for the new dimensions.
        self._anchor = transform_anchor(ax, ay, w, h, self._angle,
                                        self._scale_x, self._scale_y)
        # After anchor has changed, we set pos again to calculate the new
        # topleft position with the new anchor values.
        self.pos = p

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        # Keeps the angle between 0 and 359 degrees
        angle = angle % 360
        if angle == self._angle:
            return
        self._angle = angle
        self._transform()
        self._update_transform(_set_angle)

    @property
    def scale(self):
        return (self._scale_x, self._scale_y)

    @scale.setter
    def scale(self, value):
        if not isinstance(value, bool) and isinstance(value, (int, float)):
            if value == self._scale_x and value == self._scale_y:
                return
            self._scale_x = value
            self._scale_y = value
        else:
            try:
                sx, sy = value
                if sx == self._scale_x and sy == self._scale_y:
                    return
                self._scale_x = sx
                self._scale_y = sy
            except TypeError:
                raise TypeError("Setting 'scale' for an actor can be done with"
                                " a single integer or float value or a tuple "
                                "of two numbers, not a " + str(type(value))
                                + ".")
        self._transform()
        self._update_transform(_set_scale)

    @property
    def scale_x(self):
        return self._scale_x

    @scale_x.setter
    def scale_x(self, value):
        if value == self._scale_x:
            return
        self._scale_x = value
        self._transform()
        self._update_transform(_set_scale)

    @property
    def scale_y(self):
        return self._scale_y

    @scale_y.setter
    def scale_y(self, value):
        if value == self._scale_y:
            return
        self._scale_y = value
        self._transform()
        self._update_transform(_set_scale)

    @property
    def flip_x(self):
        return self._flip_x

    @flip_x.setter
    def flip_x(self, value):
        if value == self._flip_x:
            return
        self._flip_x = value
        self._update_transform(_set_flip)

    @property
    def flip_y(self):
        return self._flip_y

    @flip_y.setter
    def flip_y(self, value):
        if value == self._flip_y:
            return
        self._flip_y = value
        self._update_transform(_set_flip)

    @property
    def opacity(self):
        """Get/set the current opacity value.

        The allowable range for opacity is any number between and including
        0.0 and 1.0. Values outside of this will be clamped to the range.

        * 0.0 makes the image completely transparent (i.e. invisible).
        * 1.0 makes the image completely opaque (i.e. fully viewable).

        Values between 0.0 and 1.0 will give varying levels of transparency.
        """
        return self._opacity

    @opacity.setter
    def opacity(self, opacity):
        # Clamp the opacity to the allowable range.
        self._opacity = min(1.0, max(0.0, opacity))
        self._update_transform(_set_opacity)

    def _check_limit_sizes(self):
        # If there are limits on both sides of an axis, check that the actor
        # can actually fit inside them.
        if ((self._right_limit and self._left_limit
                and self._right_limit - self._left_limit < self.width)
                or (self._top_limit and self._bottom_limit
                    and self._bottom_limit - self._top_limit < self.height)):
            raise ValueError("Movement limit conflict detected. Upper limit "
                             "bounds must be larger than lower ones and "
                             "between them must be enough room for the actor.")

    def _enforce_position_limits(self):
        if self._left_limit and self.left < self._left_limit:
            self.left = self._left_limit
        elif self._right_limit and self.right > self._right_limit:
            self.right = self._right_limit
        if self._top_limit and self.top < self._top_limit:
            self.top = self._top_limit
        elif self._bottom_limit and self.bottom > self._bottom_limit:
            self.bottom = self._bottom_limit

    @property
    def x_limits(self):
        return (self._left_limit, self._right_limit)

    @x_limits.setter
    def x_limits(self, value):
        validate_limit_tuple(value)
        self._left_limit = value[0]
        self._right_limit = value[1]
        self._check_limit_sizes()
        self._enforce_position_limits()
    
    def _set_single_limit(self, limit, value):
        """Helper function to reduce duplicate code."""
        if value is None or isinstance(value, (int, float)):
            setattr(self, limit, value)
            self._check_limit_sizes()
            self._enforce_position_limits()
        else:
            raise TypeError("Limit value must be of type None, int or float, "
                            "not {}.".format(type(value)))

    @property
    def left_limit(self):
        return self._left_limit

    @left_limit.setter
    def left_limit(self, value):
        self._set_single_limit("_left_limit", value)

    @property
    def right_limit(self):
        return self._right_limit

    @right_limit.setter
    def right_limit(self, value):
        self._set_single_limit("_right_limit", value)

    @property
    def y_limits(self):
        return (self._top_limit, self._bottom_limit)

    @y_limits.setter
    def y_limits(self, value):
        validate_limit_tuple(value)
        self._top_limit = value[0]
        self._bottom_limit = value[1]
        self._check_limit_sizes()
        self._enforce_position_limits()

    @property
    def top_limit(self):
        return self._top_limit

    @top_limit.setter
    def top_limit(self, value):
        self._set_single_limit("_top_limit", value)

    @property
    def bottom_limit(self):
        return self._bottom_limit

    @bottom_limit.setter
    def bottom_limit(self, value):
        self._set_single_limit("_top_limit", value)

    @property
    def pos(self):
        px, py = self.topleft
        ax, ay = self._anchor
        return px + ax, py + ay

    @pos.setter
    def pos(self, pos):
        px, py = pos
        ax, ay = self._anchor
        self.topleft = px - ax, py - ay

    @property
    def width(self):
        return self._orig_surf.width * self._scale_x

    @width.setter
    def width(self, value):
        if value < 0:
            raise ValueError("Width cannot be set to negative values.")
        self.scale_x = value / self._orig_surf.width

    @property
    def height(self):
        return self._orig_surf.height * self._scale_y

    @height.setter
    def height(self, value):
        if value < 0:
            raise ValueError("Height cannot be set to negative values.")
        self.scale_y = value / self._orig_surf.height

    @property
    def bounding_width(self):
        return self._width

    @property
    def bounding_height(self):
        return self._height

    def rect(self):
        """Get a copy of the actor's rect object.

        This allows Actors to duck-type like rects in Pygame rect operations,
        and is not expected to be used in user code.
        """
        return self._rect.copy()

    @property
    def x(self):
        ax = self._anchor[0]
        return self.left + ax

    @x.setter
    def x(self, px):
        self.left = px - self._anchor[0]

    @property
    def y(self):
        ay = self._anchor[1]
        return self.top + ay

    @y.setter
    def y(self, py):
        self.top = py - self._anchor[1]

    @property
    def vx(self):
        return self._vx

    @vx.setter
    def vx(self, value):
        if not isinstance(value, bool) and isinstance(value, (int, float)):
            self._vx = value
        else:
            raise TypeError("Velocity components must be integers or floats,"
                            " not {}.".format(type(value)))

    @property
    def vy(self):
        return self._vy

    @vy.setter
    def vy(self, value):
        if not isinstance(value, bool) and isinstance(value, (int, float)):
            self._vy = value
        else:
            raise TypeError("Velocity components must be integers or floats,"
                            " not {}.".format(type(value)))

    @property
    def vel(self):
        return (self._vx, self._vy)

    @vel.setter
    def vel(self, value):
        if isinstance(value, tuple) and len(value) == 2:
            self._vx = value[0]
            self._vy = value[1]
        else:
            raise TypeError("Velocity must be set to a tuple of two numbers,"
                            " not {}.".format(value))

    @property
    def image(self):
        return self._image_name

    @image.setter
    def image(self, image):
        self._image_name = image
        self._orig_surf = loaders.images.load(image)
        self._surface_cache.clear()  # Clear out old image's cache.
        self._mask = None
        # NOTE: This does quite a few things multiple times with existing
        # functions. If there's ever a performance drop from this, just
        # split up the called functions into multiple smaller ones and
        # make sure position sets, dimension calculations and anchor
        # transforms are all done just once.
        p = self.pos
        self._calc_anchor()
        self._transform()
        self.pos = p

    @property
    def anim(self):
        return self._anim

    def _manage_frame_advancement(self):
        # If an animation is running and it has advanced a frame, the
        # actors new animation image needs to be fetched.
        # TODO: Solve this differently? An animation could directly
        # change actor._a_image when it runs _next_frame, would that
        # be better?
        if (self._anim._current_animation
                and self._anim._current_animation._new_frame):
            # Index of the right frame.
            i = self._anim._current_animation._frame_index
            # Setting the actors animation image to the right frame.
            self._a_image = self._anim._current_animation.frames[i]
            # Updating the animation status that the frame has been udpated.
            self._anim._current_animation.new_frame = False
            # Clear the surface cache for the new image.
            self._surface_cache.clear()
            # Update actor position to incorporate frame offsets.
            # TODO: Same note as above? Refactor to avoid duplicating many
            # calls?
            p = self.pos
            self._calc_anchor()
            self._transform()
            self.pos = p
        # Otherwise, if no animation is running but there still is an
        # animation image, it is deleted and the surface cache cleared
        # so that the static image is displayed again.
        elif (not self._anim._current_animation and self._a_image
              and not self._anim.paused):
            self._a_image = None
            self._surface_cache.clear()

    def draw(self):
        # Updates _a_image and other necessary tracking if new animation
        # frames are needed or removes it if it's not needed.
        self._manage_frame_advancement()
        s = self._build_transformed_surf()
        game.screen.blit(s, self.topleft)

    def angle_to(self, target):
        """Return the angle from this actors position to target, in degrees."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = myy - ty   # y axis is inverted from mathematical y in Pygame
        return degrees(atan2(dy, dx))

    def move_towards_angle(self, angle, distance):
        """Move the actor a certain distance towards a certain
        angle. Does not change the actors angle property.
        All other functions for movement around angles use
        this basic function."""
        # Modulo of angle is there to prevent invalid angles leading to
        # incorrect movement because of wrong radian values messing up
        # the calculation.
        rad_angle = radians(angle % 360)
        move_x = cos(rad_angle) * distance
        move_y = -1 * sin(rad_angle) * distance
        self.x += move_x
        self.y += move_y

    def move_towards_point(self, point, distance, overshoot=False):
        """Figure out the angle to the given point and then
        move the actor towards it by the given distance."""
        angle = self.angle_to(point)
        if overshoot:
            self.move_towards_angle(angle, distance)
        else:
            m_distance = min(self.distance_to(point), distance)
            self.move_towards_angle(angle, m_distance)

    def move_forward(self, distance):
        """Move the actor in the direction it is facing."""
        self.move_towards_angle(self._angle, distance)

    def move_backward(self, distance):
        """Move the actor in the opposite direction of its
        heading."""
        angle = (self._angle + 180) % 360
        self.move_towards_angle(angle, distance)

    def move_left(self, distance):
        """Move the actor left based on its heading. "Strafing"
        left."""
        angle = (self._angle + 90) % 360
        self.move_towards_angle(angle, distance)

    def move_right(self, distance):
        """Move the actor right based on its heading. "Strafing"
        right."""
        angle = (self._angle - 90) % 360
        self.move_towards_angle(angle, distance)

    def distance_to(self, target):
        """Return the distance from this actor's pos to target, in pixels."""
        if isinstance(target, Actor):
            tx, ty = target.pos
        else:
            tx, ty = target
        myx, myy = self.pos
        dx = tx - myx
        dy = ty - myy
        return sqrt(dx * dx + dy * dy)

    def is_onscreen(self):
        """Returns whether the Actor is within the screen bounds or not."""
        return not (self.right < 0 or self.left > game.screen.get_width() or
                    self.bottom < 0 or self.top > game.screen.get_height())

    def move_by_vel(self, scale=1.0):
        """Moves the position of the actor by its velocity. scale can be set
        to slow down or quicken the movement, for example if the game's
        timescale is not 1."""
        if isinstance(scale, bool) or not isinstance(scale, (int, float)):
            raise TypeError("The velocity scaling must be of type integer or"
                            " float, not {}.".format(type(scale)))
        self.x += self._vx * scale
        self.y += self._vy * scale

    def intercept_velocity(self, target, speed):
        """Returns a vector with the given magnitude (movement speed) that will
        intercept the target actor or point if it keeps moving along the same
        direction."""
        # Convert values to pygame vectors for easier math.
        self_pos = pygame.math.Vector2(self.pos)
        target_pos = pygame.math.Vector2(target.pos)
        target_vel = pygame.math.Vector2(target.vel)

        totarget_vec = target_pos - self_pos

        a = target_vel.dot(target_vel) - speed**2
        b = 2 * target_vel.dot(totarget_vec)
        c = totarget_vec.dot(totarget_vec)

        try:
            p = -b / (2 * a)
            q = sqrt((b * b) - 4 * a * c) / (2 * a)
        except Exception:
            return None

        time1 = p - q
        time2 = p + q

        # Choose the correct intercept option.
        if time1 > time2 and time2 > 0:
            intercept_time = time2
        else:
            intercept_time = time1

        intercept_point = target_pos + target_vel * intercept_time
        intercept_vec = (intercept_point - self_pos).normalize() * speed

        # Since Vector2s aren't used in pgturbo directly, return as a tuple.
        return tuple(intercept_vec)

    def _store_and_wipe_scale_and_rotation(self):
        """Stores and then defaults scaling and rotation to allow other
        operations to happen correctly."""
        self._stored_scale_rotation_state = (self._scale_x, self._scale_y,
                                             self._angle)
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.angle = 0

    def _restore_scale_and_rotation_from_store(self):
        """Sets scaling and rotation from the stored values of the last
        function."""
        self.scale_x = self._stored_scale_rotation_state[0]
        self.scale_y = self._stored_scale_rotation_state[1]
        self.angle = self._stored_scale_rotation_state[2]

    def flip_x_over_anchor(self):
        """Flip the actor image and move it so that the resulting image is
        mirrored across the anchor position along the X axis."""
        # We default scaling and rotation to make the flipping easier.
        self._store_and_wipe_scale_and_rotation()
        # Flip the actor image
        self.flip_x = not self._flip_x
        # Remeber the flip state being over the axis for animation frame
        # offset adjustment.
        self._flipped_x_over_anchor = not self._flipped_x_over_anchor
        # Remember the current position
        p = self.pos
        current_anchor_x, current_anchor_y = self.anchor
        # If anchor is set to string values, we also make the new anchor
        # based on string values.
        if isinstance(current_anchor_x, str):
            match current_anchor_x:
                case "left":
                    new_anchor_x = "right"
                case "right":
                    new_anchor_x = "left"
                case _:
                    new_anchor_x = "center"
        # Otherwise we just calculate the new anchor position.
        else:
            new_anchor_x = abs(current_anchor_x - self._width)
        # Set the new anchor position (this moves the pos value of the actor).
        self.anchor = (new_anchor_x, current_anchor_y)
        # By setting pos to what we remembered before we move the image
        # so it appears mirrored afterwards.
        self.pos = p
        # Then we restore all the saved values for scaling and rotation.
        self._restore_scale_and_rotation_from_store()

    def flip_y_over_anchor(self):
        """Flip the actor image and move it so that the resulting image is
        mirrored across the anchor position along the Y axis."""
        self._store_and_wipe_scale_and_rotation()
        self.flip_y = not self._flip_y
        self._flipped_y_over_anchor = not self._flipped_y_over_anchor
        p = self.pos
        current_anchor_x, current_anchor_y = self.anchor
        if isinstance(current_anchor_y, str):
            match current_anchor_y:
                case "top":
                    new_anchor_y = "bottom"
                case "bottom":
                    new_anchor_y = "top"
                case _:
                    new_anchor_y = "center"
        else:
            new_anchor_y = abs(current_anchor_y - self._height)
        self.anchor = (current_anchor_x, new_anchor_y)
        self.pos = p
        self._restore_scale_and_rotation_from_store()

    def _create_mask(self):
        """Gives the actor a mask from the surface that is displayed."""
        if not self._surface_cache:
            self._mask = pygame.mask.from_surface(self._orig_surf)
        else:
            self._mask = pygame.mask.from_surface(self._surface_cache[-1])

    def collidemask(self, target):
        """Returns True if the actor's mask is colliding with the targets'.
        Masks are only created and checked when necessary."""
        # Check if the target is an actor and thus suitable.
        if not isinstance(target, Actor):
            raise TypeError("collidemask() can only be used with other actors,"
                            "not with a value of type '{}'."
                            .format(type(target)))

        # If the rects don't collide, exit early.
        if not self.colliderect(target):
            return False

        # Create masks that are not yet present.
        if not self._mask:
            self._create_mask()
        if not target._mask:
            target._create_mask()

        # Calculate the positional offsets of both actors.
        x_offset = int(target.left - self.left)
        y_offset = int(target.top - self.top)

        # Check for pixel perfect collision
        return self._mask.overlap(target._mask, (x_offset, y_offset))

    def unload_image(self):
        loaders.images.unload(self._image_name)

    def track_ready(self, *args):
        """The following methods all simply pass on calls to the ready timer
        system. This is so the calls can be made to clock directly."""
        self._ready_timer_system.track_ready(*args)

    def is_ready(self, name):
        return self._ready_timer_system.is_ready(name)

    get_ready = is_ready

    def get_ready_timeout(self, name):
        return self._ready_timer_system.get_ready_timeout(name)

    def timeout_ready(self, name, time=None, absolute=False):
        self._ready_timer_system.timeout_ready(name, time, absolute)

    def set_ready(self, name, value):
        self._ready_timer_system.set_ready(name, value)

    def set_ready_timeout(self, name, value):
        self._ready_timer_system.set_ready_timeout(name, value)

    def get_all_ready(self):
        return self._ready_timer_system.get_all_ready()
