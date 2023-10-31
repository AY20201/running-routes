from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin
from routing import get_loops
from routing import convert_loops_to_dict
import time

app = Flask(__name__)
CORS(app)

@app.route('/data', methods=['GET'])
@cross_origin()
def get_data():
    args = request.args

    target_distance_min = args.get("dist_min", default=0.0, type=float)
    target_distance_max = args.get("dist_max", default=0.0, type=float)
    location_lat = args.get("loc_lat", default=0.0, type=float)
    location_lon = args.get("loc_lon", default=0.0, type=float)
    kilometers = args.get("km", default=0, type=int)
    count = args.get("count", default=0, type=int)
    
    print(target_distance_min, target_distance_max, location_lat, location_lon, kilometers, count)
    starting_time = time.time()
    #print(get_distance([42.37630424656022, -71.3342364184333], [42.36926512314529, -71.3410503638534]) * 1.609)

    if None not in (target_distance_min, target_distance_max, location_lat, location_lon):
        loops = get_loops([location_lat, location_lon], target_distance_min, target_distance_max, bool(kilometers), count) #will need to get params from react server later
        response = jsonify(convert_loops_to_dict(loops))
        print(f"completed in {time.time() - starting_time}")
        return response
    else:
        print("one or more parameters are None")
        return jsonify({})

# Running app
if __name__ == '__main__':
    app.run(debug=True)