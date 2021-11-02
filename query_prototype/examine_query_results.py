# Imports

# Standard library
from collections import Counter
import json
import os

# Main functions

def add_mockinfo_to_results(p_results_json): 

    # 1. Datasets to divide up subjects
    mock_datasets = {
        "1": {
            "range": [0, 54],
            "title": "Dataset 1",
            "description": "This is the description for dataset 1."
        },
        "2": {
            "range": [55, 109],
            "title": "Dataset 2",
            "description": "This is the description for dataset 2."
        },
        "3": {
            "range": [110, 164],
            "title": "Dataset 3",
            "description": "This is the description for dataset 3."
        },
        "4": {
            "range": [165, 219],
            "title": "Dataset 4",
            "description": "This is the description for dataset 4."
        },
        "5": {
            "range": [220, 269],
            "title": "Dataset 5",
            "description": "This is the description for dataset 5."
        },  
    }

    # 2. Create a new results json with mock dataset info
    new_results_json = { 
        "head": p_results_json["head"],
        "results": {
            "bindings": p_results_json["results"]["bindings"]
        }
    }
    for index in range(len(new_results_json["results"]["bindings"])):

        subject = new_results_json["results"]["bindings"][index]
        for key in mock_datasets:
            dataset_info = mock_datasets[key]
            if index >= dataset_info["range"][0] and \
               index <= dataset_info["range"][1]:
               subject["title"] = dataset_info["title"]
               subject["description"] = dataset_info["description"]
               break

    # c. Write new results json to file
    with open("{0}{1}modified_query_results.json".format(os.getcwd(), os.sep), "w") as output_file:
        json.dump(new_results_json, output_file)


def examine_components(p_results_json):

    # 0. Save easy references to results json components
    head = p_results_json["head"]
    results = p_results_json["results"]["bindings"]

    # 1. Number of results
    print("Result count: {0}".format(len(results)))

    # 2. Record types
    key_groups = []
    for item in results:
        if item.keys() not in key_groups:
            key_groups.append(item.keys())
    print(key_groups)

    # 3. Ages
    ages = [item["age"]["value"] for item in results if "age" in item]
    print(Counter(ages))


# Main script

def main():

    # 1. Read in json results file
    filepath = "{0}{1}simple_query_sparql_results.json".format(os.getcwd(), os.sep)
    with open(filepath, "r") as input_file:
        results_json = json.loads(input_file.read())

    # 2. Save easy references to results json components
    head = results_json["head"]
    results = results_json["results"]["bindings"]

    # 3. Examine components of the results file
    # examine_components(results_json)

    # 4. Divide results up into mock datasets
    add_mockinfo_to_results(results_json)
        

if "__main__" == __name__:
    main()