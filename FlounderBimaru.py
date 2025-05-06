
def run_my_code():
    import random

    def create_battleship_grid(grid_size=10):
        # Constants
        SHIPS = {
            4: 1,  # 4-long ships
            3: 2,  # 3-long ships
            2: 3,  # 2-long ships
            1: 4   # 1x1 ships
        }

        # Initialize grid with water
        grid = [['~' for _ in range(grid_size)] for _ in range(grid_size)]

        def is_valid_placement(x, y, length, direction):
            """Check if a ship can be placed at the starting position (x, y) with the given length and direction."""
            if direction == 'horizontal':
                if y + length > grid_size:
                    return False
                for i in range(length):
                    if grid[x][y + i] != '~':
                        return False
                    # Check surroundings for adjacency
                    if (x > 0 and grid[x - 1][y + i] != '~') or (x < grid_size - 1 and grid[x + 1][y + i] != '~'):
                        return False
                if (y > 0 and (grid[x][y - 1] != '~' or (x > 0 and grid[x - 1][y - 1] != '~') or (x < grid_size - 1 and grid[x + 1][y - 1] != '~'))):
                    return False
                if (y + length < grid_size and (grid[x][y + length] != '~' or (x > 0 and grid[x - 1][y + length] != '~') or (x < grid_size - 1 and grid[x + 1][y + length] != '~'))):
                    return False
            elif direction == 'vertical':
                if x + length > grid_size:
                    return False
                for i in range(length):
                    if grid[x + i][y] != '~':
                        return False
                    # Check surroundings for adjacency
                    if (y > 0 and grid[x + i][y - 1] != '~') or (y < grid_size - 1 and grid[x + i][y + 1] != '~'):
                        return False
                if (x > 0 and (grid[x - 1][y] != '~' or (y > 0 and grid[x - 1][y - 1] != '~') or (y < grid_size - 1 and grid[x - 1][y + 1] != '~'))):
                    return False
                if (x + length < grid_size and (grid[x + length][y] != '~' or (y > 0 and grid[x + length][y - 1] != '~') or (y < grid_size - 1 and grid[x + length][y + 1] != '~'))):
                    return False
            return True

        def place_ship(x, y, length, direction):
            """Place a ship at the starting position (x, y) with the given length and direction."""
            if direction == 'horizontal':
                grid[x][y] = 'L'
                for i in range(1, length - 1):
                    grid[x][y + i] = 'M'
                grid[x][y + length - 1] = 'R'
            elif direction == 'vertical':
                grid[x][y] = 'D'
                for i in range(1, length - 1):
                    grid[x + i][y] = 'M'
                grid[x + length - 1][y] = 'U'

        def place_1x1_ship(x, y):
            """Place a single tile ship."""
            grid[x][y] = 'B'

        # Place ships
        for length, count in SHIPS.items():
            for _ in range(count):
                placed = False
                while not placed:
                    direction = random.choice(['horizontal', 'vertical'])
                    x = random.randint(0, grid_size - 1)
                    y = random.randint(0, grid_size - 1)
                    if length == 1:
                        if grid[x][y] == '~' and is_valid_placement(x, y, length, direction):
                            place_1x1_ship(x, y)
                            placed = True
                    else:
                        if is_valid_placement(x, y, length, direction):
                            place_ship(x, y, length, direction)
                            placed = True

        # Calculate ship counts for rows and columns
        row_counts = [sum(1 for cell in row if cell != '~') for row in grid]
        col_counts = [sum(1 for row in grid if row[col] != '~') for col in range(grid_size)]

        return grid, row_counts, col_counts

    def create_working_grid(grid_key, grid_size=10, ships_to_reveal=5):
        working_grid = [['#' for _ in range(grid_size)] for _ in range(grid_size)]
        
        # Flatten the grid_key to get all ship positions
        ship_positions = [(i, j) for i in range(grid_size) for j in range(grid_size) if grid_key[i][j] != '~']
        
        # Randomly select positions to reveal
        reveal_positions = random.sample(ship_positions, ships_to_reveal)
        
        # Reveal the selected positions in the working grid
        for x, y in reveal_positions:
            working_grid[x][y] = grid_key[x][y]
        
        return working_grid

    grid_key, row_counts, col_counts = create_battleship_grid()

    working_grid = create_working_grid(grid_key)




    print("Grid Key:")
    print("  " + " ".join(f"{col_counts[i]}" for i in range(10)))  # Column counts
    for i in range(10):
        print(f"{row_counts[i]} " + " ".join(grid_key[i]))

    print("\nStarting state:")
    print("  " + " ".join(f"{col_counts[i]}" for i in range(10)))  # Column counts
    for i in range(10):
        print(f"{row_counts[i]} " + " ".join(working_grid[i]))   

    while True:
        user_input = input("Enter 1 to continue: ")
        if user_input == "1":
            print("You entered 1. Continuing...")
            break
        else:
            print("Invalid input. Please enter 1 to continue.")

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def reveal_full_rows_columns(working_grid, row_counts, col_counts, grid_size=10):
        def update_row(row_index):
            """Update the specified row in the working grid."""
            non_unknown_tiles = sum(1 for cell in working_grid[row_index] if cell != '~' and cell != '#')
            if non_unknown_tiles == row_counts[row_index]:
                working_grid[row_index] = ['~' if cell == '#' else cell for cell in working_grid[row_index]]

        def update_column(col_index):
            """Update the specified column in the working grid."""
            non_unknown_tiles = sum(1 for row in working_grid if row[col_index] != '~' and row[col_index] != '#')
            if non_unknown_tiles == col_counts[col_index]:
                for row in range(grid_size):
                    if working_grid[row][col_index] == '#':
                        working_grid[row][col_index] = '~'
        
        # Process rows
        for row_index in range(grid_size):
            update_row(row_index)

        # Process columns
        for col_index in range(grid_size):
            update_column(col_index)

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def replace_surrounding_hashes(working_grid, grid_size=10):
        def replace_b(x, y):
            """Replace '#' surrounding a 'B' with '~'."""
            for i in range(max(0, x-1), min(grid_size, x+2)):
                for j in range(max(0, y-1), min(grid_size, y+2)):
                    if (i != x or j != y) and working_grid[i][j] == '#':
                        working_grid[i][j] = '~'
        
        def replace_diagonal_with_water(working_grid, grid_size=10):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonal directions

            # Create a copy of the working_grid to avoid modifying it while iterating
            new_grid = [row[:] for row in working_grid]

            for x in range(grid_size):
                for y in range(grid_size):
                    if working_grid[x][y] in {'M', 'S'}:
                        for dx, dy in directions:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                                if working_grid[nx][ny] == '#':
                                    new_grid[nx][ny] = '~'
        
            # Copy the changes back to the original working_grid
            for x in range(grid_size):
                for y in range(grid_size):
                    working_grid[x][y] = new_grid[x][y]

        def replace_ship(x, y, direction):
            """Replace '#' surrounding a ship with '~' based on direction."""
            # Diagonal directions
            diagonals = [
                (x-1, y-1), (x-1, y+1),
                (x+1, y-1), (x+1, y+1)
            ]
            
            # Straight directions
            straights = {
                'U': [(x+1, y), (x, y-1), (x, y+1)],  # Replace below and side tiles
                'D': [(x-1, y), (x, y-1), (x, y+1)],  # Replace above and side tiles
                'L': [(x, y-1), (x-1, y), (x+1, y)],  # Replace left and side tiles
                'R': [(x, y+1), (x-1, y), (x+1, y)],  # Replace right and side tiles
            }
            
            # Replace diagonal '#' with '~'
            for dx, dy in diagonals:
                if 0 <= dx < grid_size and 0 <= dy < grid_size and working_grid[dx][dy] == '#':
                    working_grid[dx][dy] = '~'
            
            # Replace straight '#' with '~' based on direction
            for dx, dy in straights[direction]:
                if 0 <= dx < grid_size and 0 <= dy < grid_size and working_grid[dx][dy] == '#':
                    working_grid[dx][dy] = '~'

        # Iterate through the grid to find 'B' and ship components
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'B':
                    replace_b(x, y)
                elif working_grid[x][y] in {'U', 'D', 'L', 'R'}:
                    replace_ship(x, y, working_grid[x][y])
                elif working_grid[x][y] in {'S', 'M'}:
                    replace_diagonal_with_water(working_grid, grid_size=10)

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def mark_suspected_tiles(working_grid, row_counts, col_counts, grid_size=10):
        def mark_row_suspected(row_index):
            """Mark all '#' in the row with 'S' if ship tiles + '#' tiles equals the row count."""
            ship_and_hash_tiles = sum(1 for cell in working_grid[row_index] if cell in {'S', 'U', 'D', 'L', 'R', 'M', 'B', '#'})
            if ship_and_hash_tiles == row_counts[row_index]:
                working_grid[row_index] = ['S' if cell == '#' else cell for cell in working_grid[row_index]]
        
        def mark_column_suspected(col_index):
            """Mark all '#' in the column with 'S' if ship tiles + '#' tiles equals the column count."""
            ship_and_hash_tiles = sum(1 for row in working_grid if row[col_index] in {'S', 'U', 'D', 'L', 'R', 'M', 'B', '#'})
            if ship_and_hash_tiles == col_counts[col_index]:
                for row in range(grid_size):
                    if working_grid[row][col_index] == '#':
                        working_grid[row][col_index] = 'S'

        # Mark rows
        for row_index in range(grid_size):
            mark_row_suspected(row_index)
        
        # Mark columns
        for col_index in range(grid_size):
            mark_column_suspected(col_index)

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def place_s_adjacent_to_ships(working_grid, grid_size=10):
        # Create a copy of the working_grid to avoid modifying it while iterating
        new_grid = [row[:] for row in working_grid]

        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'R':
                    if y > 0 and working_grid[x][y - 1] == '#':
                        new_grid[x][y - 1] = 'S'
                elif working_grid[x][y] == 'L':
                    if y < grid_size - 1 and working_grid[x][y + 1] == '#':
                        new_grid[x][y + 1] = 'S'
                elif working_grid[x][y] == 'U':
                    if x > 0 and working_grid[x - 1][y] == '#':
                        new_grid[x - 1][y] = 'S'
                elif working_grid[x][y] == 'D':
                    if x < grid_size - 1 and working_grid[x + 1][y] == '#':
                        new_grid[x + 1][y] = 'S'
                        
        # Copy the changes back to the original working_grid
        for x in range(grid_size):
            for y in range(grid_size):
                working_grid[x][y] = new_grid[x][y]

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def place_s_around_m(working_grid, grid_size=10):
        # Create a copy of the working_grid to avoid modifying it while iterating
        new_grid = [row[:] for row in working_grid]

        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'M':
                    # Check if the tile above or below is ~
                    above_is_water = (x > 0 and working_grid[x - 1][y] == '~')
                    below_is_water = (x < grid_size - 1 and working_grid[x + 1][y] == '~')
                    
                    # Place S to the left and right if tiles above or below are ~
                    if above_is_water or below_is_water:
                        if y > 0 and working_grid[x][y - 1] == '#':
                            new_grid[x][y - 1] = 'S'
                        if y < grid_size - 1 and working_grid[x][y + 1] == '#':
                            new_grid[x][y + 1] = 'S'
                    
                    # If neither tile above nor below is ~, check the sides
                    else:
                        right_is_water = (y < grid_size - 1 and working_grid[x][y + 1] == '~')
                        left_is_water = (y > 0 and working_grid[x][y - 1] == '~')
                        
                        # Place S above and below if tiles to the sides are ~
                        if right_is_water or left_is_water:
                            if x > 0 and working_grid[x - 1][y] == '#':
                                new_grid[x - 1][y] = 'S'
                            if x < grid_size - 1 and working_grid[x + 1][y] == '#':
                                new_grid[x + 1][y] = 'S'
        
        # Copy the changes back to the original working_grid
        for x in range(grid_size):
            for y in range(grid_size):
                working_grid[x][y] = new_grid[x][y]

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def replace_s_with_b_if_surrounded_by_water(working_grid, grid_size=10):
        """Replace `S` with `B` if all adjacent tiles are `~` or out of range."""
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'S':
                    # Assume all adjacent tiles are water initially
                    all_adjacent_water = True

                    # Check all eight possible adjacent directions
                    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
                    
                    for dx, dy in directions:
                        nx, ny = x + dx, y + dy
                        
                        if 0 <= nx < grid_size and 0 <= ny < grid_size:
                            if working_grid[nx][ny] != '~':
                                all_adjacent_water = False
                                break
                        else:
                            # If out of range, consider it water
                            continue

                    # Replace `S` with `B` if all adjacent tiles are water
                    if all_adjacent_water:
                        working_grid[x][y] = 'B'

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def update_s_to_direction_with_opposite_check(working_grid, grid_size=10):
        """Update `S` to `L`, `R`, `U`, or `D` based on surrounding ships, checking the opposite direction for `~` or out of range."""
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'S':
                    # Initialize flags to check presence of ships in each direction
                    has_ship_right = False
                    has_ship_left = False
                    has_ship_up = False
                    has_ship_down = False
                    
                    # Initialize opposite direction checks
                    opposite_left = True
                    opposite_right = True
                    opposite_up = True
                    opposite_down = True

                    # Check right
                    if y + 1 < grid_size and working_grid[x][y + 1] in ['U', 'D', 'L', 'R', 'M', 'B', 'S']:
                        has_ship_right = True
                        if y - 1 >= 0 and working_grid[x][y - 1] != '~':
                            opposite_left = False
                    
                    # Check left
                    if y - 1 >= 0 and working_grid[x][y - 1] in ['U', 'D', 'L', 'R', 'M', 'B', 'S']:
                        has_ship_left = True
                        if y + 1 < grid_size and working_grid[x][y + 1] != '~':
                            opposite_right = False
                    
                    # Check up
                    if x - 1 >= 0 and working_grid[x - 1][y] in ['U', 'D', 'L', 'R', 'M', 'B', 'S']:
                        has_ship_up = True
                        if x + 1 < grid_size and working_grid[x + 1][y] != '~':
                            opposite_down = False
                    
                    # Check down
                    if x + 1 < grid_size and working_grid[x + 1][y] in ['U', 'D', 'L', 'R', 'M', 'B', 'S']:
                        has_ship_down = True
                        if x - 1 >= 0 and working_grid[x - 1][y] != '~':
                            opposite_up = False
                    
                    # Update `S` based on surrounding ships and opposite direction checks
                    if has_ship_right and not has_ship_left and opposite_left:
                        working_grid[x][y] = 'L'
                    elif has_ship_left and not has_ship_right and opposite_right:
                        working_grid[x][y] = 'R'
                    elif has_ship_up and not has_ship_down and opposite_down:
                        working_grid[x][y] = 'U'
                    elif has_ship_down and not has_ship_up and opposite_up:
                        working_grid[x][y] = 'D'

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def convert_s_to_m_if_adjacent_ship_components(working_grid, grid_size=10):
        """Convert `S` to `M` if there are ship components adjacent to two of its sides."""
        # Iterate through each cell in the grid
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'S':
                    # Track adjacent ship components
                    adjacent_ship_components = 0

                    # Check all four possible directions
                    if x > 0 and working_grid[x - 1][y] in ['U', 'D', 'L', 'R', 'M', 'S']:  # Up
                        adjacent_ship_components += 1
                    if x < grid_size - 1 and working_grid[x + 1][y] in ['U', 'D', 'L', 'R', 'M', 'S']:  # Down
                        adjacent_ship_components += 1
                    if y > 0 and working_grid[x][y - 1] in ['U', 'D', 'L', 'R', 'M', 'S']:  # Left
                        adjacent_ship_components += 1
                    if y < grid_size - 1 and working_grid[x][y + 1] in ['U', 'D', 'L', 'R', 'M', 'S']:  # Right
                        adjacent_ship_components += 1

                    # Convert `S` to `M` if adjacent to ship components on two sides
                    if adjacent_ship_components >= 2:
                        working_grid[x][y] = 'M'

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def count_and_display_remaining_ships(working_grid, grid_size=10):
        """Counts the number of ships in the grid and calculates how many ships of each type are still remaining."""
        
        def count_ship_sequences(grid):
            row_counts = []
            col_counts = []

            # Check rows for sequences
            for x in range(grid_size):
                count = 0
                in_sequence = False
                for y in range(grid_size):
                    if grid[x][y] == 'L':
                        count = 1
                        in_sequence = True
                    elif in_sequence and grid[x][y] in ['M', 'R']:
                        count += 1
                        if grid[x][y] == 'R':
                            row_counts.append(count)
                            in_sequence = False
                    elif in_sequence and grid[x][y] == 'S':
                        in_sequence = False  # Discard count if `S` is encountered
                if in_sequence:
                    continue

            # Check columns for sequences
            for y in range(grid_size):
                count = 0
                in_sequence = False
                for x in range(grid_size):
                    if grid[x][y] == 'D':
                        count = 1
                        in_sequence = True
                    elif in_sequence and grid[x][y] in ['M', 'U']:
                        count += 1
                        if grid[x][y] == 'U':
                            col_counts.append(count)
                            in_sequence = False
                    elif in_sequence and grid[x][y] == 'S':
                        in_sequence = False  # Discard count if `S` is encountered
                if in_sequence:
                    continue

            return row_counts, col_counts

        # Count the number of B ships
        b_count = sum(row.count('B') for row in working_grid)
        
        # Get the counts of ship parts from rows and columns
        row_counts, col_counts = count_ship_sequences(working_grid)

        # Total number of ships required by type
        total_ships_required = {
            4: 1,  # 1 four-tile ship
            3: 2,  # 2 three-tile ships
            2: 3,  # 3 two-tile ships
            1: 4   # 4 one-tile ships (Bs)
        }

        # Count the ships found
        ships_found = {
            4: 0,
            3: 0,
            2: 0,
            1: 0
        }

        for count in row_counts + col_counts:
            if count in ships_found:
                ships_found[count] += 1

        # Adjust the number of one-tile ships found
        ships_found[1] = b_count

        # Calculate remaining ships
        remaining_ships = {length: total_ships_required[length] - ships_found[length] for length in total_ships_required}
        return remaining_ships

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def replace_unsolved_ships_with_hash(working_grid, grid_size=10):
        """Replace all ship parts that are not fully solved with '#'."""
        # Create a copy of the grid to track changes
        temp_grid = [row[:] for row in working_grid]

        def mark_adjacent_tiles_as_hash(x, y):
            """Marks the ship part at (x, y) and its adjacent ship parts with '#'."""
            if temp_grid[x][y] in ['L', 'R', 'U', 'D', 'M', 'S']:
                temp_grid[x][y] = '#'
                # Check all 8 possible adjacent tiles
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
                            if temp_grid[x + dx][y + dy] in ['L', 'R', 'U', 'D', 'M', 'S']:
                                temp_grid[x + dx][y + dy] = '#'

        # Iterate over the grid to find unsolved ships
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'S':
                    # Mark all adjacent ship parts as '#' including their surrounding parts
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size:
                                mark_adjacent_tiles_as_hash(x + dx, y + dy)

        # Update the working grid with changes from temp_grid
        for x in range(grid_size):
            for y in range(grid_size):
                if temp_grid[x][y] == '#':
                    working_grid[x][y] = '#'

        return working_grid

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def replace_isolated_ship_parts_with_hash(working_grid, grid_size=10):
        """Replace isolated ship parts with '#'."""
        
        def count_adjacent_ship_parts(x, y):
            """Count the number of adjacent ship parts around a given tile."""
            adjacent_count = 0
            # Check all 4 possible adjacent tiles (up, down, left, right)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    if working_grid[nx][ny] in ['L', 'R', 'U', 'D', 'M']:
                        adjacent_count += 1
            return adjacent_count

        # Create a copy of the grid to track changes
        temp_grid = [row[:] for row in working_grid]

        # Iterate over the grid to find isolated ship parts
        for x in range(grid_size):
            for y in range(grid_size):
                if working_grid[x][y] == 'M':
                    if count_adjacent_ship_parts(x, y) < 2:
                        temp_grid[x][y] = '#'
                elif working_grid[x][y] in ['U', 'D', 'L', 'R']:
                    if count_adjacent_ship_parts(x, y) < 1:
                        temp_grid[x][y] = '#'

        # Update the working grid with changes from temp_grid
        for x in range(grid_size):
            for y in range(grid_size):
                if temp_grid[x][y] == '#':
                    working_grid[x][y] = '#'

        return working_grid

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    reveal_full_rows_columns(working_grid, row_counts, col_counts)
    replace_surrounding_hashes(working_grid)
    mark_suspected_tiles(working_grid, row_counts, col_counts)
    place_s_adjacent_to_ships(working_grid)
    reveal_full_rows_columns(working_grid, row_counts, col_counts)
    replace_surrounding_hashes(working_grid)
    mark_suspected_tiles(working_grid, row_counts, col_counts)
    place_s_adjacent_to_ships(working_grid)
    reveal_full_rows_columns(working_grid, row_counts, col_counts)
    replace_surrounding_hashes(working_grid)
    mark_suspected_tiles(working_grid, row_counts, col_counts)
    place_s_adjacent_to_ships(working_grid)
    place_s_around_m(working_grid, grid_size=10)
    reveal_full_rows_columns(working_grid, row_counts, col_counts)
    replace_surrounding_hashes(working_grid)
    mark_suspected_tiles(working_grid, row_counts, col_counts)
    place_s_adjacent_to_ships(working_grid)
    place_s_around_m(working_grid, grid_size=10)
    reveal_full_rows_columns(working_grid, row_counts, col_counts)
    replace_surrounding_hashes(working_grid)
    mark_suspected_tiles(working_grid, row_counts, col_counts)
    place_s_adjacent_to_ships(working_grid)
    replace_s_with_b_if_surrounded_by_water(working_grid, grid_size=10)
    convert_s_to_m_if_adjacent_ship_components(working_grid, grid_size=10)
    update_s_to_direction_with_opposite_check(working_grid, grid_size=10)
    count_and_display_remaining_ships(working_grid, grid_size=10)

    replace_unsolved_ships_with_hash(working_grid, grid_size=10)
    replace_isolated_ship_parts_with_hash(working_grid, grid_size=10)
    replace_isolated_ship_parts_with_hash(working_grid, grid_size=10)
    replace_unsolved_ships_with_hash(working_grid, grid_size=10)

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def get_ship_lengths_list_from_remaining(remaining_ships):
        """Generate a list of ship lengths left to place from longest to shortest."""
        lengths_list = []
        for length in sorted(remaining_ships.keys(), reverse=True):
            lengths_list.extend([length] * remaining_ships[length])
        return lengths_list

    remaining_ships = count_and_display_remaining_ships(working_grid, grid_size=10)
    ship_lengths_list = get_ship_lengths_list_from_remaining(remaining_ships)

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################

    def convert_to_s(working_grid):
        for x in range(len(working_grid)):
            for y in range(len(working_grid[x])):
                if working_grid[x][y] not in ['~', '#']:
                    working_grid[x][y] = 'S'
        return working_grid

    convert_to_s(working_grid)

    print('START OF SOLVING:')

    ########################################################################################################
    ########################################################################################################
    ########################################################################################################


    import copy

    def is_valid_placement(grid, ship_length, row, col, orientation, row_counts, col_counts):
        rows = len(grid)
        cols = len(grid[0])

        # Check if the ship placement stays within the grid boundaries
        if orientation == 'horizontal' and col + ship_length > cols:
            return False
        if orientation == 'vertical' and row + ship_length > rows:
            return False

        # Check each cell in the intended placement
        for i in range(ship_length):
            r, c = (row, col + i) if orientation == 'horizontal' else (row + i, col)

            # Ensure the cell is within grid boundaries and is a valid placement
            if r >= rows or c >= cols or r < 0 or c < 0 or grid[r][c] != '#':
                return False

            # Check adjacent/diagonal cells, making sure to stay within grid boundaries
            for nr in range(max(0, r - 1), min(rows, r + 2)):
                for nc in range(max(0, c - 1), min(cols, c + 2)):
                    if (nr, nc) != (r, c) and grid[nr][nc] == 'S':
                        return False

        # Temporarily place the ship and count the `S` tiles in the grid
        temp_grid = copy.deepcopy(grid)
        for i in range(ship_length):
            r, c = (row, col + i) if orientation == 'horizontal' else (row + i, col)
            temp_grid[r][c] = 'S'

        # Verify that row and column counts are not exceeded
        for r in range(rows):
            if sum(1 for cell in temp_grid[r] if cell == 'S') > row_counts[r]:
                return False
        for c in range(cols):
            if sum(1 for r in range(rows) if temp_grid[r][c] == 'S') > col_counts[c]:
                return False

        return True



    def place_ship(working_grid, ship_length, row, col, orientation):
        if orientation == 'horizontal':
            for i in range(ship_length):
                working_grid[row][col + i] = 'S'
        else:  # vertical
            for i in range(ship_length):
                working_grid[row + i][col] = 'S'


    ships = [{'id': i, 'length': length} for i, length in enumerate(ship_lengths_list)]
    ships = [(ship['id'], ship['length']) for ship in ships]

    import copy

    def solve_ship(working_grid, ships, row_counts, col_counts, ship_index, excluded_positions):
        rows = 10
        cols = 10
        positions_tried = 0
        ship_length = ships[ship_index][1]
        
        for row in range(rows):
            for col in range(cols):
                for orientation in ['horizontal', 'vertical']:
                    if is_valid_placement(working_grid, ship_length, row, col, orientation, row_counts, col_counts):
                        positions_tried += 1
                        if positions_tried > excluded_positions[ship_index]:
                            place_ship(working_grid, ship_length, row, col, orientation)
                            return working_grid
        return None

    def solve_whole_puzzle(working_grid, ships, row_counts, col_counts):
        excluded_positions = [0] * len(ships)
        starting_grid = copy.deepcopy(working_grid)
        grid_list = [copy.deepcopy(working_grid)]
        ship_index = 0
        while True:
            working_grid = solve_ship(copy.deepcopy(grid_list[-1]), ships, row_counts, col_counts, ship_index, excluded_positions)

            if working_grid is not None:
                ship_index += 1
                grid_list.append(copy.deepcopy(working_grid))
                if ship_index == len(ships):
                    return grid_list[-1]  # Puzzle is fully solved with all ships placed
            else:
                ship_index -= 1
                if ship_index < 0:
                    ship_index = 0
                    excluded_positions[0] += 1
                    print('we got this thing')
                    if excluded_positions[0] > 199:
                        print('Error')
                        return None
                    
                excluded_positions[ship_index] += 1
                excluded_positions[ship_index + 1:] = [0] * (len(ships) - ship_index - 1)

                grid_list.pop()
                print('backtracking', excluded_positions)

                if excluded_positions[0] > 199:
                    print('Error')
                    return None



    working_grid = solve_whole_puzzle(working_grid, ships, row_counts, col_counts)




    def convert_hash_to_tilde(grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == '#':
                    grid[i][j] = '~'
        return grid

    convert_hash_to_tilde(working_grid)

    replace_s_with_b_if_surrounded_by_water(working_grid, grid_size=10)
    convert_s_to_m_if_adjacent_ship_components(working_grid, grid_size=10)
    update_s_to_direction_with_opposite_check(working_grid, grid_size=10)



    # Print the updated working_grid
    print("\nCompleted Puzzle:")
    print("  " + " ".join(f"{col_counts[i]}" for i in range(10)))  # Column counts
    for i in range(10):
        print(f"{row_counts[i]} " + " ".join(working_grid[i]))

while True:
    user_input = input("Type '1' to randomly generate and solve a puzzle (or 'exit' to stop): ")
    if user_input == "1":
        run_my_code()
    elif user_input.lower() == "exit":
        print("Exiting...")
        break
    else:
        print("Invalid input. Please type '1' to run the code or 'exit' to stop.")








            
        

