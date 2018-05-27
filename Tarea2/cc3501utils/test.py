from characters import Characters
from grid import Grid
from physics import Physics

pjs = Characters()
pjs.set_physics(Physics(5, 8, 10))
grid = Grid(5, 8, pjs)
pjs.set_grid(grid)
grid.init_blocks()
for block in pjs.physics.blocks['sblock']:
    print(block)