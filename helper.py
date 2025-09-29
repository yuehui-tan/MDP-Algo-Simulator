from consts import WIDTH, HEIGHT, Direction


def is_valid(center_x: int, center_y: int):
    """Checks if given position is within bounds

    Inputs
    ------
    center_x (int): x-coordinate
    center_y (int): y-coordinate

    Returns
    -------
    bool: True if valid, False otherwise
    """
    return center_x > 0 and center_y > 0 and center_x < WIDTH - 1 and center_y < HEIGHT - 1


# def command_generator(states, obstacles):
#     """
#     This function takes in a list of states and generates a list of commands for the robot to follow
    
#     Inputs
#     ------
#     states: list of State objects
#     obstacles: list of obstacles, each obstacle is a dictionary with keys "x", "y", "d", and "id"

#     Returns
#     -------
#     commands: list of commands for the robot to follow
#     """

#     # Convert the list of obstacles into a dictionary with key as the obstacle id and value as the obstacle
#     obstacles_dict = {ob['id']: ob for ob in obstacles}
    
#     # Initialize commands list
#     commands = []

#     # Iterate through each state in the list of states
#     for i in range(1, len(states)):
#         steps = "00"

#         # If previous state and current state are the same direction,
#         if states[i].direction == states[i - 1].direction:
#             # Forward - Must be (east facing AND x value increased) OR (north facing AND y value increased)
#             if (states[i].x > states[i - 1].x and states[i].direction == Direction.EAST) or (states[i].y > states[i - 1].y and states[i].direction == Direction.NORTH):
#                 commands.append("FW10")
#             # Forward - Must be (west facing AND x value decreased) OR (south facing AND y value decreased)
#             elif (states[i].x < states[i-1].x and states[i].direction == Direction.WEST) or (
#                     states[i].y < states[i-1].y and states[i].direction == Direction.SOUTH):
#                 commands.append("FW10")
#             # Backward - All other cases where the previous and current state is the same direction
#             else:
#                 commands.append("BW10")

#             # If any of these states has a valid screenshot ID, then add a SNAP command as well to take a picture
#             if states[i].screenshot_id != -1:
#                 # NORTH = 0
#                 # EAST = 2
#                 # SOUTH = 4
#                 # WEST = 6

#                 current_ob_dict = obstacles_dict[states[i].screenshot_id] # {'x': 9, 'y': 10, 'd': 6, 'id': 9}
#                 current_robot_position = states[i] # {'x': 1, 'y': 8, 'd': <Direction.NORTH: 0>, 's': -1}

#                 # Obstacle facing WEST, robot facing EAST
#                 if current_ob_dict['d'] == 6 and current_robot_position.direction == 2:
#                     if current_ob_dict['y'] > current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_L")
#                     elif current_ob_dict['y'] == current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_C")
#                     elif current_ob_dict['y'] < current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_R")
#                     else:
#                         commands.append(f"SNAP{states[i].screenshot_id}")
                
#                 # Obstacle facing EAST, robot facing WEST
#                 elif current_ob_dict['d'] == 2 and current_robot_position.direction == 6:
#                     if current_ob_dict['y'] > current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_R")
#                     elif current_ob_dict['y'] == current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_C")
#                     elif current_ob_dict['y'] < current_robot_position.y:
#                         commands.append(f"SNAP{states[i].screenshot_id}_L")
#                     else:
#                         commands.append(f"SNAP{states[i].screenshot_id}")

#                 # Obstacle facing NORTH, robot facing SOUTH
#                 elif current_ob_dict['d'] == 0 and current_robot_position.direction == 4:
#                     if current_ob_dict['x'] > current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_L")
#                     elif current_ob_dict['x'] == current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_C")
#                     elif current_ob_dict['x'] < current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_R")
#                     else:
#                         commands.append(f"SNAP{states[i].screenshot_id}")

#                 # Obstacle facing SOUTH, robot facing NORTH
#                 elif current_ob_dict['d'] == 4 and current_robot_position.direction == 0:
#                     if current_ob_dict['x'] > current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_R")
#                     elif current_ob_dict['x'] == current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_C")
#                     elif current_ob_dict['x'] < current_robot_position.x:
#                         commands.append(f"SNAP{states[i].screenshot_id}_L")
#                     else:
#                         commands.append(f"SNAP{states[i].screenshot_id}")
#             continue

