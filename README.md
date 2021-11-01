# Escher Cubes Solver
Auther: Tong Zhang (ztqwerty)
Date: Nov.1, 2021

### Intro
This is a solver (WIP) for tackling the Escher Cubes puzzle. 

The Escher Cubes puzzle is a packing puzzle designed by Jean Claude Constantin. The goal is to put all pieces into the cube base. There are existing reviews about this puzzle, like [this one](http://mypuzzlecollection.blogspot.com/2013/10/escher-cubes.html). So let's directly jump into the solver!

### Demo Solving Process
To run the solver:
``` python
>> python hexagon_puzzle.py
```

- The solving screenshot should be something like this:
<iframe src="https://streamable.com/e/lcvhu4" width="560" height="440" frameborder="0" allowfullscreen></iframe>

### Tips
- The location of the pin hex can be set like:
`pin_hex = libhex.Hex(0, -3, 3)`
The defintion of the hex coordinates can be found in [Hexagonal Grid](https://www.redblobgames.com/grids/hexagons/) website. 

- Once it finds a solution, it will print in the terminal. One can also plot the solution by running:
`Hex_plot_current_candi(Hex_Map, pin_hex, Sol)`

- See more in the **Spoiler** part in `hexagon_puzzle.py`

- Currently the solver is quite slow (kind of a brute-force search). Optimization work TBD.
### References
- [Hexagonal Grid](https://www.redblobgames.com/grids/hexagons/) from Red Blob Games:
This site is quite helpful for providing some fundamental knowledge including math and modeling of 2D hexagon games. 

- I bought this puzzle from [PuzzleMaster](https://www.puzzlemaster.ca/browse/wood/european/5649-escher-cubes)
