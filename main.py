import os
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from algo.algo import MazeSolver
from helper import generate_commands

app = Flask(__name__)
CORS(app)

model = None


@app.route('/status', methods=['GET'])
def check_status():
    return jsonify({"result": "ok"})


@app.route('/path', methods=['POST'])
def find_path():
    content = request.json

    obstacles = content['obstacles']
    retry_flag = content['retrying']
    robot_x, robot_y = content['robot_x'], content['robot_y']
    robot_direction = int(content['robot_dir'])

    solver = MazeSolver(20, 20, robot_x, robot_y, robot_direction, big_turn=None, allow_45=False)

    for obstacle in obstacles:
        solver.add_obstacle(obstacle['x'], obstacle['y'], obstacle['d'], obstacle['id'])

    start_time = time.time()
    best_path, total_distance = solver.get_optimal_order_dp(retrying=retry_flag)
    print(f"Time taken: {time.time() - start_time:.3f}s")
    print(f"Total distance: {total_distance} units")

    command_list, time_list = generate_commands(best_path, obstacles)

    path_points = [best_path[0].get_dict()]
    index = 0
    for command in command_list:
        if command.startswith(("SNAP", "FIN")):
            continue
        elif command.startswith(("FW", "FS", "BW", "BS")):
            index += int(command[2:]) // 10
        else:
            index += 1
        path_points.append(best_path[index].get_dict())

    return jsonify({
        "data": {
            "distance": total_distance,
            "path": path_points,
            "commands": command_list,
            "time": time_list
        },
        "error": None
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
