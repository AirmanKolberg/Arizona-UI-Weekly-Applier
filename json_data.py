import json


def json_to_dictionary(json_file):

    with open('job_data.json') as json_file:
        data = json.load(json_file)

        return data


def dictionary_to_json(python_dictionary, json_name):

    with open(json_name, 'w') as the_dumpee:
        json.dump(python_dictionary, the_dumpee)


# Changes the value in a {key:value} pair
def change_dictionary_value(python_dictionary, key_value, new_value):

    python_dictionary[key_value] = new_value
    return python_dictionary