#         # If previous state and current state are not the same direction, it means that there will be a turn command involved
#         # Assume there are 4 turning command: FR, FL, BL, BR (the turn command will turn the robot 90 degrees)
#         # FR00 | FR30: Forward Right;
#         # FL00 | FL30: Forward Left;
#         # BR00 | BR30: Backward Right;
#         # BL00 | BL30: Backward Left;

#         # Facing north previously
#         if states[i - 1].direction == Direction.NORTH:
#             # Facing east afterwards
#             if states[i].direction == Direction.EAST:
#                 # y value increased -> Forward Right
#                 if states[i].y > states[i - 1].y:
#                     commands.append("FR{}".format(steps))
#                 # y value decreased -> Backward Left
#                 else:
#                     commands.append("BL{}".format(steps))
#             # Facing west afterwards
#             elif states[i].direction == Direction.WEST:
#                 # y value increased -> Forward Left
#                 if states[i].y > states[i - 1].y:
#                     commands.append("FL{}".format(steps))
#                 # y value decreased -> Backward Right
#                 else:
#                     commands.append("BR{}".format(steps))
#             else:
#                 raise Exception("Invalid turing direction")

#         elif states[i - 1].direction == Direction.EAST:
#             if states[i].direction == Direction.NORTH:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("FL{}".format(steps))
#                 else:
#                     commands.append("BR{}".format(steps))

#             elif states[i].direction == Direction.SOUTH:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("BL{}".format(steps))
#                 else:
#                     commands.append("FR{}".format(steps))
#             else:
#                 raise Exception("Invalid turing direction")

#         elif states[i - 1].direction == Direction.SOUTH:
#             if states[i].direction == Direction.EAST:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("BR{}".format(steps))
#                 else:
#                     commands.append("FL{}".format(steps))
#             elif states[i].direction == Direction.WEST:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("BL{}".format(steps))
#                 else:
#                     commands.append("FR{}".format(steps))
#             else:
#                 raise Exception("Invalid turing direction")

#         elif states[i - 1].direction == Direction.WEST:
#             if states[i].direction == Direction.NORTH:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("FR{}".format(steps))
#                 else:
#                     commands.append("BL{}".format(steps))
#             elif states[i].direction == Direction.SOUTH:
#                 if states[i].y > states[i - 1].y:
#                     commands.append("BR{}".format(steps))
#                 else:
#                     commands.append("FL{}".format(steps))
#             else:
#                 raise Exception("Invalid turing direction")
#         else:
#             raise Exception("Invalid position")

#         # If any of these states has a valid screenshot ID, then add a SNAP command as well to take a picture
#         if states[i].screenshot_id != -1:  
#             # NORTH = 0
#             # EAST = 2
#             # SOUTH = 4
#             # WEST = 6

#             current_ob_dict = obstacles_dict[states[i].screenshot_id] # {'x': 9, 'y': 10, 'd': 6, 'id': 9}
#             current_robot_position = states[i] # {'x': 1, 'y': 8, 'd': <Direction.NORTH: 0>, 's': -1}

#             # Obstacle facing WEST, robot facing EAST
#             if current_ob_dict['d'] == 6 and current_robot_position.direction == 2:
#                 if current_ob_dict['y'] > current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_L")
#                 elif current_ob_dict['y'] == current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_C")
#                 elif current_ob_dict['y'] < current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_R")
#                 else:
#                     commands.append(f"SNAP{states[i].screenshot_id}")
            
#             # Obstacle facing EAST, robot facing WEST
#             elif current_ob_dict['d'] == 2 and current_robot_position.direction == 6:
#                 if current_ob_dict['y'] > current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_R")
#                 elif current_ob_dict['y'] == current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_C")
#                 elif current_ob_dict['y'] < current_robot_position.y:
#                     commands.append(f"SNAP{states[i].screenshot_id}_L")
#                 else:
#                     commands.append(f"SNAP{states[i].screenshot_id}")

#             # Obstacle facing NORTH, robot facing SOUTH
#             elif current_ob_dict['d'] == 0 and current_robot_position.direction == 4:
#                 if current_ob_dict['x'] > current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_L")
#                 elif current_ob_dict['x'] == current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_C")
#                 elif current_ob_dict['x'] < current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_R")
#                 else:
#                     commands.append(f"SNAP{states[i].screenshot_id}")

