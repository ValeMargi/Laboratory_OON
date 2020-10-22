import pandas as pd, json

# Write a Python program to convert JSON data to Python objects.
states = "../results/states.json"
with open(states, 'r') as read_file:
    python_dict = json.load(read_file)
    print(python_dict)

# Write a Python program to convert Python objects (dictionary) to JSON
# data.
python_object = {
    'name': 'David', 'class': 'I', 'age': 6
}
with open("../results/pythonObject_to_JSON.json", "w") as write_file:
    json.dump(python_object, write_file)

# Write a Python program to convert Python objects into JSON strings.
# Print all the values
json_string = json.dumps(python_object)
print(json_string)

# Write a Python program to convert Python dictionary objects (sort by
# key) to JSON data. Print the object members with indent level 4.

json_data = json.dumps(python_dict, sort_keys=True, indent=4)
print(json.dumps(python_dict, sort_keys=True, indent=4))

#Write a Python program to create a new JSON file from an existing JSON
#file. Use the included json file ’states.json’ and create a new json file that
#does not contain the ’area code’ field.


with open("../results/states_modified.json", "w") as wf:

 for i in python_dict["states"]:
     del i['area_codes']
 json.dump(python_dict, wf,indent=4)
