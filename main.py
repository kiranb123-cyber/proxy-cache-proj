from flask import Flask, make_response
import requests
import argparse

app = Flask(__name__)


#the local cache for now
cache = {}

#cli section
#port cli
parser = argparse.ArgumentParser(description="proxy's cache")
parser.add_argument("--port", type=int, help="put in your port number")
parser.add_argument("--origin", type=str, help="put in your url server like dummy json")
args = parser.parse_args()


#what catches every path and applies it to the dummy route
@app.route("/", defaults={"Allpaths":""})
@app.route("/<path:Allpaths>")

#the function that carries it all out
def catch_all(Allpaths):
    #checks if its in the cache
    is_it_in_cache = cache.get(Allpaths)
    if is_it_in_cache == None:
        #if not itll have to get its path back from the --origin and parse it
        response = requests.get(f"{args.origin}/{Allpaths}") 
        custom_response = make_response(response.content , response.status_code)
        custom_response.headers["X-Cache"] = "MISS"
        cache[Allpaths] = (response.content, response.status_code)

        return custom_response
    else:
        #if it is in the cache it can get all params from the cache and use them in a make response
        custom_response = make_response(cache[Allpaths][0] , cache[Allpaths][1])
        custom_response.headers["X-Cache"] = "HIT"
        return custom_response
    


#this is for the cli --port 9000
if __name__ == "__main__":
    app.run(port=args.port, debug=True)