#             # Obstacle facing SOUTH, robot facing NORTH
#             elif current_ob_dict['d'] == 4 and current_robot_position.direction == 0:
#                 if current_ob_dict['x'] > current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_R")
#                 elif current_ob_dict['x'] == current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_C")
#                 elif current_ob_dict['x'] < current_robot_position.x:
#                     commands.append(f"SNAP{states[i].screenshot_id}_L")
#                 else:
#                     commands.append(f"SNAP{states[i].screenshot_id}")

#     # Final command is the stop command (FIN)
#     commands.append("FIN")  

#     # Compress commands if there are consecutive forward or backward commands
#     compressed_commands = [commands[0]]

#     for i in range(1, len(commands)):
#         # If both commands are BW
#         if commands[i].startswith("BW") and compressed_commands[-1].startswith("BW"):
#             # Get the number of steps of previous command
#             steps = int(compressed_commands[-1][2:])
#             # If steps are not 90, add 10 to the steps
#             if steps != 90:
#                 compressed_commands[-1] = "BW{}".format(steps + 10)
#                 continue

#         # If both commands are FW
#         elif commands[i].startswith("FW") and compressed_commands[-1].startswith("FW"):
#             # Get the number of steps of previous command
#             steps = int(compressed_commands[-1][2:])
#             # If steps are not 90, add 10 to the steps
#             if steps != 90:
#                 compressed_commands[-1] = "FW{}".format(steps + 10)
#                 continue
        
#         # Otherwise, just add as usual
#         compressed_commands.append(commands[i])
#     time = time_generator(compressed_commands)
#     return compressed_commands,time

