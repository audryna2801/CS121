"""
CS121: Schelling Model of Housing Segregation

Rhedintza Audryna

  Program for simulating a variant of Schelling's model of
  housing segregation.  This program takes six parameters:

    filename -- name of a file containing a sample city grid

    R - The radius of the neighborhood: a home at Location (k, l) is in
        the neighborhood of the home at Location (i,j) if 0 <= k < N,
        0 <= l < N, and 0 <= |i-k| + |j-l| <= R.

    similarity_satisfaction_range (lower bound and upper bound) -
         acceptable range for ratio of the number of
         homes of a similar color to the number
         of occupied homes in a neighborhood.

   patience - number of satisfactory homes that must be visited before choosing
              the last one visited.

   max_steps - the maximum number of passes to make over the city
               during a simulation.

  Sample: python3 schelling.py --grid_file=tests/a20-sample-writeup.txt --r=1
         --sim_lb=0.40 --sim_ub=0.7 --patience=3 --max_steps=1
  The sample command is shown on two lines, but should be entered on
  a single line in the linux command-line
"""

import click
import utility


def is_satisfied(grid, R, location, sim_sat_range):
    '''
    Determine whether or not the homeowner at a specific location is
    satisfied using an R-neighborhood centered around the location.
    That is, does their similarity score fall with the specified
    range (inclusive).

    Inputs:
        grid(list of lists of strings): the grid
        R (int): neighborhood parameter
        location (int, int): a grid location
        sim_sat_range (float, float): lower bound and upper bound on the range
         (inclusive) for when the homeowner is satisfied with his similarity score.

    Returns:
        (boolean) True if their similarity score fall with the specified range (inclusive), 
        False otherwise

    '''

    (x, y) = location
    (lb, ub) = sim_sat_range

    assert grid[x][y] != "F"

    dim = len(grid)
    (top_x, top_y) = (max(0, x - R), max(0, y - R))
    (bot_x, bot_y) = (min(dim - 1, x + R), min(dim - 1, y + R))

    similar_count = 0
    opposite_count = 0

    for row in range(top_x, bot_x + 1):
        for col in range(top_y, bot_y + 1):
            if 0 <= abs(x - row) + abs(y - col) <= R:
                neighbor = grid[row][col]
                if neighbor == grid[x][y]:
                    similar_count += 1
                elif neighbor != "F":
                    opposite_count += 1

    similarity_score = similar_count/(similar_count + opposite_count)
    check = (lb <= similarity_score <= ub)

    return check


def swap_locations(grid, origin, destination):
    '''
    Swaps values of two locations and modifies the grid 

    Inputs:
        grid(list of lists of strings): the grid
        origin (int, int): original location
        destination (int, int): destination

    '''

    (x, y) = origin
    (i, j) = destination

    original_value = grid[x][y]
    desired_value = grid[i][j]

    grid[x][y] = desired_value
    grid[i][j] = original_value


def find_new_house(grid, R, location, sim_sat_range, patience, homes_for_sale):
    '''
    Find new location for unsatisfied homeowner, if one exists

    Inputs:
        grid(list of lists of strings): the grid
        R (int): neighborhood parameter
        location (int, int): original location
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory houses needed to move
        homes_for_sale (list of tuples): list of locations with homes for sale

    Returns:
        (int, int): location of new house if exists, 
        otherwise returns location of old house
    '''

    for new_house in homes_for_sale:
        swap_locations(grid, location, new_house)
        if is_satisfied(grid, R, new_house, sim_sat_range):
            patience -= 1
            if patience == 0:
                swap_locations(grid, location, new_house)
                return new_house
        swap_locations(grid, location, new_house)

    return location


def simulate_wave(color, grid, R, sim_sat_range, patience, homes_for_sale):
    '''
    Simulates one wave for a certain color and returns the number of
     relocations that occured in that wave

    Inputs: 
        color (str): to indicate marroon or blue wave
        grid(list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory house needed to move
        homes_for_sale (list of tuples): list of locations with homes for sale

    Returns:
        (int): number of relocations in wave
    '''

    dim = len(grid)
    relocations = 0

    for row in range(dim):
        for col in range(dim):
            location = (row, col)
            right_color = (grid[row][col] == color)
            if right_color and (not is_satisfied(grid, R, location, sim_sat_range)):
                new_location = find_new_house(grid, R, location, sim_sat_range,
                                              patience, homes_for_sale)
                if new_location != location:
                    swap_locations(grid, location, new_location)
                    homes_for_sale.remove(new_location)
                    homes_for_sale.insert(0, location)
                    relocations += 1

    return relocations


def simulate_step(grid, R, sim_sat_range, patience, homes_for_sale):
    '''
    Simulates a step, consisting of a maroon wave, followed by a blue wave

    Inputs: 
        grid (list of lists of strings): the grid
        R (int): neighborhood parameter
        sim_sat_range (float, float): lower bound and upper bound on
          the range (inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience (int): number of satisfactory houses needed to move
        homes_for_sale (list of tuples): list of locations with homes for sale

    Returns:
        (int): number of relocations in step
    '''

    maroon_wave = simulate_wave("M", grid, R, sim_sat_range, patience,
                                homes_for_sale)
    blue_wave = simulate_wave("B", grid, R, sim_sat_range, patience,
                              homes_for_sale)

    total_relocations = maroon_wave + blue_wave

    return total_relocations


def do_simulation(grid, R, sim_sat_range, patience, max_steps, homes_for_sale):
    '''
    Do a full simulation

    Inputs:
        grid(list of lists of strings): the grid
        R(int): neighborhood parameter
        sim_sat_range(float, float): lower bound and upper bound on
          the range(inclusive) for when the homeowner is satisfied
          with his similarity score.
        patience(int): number of satisfactory houses needed to move
        max_steps(int): maximum number of steps to do
        for_sale(list of tuples): list of locations with homes for sale

    Returns: 
        (int): total number of relocations completed
    '''

    total_relocations = 0
    steps = 0
    one_step_relocation = 1  # To define variable before assigning in loop

    while (steps < max_steps) and (one_step_relocation != 0):
        one_step_relocation = simulate_step(grid, R, sim_sat_range, patience,
                                            homes_for_sale)
        total_relocations += one_step_relocation
        steps += 1

    return total_relocations


@ click.command(name="schelling")
@ click.option('--grid_file', type=click.Path(exists=True))
@ click.option('--r', type=int, default=1,
               help="neighborhood radius")
@ click.option('--sim_lb', type=float, default=0.40,
               help="Lower bound of similarity range")
@ click.option('--sim_ub', type=float, default=0.70,
               help="Upper bound of similarity range")
@ click.option('--patience', type=int, default=1, help="patience level")
@ click.option('--max_steps', type=int, default=1)
def cmd(grid_file, r, sim_lb, sim_ub, patience, max_steps):
    '''
    Put it all together: do the simulation and process the results.
    '''

    if grid_file is None:
        print("No parameters specified...just loading the code")
        return

    grid = utility.read_grid(grid_file)
    for_sale = utility.find_homes_for_sale(grid)
    sim_sat_range = (sim_lb, sim_ub)

    if len(grid) < 20:
        print("Initial state of city:")
        for row in grid:
            print(row)
        print()

    num_relocations = do_simulation(grid, r, sim_sat_range, patience,
                                    max_steps, for_sale)

    if len(grid) < 20:
        print("Final state of the city:")
        for row in grid:
            print(row)
        print()

    print("Total number of relocations done: " + str(num_relocations))


if __name__ == "__main__":
    cmd()  # pylint: disable=no-value-for-parameter
