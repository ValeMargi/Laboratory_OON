import pandas as pd
import json

# Write a Python program to convert JSON data to Python objects.
json_obj = '{ " Name ":" David " , " Class ":"I" , "Age ":6 }'
python_obj = json.loads(json_obj)
print('\ nJSON data :')
print(python_obj)
print('\ nName :', python_obj ['Name '])
print('Class :', python_obj ['Class '])
print('Age:', python_obj ['Age '])

#our solution
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

print(type( python_object ))
# convert into JSON :
j_data = json.dumps(python_object)
# result is a JSON string :
print((j_data))


# Write a Python program to convert Python objects into JSON strings.
# Print all the values
json_string = json.dumps(python_object)
print(json_string)

python_dict = {'name ': 'David ', 'age ': 6, 'class ': 'I'}
python_list = ['Red ', 'Green ', 'Black ']
python_str = 'Python Json '
python_int = 1234
python_float = 21.34
python_t = True
python_f = False
python_n = None
json_dict = json.dumps(python_dict)
json_list = json.dumps(python_list)
json_str = json.dumps(python_str )
json_num1 = json.dumps(python_int )
json_num2 = json.dumps(python_float )
json_t = json.dumps( python_t )
json_f = json.dumps( python_f )
json_n = json.dumps( python_n )
print('json dict :', json_dict )
print('jason list :', json_list )
print('json string :', json_str )
print('json number1 :', json_num1 )
print('json number2 :', json_num2 )
print('json true :', json_t )
print('json false :', json_f )
print('json null :', json_n )


# Write a Python program to convert Python dictionary objects (sort by
# key) to JSON data. Print the object members with indent level 4.

json_data = json.dumps(python_dict, sort_keys=True, indent=4)
print(json.dumps(python_dict, sort_keys=True, indent=4))

#Write a Python program to create a new JSON file from an existing JSON
#file. Use the included json file 'states.json' and create a new json file that
#does not contain the 'area code' field.

states = "./resources/states.json"
with open(states, 'r') as read_file:
    python_dict = json.load(read_file)
with open("./resources/states_modified.json", "w") as wf:

 for i in python_dict["states"]:
     del i['area_codes']
 json.dump(python_dict, wf,indent=4)

# sol prof
 with open('./resources/states.json') as f:
     state_data = json.load(f)
 for state in state_data['states']:
     del state['area_codes']
 with open('./resources/new_states.json', 'w') as fwrite:
         json.dump(state_data, fwrite, indent=2)