def command_generator(states, obstacles):
    """
    Generate movement + turn + SNAP commands for the robot.
    
    Supports 8 directions (45° increments).
    """

    # Convert obstacles to dict
    obstacles_dict = {ob['id']: ob for ob in obstacles}
    commands = []

    for i in range(1, len(states)):
        prev = states[i - 1]
        curr = states[i]

        # === Case 1: Same direction (move forward/backward) ===
        if curr.direction == prev.direction:
            if (curr.x > prev.x and curr.direction in [Direction.EAST, Direction.NORTHEAST, Direction.SOUTHEAST]) \
               or (curr.x < prev.x and curr.direction in [Direction.WEST, Direction.NORTHWEST, Direction.SOUTHWEST]) \
               or (curr.y > prev.y and curr.direction in [Direction.NORTH, Direction.NORTHEAST, Direction.NORTHWEST]) \
               or (curr.y < prev.y and curr.direction in [Direction.SOUTH, Direction.SOUTHEAST, Direction.SOUTHWEST]):
                commands.append("FW10")
            else:
                commands.append("BW10")

        # === Case 2: Different direction (turn needed) ===
        else:
            old_dir = int(prev.direction)
            new_dir = int(curr.direction)
            diff = (new_dir - old_dir) % 8  # clockwise difference in 45° steps

            if diff == 1:   # 45° right
                commands.append("FR45")
            elif diff == 2: # 90° right
                commands.append("FR90")
            elif diff == 3: # 135° right
                commands.extend(["FR90", "FR45"])
            elif diff == 4: # 180°
                commands.extend(["FR90", "FR90"])
            elif diff == 7: # 45° left
                commands.append("FL45")
            elif diff == 6: # 90° left
                commands.append("FL90")
            elif diff == 5: # 135° left
                commands.extend(["FL90", "FL45"])
            else:
                raise Exception("Invalid turning direction")

        # === SNAP command handling ===
        if curr.screenshot_id != -1:
            current_ob_dict = obstacles_dict[curr.screenshot_id]
            current_robot_position = curr

            # Obstacle facing WEST, robot facing EAST
            if current_ob_dict['d'] == Direction.WEST and current_robot_position.direction == Direction.EAST:
                if current_ob_dict['y'] > current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_L")
                elif current_ob_dict['y'] == current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_C")
                elif current_ob_dict['y'] < current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_R")
                else:
                    commands.append(f"SNAP{curr.screenshot_id}")

            # Obstacle facing EAST, robot facing WEST
            elif current_ob_dict['d'] == Direction.EAST and current_robot_position.direction == Direction.WEST:
                if current_ob_dict['y'] > current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_R")
                elif current_ob_dict['y'] == current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_C")
                elif current_ob_dict['y'] < current_robot_position.y:
                    commands.append(f"SNAP{curr.screenshot_id}_L")
                else:
                    commands.append(f"SNAP{curr.screenshot_id}")

            # Obstacle facing NORTH, robot facing SOUTH
            elif current_ob_dict['d'] == Direction.NORTH and current_robot_position.direction == Direction.SOUTH:
                if current_ob_dict['x'] > current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_L")
                elif current_ob_dict['x'] == current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_C")
                elif current_ob_dict['x'] < current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_R")
                else:
                    commands.append(f"SNAP{curr.screenshot_id}")

            # Obstacle facing SOUTH, robot facing NORTH
            elif current_ob_dict['d'] == Direction.SOUTH and current_robot_position.direction == Direction.NORTH:
                if current_ob_dict['x'] > current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_R")
                elif current_ob_dict['x'] == current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_C")
                elif current_ob_dict['x'] < current_robot_position.x:
                    commands.append(f"SNAP{curr.screenshot_id}_L")
                else:
                    commands.append(f"SNAP{curr.screenshot_id}")

    # Final stop
    commands.append("FIN")

    # === Compress consecutive FW/BW commands ===
    compressed_commands = [commands[0]]
    for i in range(1, len(commands)):
        if commands[i].startswith("BW") and compressed_commands[-1].startswith("BW"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "BW{}".format(steps + 10)
                continue
        elif commands[i].startswith("FW") and compressed_commands[-1].startswith("FW"):
            steps = int(compressed_commands[-1][2:])
            if steps != 90:
                compressed_commands[-1] = "FW{}".format(steps + 10)
                continue
        compressed_commands.append(commands[i])

    from helper import time_generator  # ensure you import correctly
    time = time_generator(compressed_commands)
    return compressed_commands, time

# def time_generator(compressed_commands: list):
#     """
#     This function takes in a list of commands and generates the time taken

#     Inputs
#     ------
#     compressed_commands: list of commands 

#     Returns
#     -------
#     time: list of time taken for each command
#     """
#     time = []
    
#     # Iterate through each command in the list of compressed commands
#     for command in compressed_commands:
#         # Check if the command starts with 'FW' (forward movement) or 'BW' (backward movement)
#         if command.startswith("FW") or command.startswith("BW"):
#             # Extract the number of steps from the command string
#             steps = int(command[2:])
#             # Calculate time for movement: 3 seconds per step
#             time.append(steps / 10 * 3)
#         # Check if the command is a turning command (FR, FL, BR, BL)
#         elif command.startswith("FR") or command.startswith("FL") or command.startswith("BR") or command.startswith("BL"):
#             # A turn takes 8 seconds, 
#             time.append(8)
#         # Handle 'SNAP' command for taking a picture
#         elif command.startswith("SNAP"):
#             # (We assume) taking a picture takes 0 second (but we filter this out later anyway, if not we can just add x seconds to the latest step)
#             #time[:-1] += 1
#             time.append(0)
#         # Handle 'FIN' command to stop
#         elif command.startswith("FIN"):
#             # Final Commands just to end simulation should take 0 seconds
#             time.append(0)
    
#     return time


def time_generator(compressed_commands: list):
    """
    This function takes in a list of commands and generates the time taken

    Inputs
    ------
    compressed_commands: list of commands 

    Returns
    -------
    time: list of time taken for each command
    """
    time = []
    
    for command in compressed_commands:
        # Forward / Backward
        if command.startswith("FW") or command.startswith("BW"):
            steps = int(command[2:])
            # 3 seconds per 10-unit step
            time.append(steps / 10 * 3)

        # 45° turns
        elif command.startswith("FR45") or command.startswith("FL45") \
             or command.startswith("BR45") or command.startswith("BL45"):
            time.append(4)  # half of 90°

        # 90° turns
        elif command.startswith("FR90") or command.startswith("FL90") \
             or command.startswith("BR90") or command.startswith("BL90"):
            time.append(8)

        # SNAP (picture taking)
        elif command.startswith("SNAP"):
            time.append(0)

        # Finish
        elif command.startswith("FIN"):
            time.append(0)

        else:
            # Safety fallback
            raise Exception(f"Unknown command in time_generator: {command}")
    
    return time
