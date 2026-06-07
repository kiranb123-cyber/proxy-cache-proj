from flask import Flask, make_response
import requests
import argparse
import redis
import json

app = Flask(__name__)






#cli section
#port cli
parser = argparse.ArgumentParser(description="proxy's cache")
parser.add_argument("--port", type=int, help="put in your port number")
parser.add_argument("--origin", type=str, help="put in your url server like dummy json")
parser.add_argument("--clear-cache", help="clears cache", action="store_true")
args = parser.parse_args()

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


#what catches every path and applies it to the dummy route
@app.route("/", defaults={"Allpaths":""})
@app.route("/<path:Allpaths>")
#the function that carries it all out
def catch_all(Allpaths):
    raw_string = r.get(Allpaths)
    #checks if its in the cache
    if raw_string == None:
        #if not itll have to get its path back from the --origin and parse it
        response = requests.get(f"{args.origin}/{Allpaths}") 
        custom_response = make_response(response.content , response.status_code)
        custom_response.headers["X-Cache"] = "MISS"
        string_content = json.dumps({"content": response.text, "status": response.status_code})
        r.set(Allpaths, string_content)
        #cache[Allpaths] = (response.content, response.status_code)

        return custom_response
    else:
        is_it_in_cache = json.loads(raw_string)
        #if it is in the cache it can get all params from the cache and use them in a make response
        custom_response = make_response(is_it_in_cache["content"] , is_it_in_cache["status"])
        custom_response.headers["X-Cache"] = "HIT"
        return custom_response
    

#the redis cache clearer
def cache_clear():
    r.flushdb()


#esnures cache is empty before its going to be used repeatedly
if args.clear_cache:
    cache_clear()
    exit()

#this is for the cli --port 9000
if __name__ == "__main__":
    app.run(port=args.port, debug=True)