import json
import sys

## required library:
## pip install simplejson

#-----------------------------------------
# read a JSON file and return a dictionary
def read_json(json_config_file):
    with open(json_config_file) as f:
        # Load the JSON data into a Python dictionary
        config_as_dict = json.load(f)
        return config_as_dict
#end-def
#-----------------------------------------


# read the JSON file
json_config_file = sys.argv[1]
print("json_config_file=", json_config_file)

# Now you can work with the dictionary
print("config=", read_json(json_config_file))
