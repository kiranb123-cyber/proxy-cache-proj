from flask import Flask, make_response
import requests
import argparse

app = Flask(__name__)


#the local cache for now
cache = {}




#what catches every path and applies it to the dummy route
@app.route("/", defaults={"Allpaths":""})
@app.route("/<path:Allpaths>")

#the function that carries it all out
def catch_all(Allpaths):
    #checks if its in the cache
    is_it_in_cache = cache.get(Allpaths)
    if is_it_in_cache == None:
        #if not itll have to get its path back from the origin and parse it
        response = requests.get(f"http://dummyjson.com/{Allpaths}") 
        custom_response = make_response(response.content , response.status_code)
        custom_response.headers["X-Cache"] = "MISS"
        cache[Allpaths] = (response.content, response.status_code)

        return custom_response
    else:
        #if it is in the cache it can get all params from the cache and use them in a make response
        custom_response = make_response(cache[Allpaths][0] , cache[Allpaths][1])
        custom_response.headers["X-Cache"] = "HIT"
        return custom_response