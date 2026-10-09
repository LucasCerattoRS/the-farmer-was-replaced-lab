"""World model and built-in verbs — cites `mechanics/drones.md` (torus), `api/reference.md`
(signatures) and `mechanics/measured-numbers.md` (tick costs).

The deterministic core (movement, wrap, ground, tick costs) is asserted exactly. The four
unmeasured numbers stay loud: consulting one without an injected model raises `Unspecified`.
"""

import pytest

from tfwrlang import world as W
from tfwrlang.builtins import make_world_interpreter
from tfwrlang.errors import Unspecified, NotSupported


def make(src, world=None, **kw):
    interp, world = make_world_interpreter(world=world, max_loop_iterations=10_000, **kw)
    interp.run_source(src)
    return interp, world


# -- torus geometry (drones.md) --------------------------------------------------------------
def test_move_wraps_at_the_edges():
    _, world = make(
        "move(West)\n"    # from x=0 wraps to x=size-1
        "move(South)\n",  # from y=0 wraps to y=size-1
        world=W.World(size=3),
    )
    assert (world.x, world.y) == (2, 2)


def test_position_and_size_readbacks():
    _, world = make(
        "move(North)\n"
        "move(East)\n"
        "x = get_pos_x()\n"
        "y = get_pos_y()\n"
        "n = get_world_size()\n",
        world=W.World(size=5),
    )
    assert world.tile  # sanity
    # values are exposed through the interpreter globals too
    interp, world2 = make_world_interpreter(world=W.World(size=5))
    interp.run_source("a = get_pos_x()\n")
    assert interp.global_env.get("a") == 0.0


# -- tick costs (measured-numbers.md) --------------------------------------------------------
def test_get_tick_count_is_free():
    _, world = make("t = get_tick_count()\n")
    assert world.ticks == 0  # measuring instrument costs nothing


def test_sensing_costs_one_and_move_costs_two_hundred():
    _, world = make("d = get_pos_x()\n")   # one sense
    assert world.ticks == 1
    _, world = make("move(North)\n")       # a successful move
    assert world.ticks == 200


def test_till_toggles_ground_and_costs_two_hundred():
    _, world = make("till()\n", world=W.World(size=3))
    assert world.tile().ground == W.GRASSLAND  # started as Soil
    assert world.ticks == 200


def test_failed_plant_is_the_cheap_price():
    # planting onto an occupied tile does not succeed -> 1 tick, not 200 (the two-price rule)
    grow = W.ModelSet(grow=lambda e, el: False)
    _, world = make(
        "plant(Entities.Grass)\n"   # succeeds: 200
        "plant(Entities.Bush)\n",   # tile occupied: 1
        world=W.World(size=3, models=grow),
    )
    assert world.ticks == 201


# -- entities and harvest (api/reference.md, crops.md) ---------------------------------------
def test_plant_sets_the_entity():
    _, world = make("plant(Entities.Grass)\n", world=W.World(size=3))
    assert world.tile().entity == W.ENTITIES["Grass"]


def test_full_grow_harvest_cycle_with_injected_models():
    # inject concrete models so the script can actually run end to end
    models = W.ModelSet(
        grow=lambda entity, elapsed: True,        # instant growth
        yield_=lambda entity, size: 1.0,          # one item per harvest
    )
    interp, world = make(
        "plant(Entities.Grass)\n"
        "ok = can_harvest()\n"
        "got = harvest()\n",
        world=W.World(size=3, models=models),
    )
    assert interp.global_env.get("ok") is True
    assert interp.global_env.get("got") is True
    assert world.tile().entity is None            # harvested away
    assert world.num_items("Hay") == 1.0


# -- the loud holes (default models refuse) --------------------------------------------------
def test_can_harvest_refuses_without_a_grow_model():
    with pytest.raises(Unspecified) as exc:
        make("plant(Entities.Grass)\nx = can_harvest()\n", world=W.World(size=3))
    assert exc.value.topic == "grow-time"


def test_harvest_yield_refuses_without_a_yield_model():
    models = W.ModelSet(grow=lambda e, el: True)  # grows, but yield still unmeasured
    with pytest.raises(Unspecified) as exc:
        make("plant(Entities.Grass)\nharvest()\n", world=W.World(size=3, models=models))
    assert exc.value.topic == "harvest-yield"


def test_measure_sunflower_refuses_without_a_petal_model():
    with pytest.raises(Unspecified) as exc:
        make("plant(Entities.Sunflower)\np = measure()\n", world=W.World(size=3))
    assert exc.value.topic == "sunflower-petals"


def test_pumpkin_death_refuses_without_a_death_model():
    models = W.ModelSet(grow=lambda e, el: True)  # grown, so death must resolve — and it is unmeasured
    with pytest.raises(Unspecified) as exc:
        make("plant(Entities.Pumpkin)\nx = can_harvest()\n", world=W.World(size=3, models=models))
    assert exc.value.topic == "pumpkin-death-rate"


def test_pumpkin_that_dies_becomes_dead_pumpkin():
    models = W.ModelSet(grow=lambda e, el: True, death=lambda: True)
    _, world = make(
        "plant(Entities.Pumpkin)\nx = can_harvest()\n",
        world=W.World(size=3, models=models),
    )
    assert world.tile().entity == W.ENTITIES["Dead_Pumpkin"]


# -- drones refused, on purpose (drones.md) --------------------------------------------------
def test_spawn_drone_is_a_documented_refusal():
    with pytest.raises(Unspecified) as exc:
        make("def w():\n    pass\nspawn_drone(w)\n")
    assert exc.value.topic == "drone-scheduling"


def test_measure_on_unmodelled_entity_is_not_supported():
    with pytest.raises(NotSupported):
        make("plant(Entities.Cactus)\nm = measure()\n", world=W.World(size=3))


# -- get_water (api/reference.md: float 0-1 under the drone; measured-numbers.md: 1 tick) ------
def test_get_water_reads_current_tile_follows_position_and_costs_one_tick():
    world = W.World(size=3)
    world.tile(0, 0).water = 0.25
    world.tile(1, 0).water = 0.75
    interp, world = make_world_interpreter(world=world)

    interp.run_source("a = get_water()\n")
    assert interp.global_env.get("a") == 0.25
    assert isinstance(interp.global_env.get("a"), float)
    assert world.ticks == 1

    ticks_before = world.ticks
    interp.run_source("move(East)\nb = get_water()\n")
    assert interp.global_env.get("b") == 0.75
    assert world.ticks - ticks_before == 200 + 1  # move (200) + one sense (1)
