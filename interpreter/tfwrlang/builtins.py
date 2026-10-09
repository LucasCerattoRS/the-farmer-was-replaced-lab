"""The game verbs, layered on `world.py` — cites `mechanics/measured-numbers.md` for every tick
cost and `api/reference.md` for every signature.

Each verb charges the exact tick cost from the ✅ **sourced** table on
`mechanics/measured-numbers.md` (transcribed from the canonical `builtins.py` the game ships).
The two-price group — `move` / `harvest` / `plant` — costs **200 on success, 1 otherwise**,
which is the reason a guarded `if can_move(d): move(d)` is not automatically cheaper than a bare
`move(d)`; that subtlety is modelled here, not glossed over.

Anything gated on an unmeasured number (grow time, pumpkin death, sunflower petals, harvest
yield) is delegated to the injected models on the `World`, whose defaults raise `Unspecified`.

**Drones are deliberately absent.** `spawn_drone` / `wait_for` / `has_finished` are refused via
`Unspecified('drone-scheduling')`: inter-drone ordering is the least documented part of the game
(drones.md), and a documented refusal is the honest deliverable, not an invented scheduler.
"""

from .errors import NotSupported, TfwrRuntimeError, Unspecified
from .interp import Namespace
from . import world as W


def install_constants(builtins):
    """Add the constant groups and bare directions a script reads by name."""
    builtins["Entities"] = Namespace("Entities", dict(W.ENTITIES))
    builtins["Items"] = Namespace("Items", dict(W.ITEMS))
    builtins["Grounds"] = Namespace("Grounds", {"Grassland": W.GRASSLAND, "Soil": W.SOIL})
    builtins["Direction"] = Namespace(
        "Direction", {"North": W.NORTH, "East": W.EAST, "South": W.SOUTH, "West": W.WEST}
    )
    # api/reference.md: North/East/South/West are also bare globals.
    builtins["North"] = W.NORTH
    builtins["East"] = W.EAST
    builtins["South"] = W.SOUTH
    builtins["West"] = W.WEST


def make_world_builtins(world):
    """Return the verb table for `world`, each entry charging its documented tick cost."""

    def charge(n):
        world.ticks += n

    def _require_direction(d, verb):
        if not isinstance(d, W.Direction):
            raise TfwrRuntimeError(f"{verb}() needs a Direction, got {type(d).__name__}")

    # -- free (0 ticks) ----------------------------------------------------------------------
    def get_tick_count():
        return float(world.ticks)  # the measuring instrument is free — a t1-t0 diff is exact

    def quick_print(*args):
        from .interp import tfwr_str
        world.output.append(" ".join(tfwr_str(a) for a in args))

    # -- sensing (1 tick) --------------------------------------------------------------------
    def get_pos_x():
        charge(1); return float(world.x)

    def get_pos_y():
        charge(1); return float(world.y)

    def get_world_size():
        charge(1); return float(world.size)

    def get_ground_type():
        charge(1); return world.tile().ground

    def get_entity_type():
        charge(1)
        t = world.tile()
        return t.entity  # a Symbol, or None

    def get_water():
        charge(1)
        return float(world.tile().water)  # 0..1 under the drone; no water source is modelled yet

    def num_items(item):
        charge(1)
        name = item.name if isinstance(item, W.Symbol) else item
        return world.num_items(name)

    def can_move(direction):
        _require_direction(direction, "can_move")
        charge(1)
        return True  # torus, no walls in this model — a move never fails

    def measure(direction=None):
        charge(1)
        t = world.tile()
        if t.entity is None:
            return None
        if t.entity.name == "Sunflower":
            # petal count — sunflower-petals is unmeasured, so this consults the injected model
            return float(world.models.petals())
        raise NotSupported(
            f"measure() is modelled for sunflowers only; {t.entity.name} needs world-specific "
            "setup (cactus size / maze coordinates are not modelled here)"
        )

    # -- till (200 ticks, always) ------------------------------------------------------------
    def till():
        charge(200)
        t = world.tile()
        t.ground = W.SOIL if t.ground == W.GRASSLAND else W.GRASSLAND
        return None

    # -- two-price group (200 on success, 1 otherwise) ---------------------------------------
    def move(direction):
        _require_direction(direction, "move")
        world.step(direction)
        charge(200)  # the move always succeeds in this model, so it is always the success price
        return True

    def plant(entity):
        if not (isinstance(entity, W.Symbol) and entity.group == "Entities"):
            raise TfwrRuntimeError("plant() needs an Entities.* value")
        t = world.tile()
        if t.entity is not None:
            charge(1)  # tile occupied — planting did not succeed
            return False
        t.entity = entity
        t.planted_tick = world.ticks
        t.dead = False
        charge(200)
        return True

    def _is_grown(t):
        elapsed = world.ticks - (t.planted_tick or 0)
        grown = bool(world.models.grow(t.entity.name, elapsed))
        if grown and t.entity.name == "Pumpkin" and not t.dead:
            # a pumpkin resolves life/death when it finishes growing (crops.md: ~1 in 5 dies)
            if world.models.death():
                t.entity = W.ENTITIES["Dead_Pumpkin"]
                t.dead = True
                return False
        return grown

    def can_harvest():
        charge(1)
        t = world.tile()
        if t.entity is None or t.entity.name == "Dead_Pumpkin":
            return False
        return _is_grown(t)

    def harvest():
        t = world.tile()
        if t.entity is None or t.entity.name == "Dead_Pumpkin" or not _is_grown(t):
            charge(1)  # nothing removed — the cheap price
            return False
        name = t.entity.name
        item = W.HARVEST_ITEM.get(name)
        if item is not None:
            world.credit(item, float(world.models.yield_(name, None)))
        t.entity = None
        t.planted_tick = None
        charge(200)
        return True

    # -- drones: refused, on purpose ---------------------------------------------------------
    def _drone_refused(*args, **kwargs):
        raise Unspecified(
            "drone-scheduling",
            "spawn_drone/wait_for/has_finished are not modelled — see world.py docstring",
        )

    return {
        "get_tick_count": get_tick_count,
        "quick_print": quick_print,
        "get_pos_x": get_pos_x,
        "get_pos_y": get_pos_y,
        "get_world_size": get_world_size,
        "get_ground_type": get_ground_type,
        "get_entity_type": get_entity_type,
        "get_water": get_water,
        "num_items": num_items,
        "can_move": can_move,
        "measure": measure,
        "till": till,
        "move": move,
        "plant": plant,
        "can_harvest": can_harvest,
        "harvest": harvest,
        "spawn_drone": _drone_refused,
        "wait_for": _drone_refused,
        "has_finished": _drone_refused,
    }


def make_world_interpreter(world=None, **interp_kwargs):
    """Build an `Interpreter` wired to a `World`: verbs + constants installed as built-ins.

    Returns `(interp, world)`. Everything unmeasured stays loud unless `world` was created with
    concrete models injected.
    """
    from .interp import Interpreter
    if world is None:
        world = W.World()
    extra = make_world_builtins(world)
    interp = Interpreter(extra_builtins=extra, **interp_kwargs)
    install_constants(interp.builtins)
    return interp, world
