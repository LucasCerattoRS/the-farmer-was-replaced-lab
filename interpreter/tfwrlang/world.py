"""The game world the built-in verbs act on — cites `mechanics/drones.md` (torus) and
`api/reference.md` (verb behaviour).

This is the deterministic, fully-documented core of the world: an N×N **torus** grid, per-tile
ground / entity / water, an inventory, and a tick counter. It models what the docs pin down and
nothing else.

Everything the official sources leave to an unmeasured number lives behind an **injected model**
that, by default, raises `Unspecified` the moment it is consulted — so a script cannot silently
run on a guessed grow time or death rate. The four such models are `grow`, `death`, `petals`,
`yield_` (see `ModelSet`). Inject a concrete one to make a script runnable; the honest default
refuses.

Constants (`Entities`, `Items`, `Grounds`, and the bare `North`/`East`/`South`/`West`
directions) live in `builtins.py` next to the verbs that consume them.
"""

from .errors import TfwrRuntimeError, Unspecified


# -- constants used as tile values -----------------------------------------------------------
class Symbol:
    """A named game constant such as `Entities.Grass` or `Grounds.Soil`. Equality is by
    (group, name), so `get_entity_type() == Entities.Grass` behaves as a script expects."""

    __slots__ = ("group", "name")

    def __init__(self, group, name):
        self.group = group
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Symbol) and (self.group, self.name) == (other.group, other.name)

    def __hash__(self):
        return hash((self.group, self.name))

    def __repr__(self):
        return f"{self.group}.{self.name}"


class Direction(Symbol):
    __slots__ = ("dx", "dy")

    def __init__(self, name, dx, dy):
        super().__init__("Direction", name)
        self.dx = dx
        self.dy = dy


NORTH = Direction("North", 0, 1)
SOUTH = Direction("South", 0, -1)
EAST = Direction("East", 1, 0)
WEST = Direction("West", -1, 0)

# Grounds (get_ground_type) — api/reference.md: exactly Grassland and Soil.
GRASSLAND = Symbol("Grounds", "Grassland")
SOIL = Symbol("Grounds", "Soil")

# Entities this world models. Names match `Entities.*` on api/reference.md; the world does not
# invent entities the docs don't list.
_ENTITY_NAMES = (
    "Grass", "Bush", "Tree", "Carrot", "Pumpkin", "Dead_Pumpkin",
    "Sunflower", "Cactus",
)
ENTITIES = {name: Symbol("Entities", name) for name in _ENTITY_NAMES}

# Items (num_items / use_item). Names match `Items.*` on api/reference.md.
_ITEM_NAMES = (
    "Hay", "Wood", "Carrot", "Pumpkin", "Cactus", "Bone", "Gold", "Power",
    "Water", "Fertilizer", "Weird_Substance", "Piggy",
)
ITEMS = {name: Symbol("Items", name) for name in _ITEM_NAMES}

# The documented product of harvesting each crop (crops.md / api/reference.md). This is the item
# *type*; the *quantity* is the `harvest-yield` hole — see errors.py — so it comes from the
# injected yield model, never from a number baked in here.
HARVEST_ITEM = {
    "Grass": "Hay",
    "Bush": "Wood",
    "Tree": "Wood",
    "Carrot": "Carrot",
    "Pumpkin": "Pumpkin",
    "Sunflower": "Power",
    "Cactus": "Cactus",
}


# -- injected models: the loud holes ---------------------------------------------------------
class _Unmeasured:
    """The default for every injected model. Consulting it raises `Unspecified`, which is the
    whole point: the game number behind it has never been measured (a Track 2 item), so the
    model refuses to proceed rather than invent one."""

    def __init__(self, topic):
        self.topic = topic

    def __call__(self, *args, **kwargs):
        raise Unspecified(self.topic)


class ModelSet:
    """The four unmeasured game numbers, each an injectable callable. Defaults refuse.

    * ``grow(entity, elapsed_ticks) -> bool`` — is a planted entity fully grown yet?
    * ``death() -> bool`` — did a pumpkin die on growing up?  (crops.md: "about 1 in 5")
    * ``petals() -> float`` — petal count of a freshly grown sunflower.
    * ``yield_(entity, size) -> float`` — how many items a harvest of `entity` credits.
    """

    def __init__(self, grow=None, death=None, petals=None, yield_=None):
        self.grow = grow or _Unmeasured("grow-time")
        self.death = death or _Unmeasured("pumpkin-death-rate")
        self.petals = petals or _Unmeasured("sunflower-petals")
        self.yield_ = yield_ or _Unmeasured("harvest-yield")


# -- the grid ---------------------------------------------------------------------------------
class Tile:
    __slots__ = ("ground", "entity", "water", "planted_tick", "dead")

    def __init__(self, ground):
        self.ground = ground
        self.entity = None          # a Symbol from Entities, or None
        self.water = 0.0            # 0..1
        self.planted_tick = None    # tick at which the current entity was planted
        self.dead = False           # a pumpkin that died on growing up


class World:
    """An N×N torus. The wrap is documented and is the top pitfall on drones.md, so it is modelled
    exactly: moving off one edge arrives on the opposite one. Coordinates are always taken mod N.

    `models` holds the four unmeasured game numbers; leave it at the default to keep every hole
    loud, or inject concrete callables to make a script runnable."""

    def __init__(self, size=8, models=None):
        if size < 3:
            raise TfwrRuntimeError("world size min is 3 (set_world_size documents this)")
        self.size = size
        self.grid = [[Tile(SOIL) for _ in range(size)] for _ in range(size)]
        self.x = 0
        self.y = 0
        self.inventory = {}         # item name -> float count
        self.ticks = 0
        self.output = []            # quick_print destination
        self.models = models or ModelSet()

    # -- geometry ----------------------------------------------------------------------------
    def tile(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        return self.grid[y % self.size][x % self.size]

    def step(self, direction):
        """Move one tile with torus wrap. Always succeeds in this model — there are no maze walls
        here, so `can_move` is always True and a move never fails."""
        self.x = (self.x + direction.dx) % self.size
        self.y = (self.y + direction.dy) % self.size
        return True

    # -- inventory ---------------------------------------------------------------------------
    def num_items(self, item_name):
        return self.inventory.get(item_name, 0.0)

    def credit(self, item_name, amount):
        self.inventory[item_name] = self.inventory.get(item_name, 0.0) + amount
