from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Fixed start & destination points for multiple bots
bot_data = {
    "bot_1": {"start": [37.7749, -122.4194], "end": [37.7800, -122.4150]},
    "bot_2": {"start": [37.7720, -122.4140], "end": [37.7775, -122.4090]},
    "bot_3": {"start": [37.7765, -122.4220], "end": [37.7810, -122.4185]}
}

# Generate intermediate waypoints for each bot
def generate_path(start, end, steps=15):
    lat_diff = (end[0] - start[0]) / steps
    lng_diff = (end[1] - start[1]) / steps
    forward_path = [[start[0] + i * lat_diff, start[1] + i * lng_diff] for i in range(steps)] + [end]
    return forward_path + forward_path[::-1]  # Loop back

bot_paths = {bot_id: generate_path(data["start"], data["end"]) for bot_id, data in bot_data.items()}
bot_indices = {bot_id: 0 for bot_id in bot_data}  # Track bot positions

@app.route('/bot-move')
def bot_move():
    global bot_indices

    bot_updates = []
    for bot_id, path in bot_paths.items():
        bot_indices[bot_id] = (bot_indices[bot_id] + 1) % len(path)  # Loop movement

        bot_updates.append({
            "id": bot_id,
            "path": path,
            "current_position": path[bot_indices[bot_id]]
        })

    return jsonify({"bots": bot_updates})




@app.route('/')
def dashboard():
    bots = [
        {"id": "BOT001", "location": "A3", "battery": 76, "status": "Active", "task": "Transporting"},
        {"id": "BOT002", "location": "B1", "battery": 32, "status": "Idle", "task": "Waiting"},
        {"id": "BOT003", "location": "C2", "battery": 15, "status": "Charging", "task": "Docked"},
    ]
    return render_template("dashboard.html", 
                           total_bots=len(bots), 
                           active_bots=len([b for b in bots if b["status"] == "Active"]),
                           available_charging_stations=3, 
                           bots=bots)


@app.route("/bot-tracking")
def bot_tracking():
    bots = [
        {"id": 1, "lat": 37.7749, "lng": -122.4194, "battery": 80, "status": "Active"},
        {"id": 2, "lat": 37.7755, "lng": -122.4183, "battery": 30, "status": "Idle"},
    ]
    print(bots)  # Debugging
    return render_template("bot_tracking.html", bots=bots)


@app.route('/path-planning')
def path_planning():
    return render_template('path_planning.html')

@app.route('/charging-stations')
def charging_stations():
    return render_template('charging_stations.html')

@app.route('/collision-avoidance')
def collision_avoidance():
    return render_template('collision_avoidance.html')

@app.route('/bot-data')
def get_bot_data():
    global bot_positions

    # Simulate movement
    for bot_id in bot_positions:
        bot_positions[bot_id]["lat"] += random.uniform(-0.0005, 0.0005)
        bot_positions[bot_id]["lng"] += random.uniform(-0.0005, 0.0005)
    
    return jsonify([{**{"id": bot_id}, **data} for bot_id, data in bot_positions.items()])

# if __name__ == '__main__':
#     app.run(debug=True)
