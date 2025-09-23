import pygame
from math import radians, sin, cos, atan2, degrees, sqrt

from . import game
from . import loaders
from . import rect
from . import spellcheck


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

# Provides more meaningful default-arguments e.g. for display in IDEs etc.
POS_TOPLEFT = None
ANCHOR_CENTER = None

MAX_ALPHA = 255  # Based on pygame's max alpha.


def transform_anchor(ax, ay, w, h, angle):
    """Transform anchor based upon a rotation of a surface of size w x h."""
    theta = -radians(angle)

    sintheta = sin(theta)
    costheta = cos(theta)

    # Dims of the transformed rect
    tw = abs(w * costheta) + abs(h * sintheta)
    th = abs(w * sintheta) + abs(h * costheta)

    # Offset of the anchor from the center
    cax = ax - w * 0.5
    cay = ay - h * 0.5

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
        a for a in dir(rect.ZRect) if not a.startswith("_")
    ]

    function_order = [_set_opacity, _set_angle]
    _anchor = _anchor_value = (0, 0)
    _angle = 0.0
    _opacity = 1.0

    def _build_transformed_surf(self):
        cache_len = len(self._surface_cache)
        # Note if the surface to be displayed has changed.
        surf_changed = False
        if cache_len == 0:
            last = self._orig_surf
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

        self.image = image
        self._init_position(pos, anchor, **kwargs)
        self._vx = 0
        self._vy = 0

    def __getattr__(self, attr):
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
            return getattr(self._rect, attr)
        else:
            return object.__getattribute__(self, attr)

    def __setattr__(self, attr, value):
        """Assign rect attributes to the underlying rect."""
        if attr in self.__class__.DELEGATED_ATTRIBUTES:
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
        ax, ay = self._anchor_value
        ow, oh = self._orig_surf.get_size()
        ax = calculate_anchor(ax, 'x', ow)
        ay = calculate_anchor(ay, 'y', oh)
        self._untransformed_anchor = ax, ay
        if self._angle == 0.0:
            self._anchor = self._untransformed_anchor
        else:
            self._anchor = transform_anchor(ax, ay, ow, oh, self._angle)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):
        # Keeps the angle between 0 and 359 degrees
        angle = angle % 360
        self._angle = angle
        w, h = self._orig_surf.get_size()

        ra = radians(angle)
        sin_a = sin(ra)
        cos_a = cos(ra)
        self.height = abs(w * sin_a) + abs(h * cos_a)
        self.width = abs(w * cos_a) + abs(h * sin_a)
        ax, ay = self._untransformed_anchor
        p = self.pos
        self._anchor = transform_anchor(ax, ay, w, h, angle)
        self.pos = p
        self._update_transform(_set_angle)

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
        if isinstance(value, (int, float)):
            self._vx = value
        else:
            raise TypeError("Velocity components must be integers or floats,"
                            " not {}.".format(type(value)))

    @property
    def vy(self):
        return self._vy

    @vy.setter
    def vy(self, value):
        if isinstance(value, (int, float)):
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
        self._update_pos()

    def _update_pos(self):
        p = self.pos
        self.width, self.height = self._orig_surf.get_size()
        self._calc_anchor()
        self.pos = p

    def draw(self):
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
        if not isinstance(scale, (int, float)):
            raise TypeError(f"The velocity scaling must be of type integer or"
                             " float, not {type(scale)}.")
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
