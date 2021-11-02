# Author: Jonathan Armoza
# Creation date: October 25, 2021
# Purpose: Possible views for concept query demo

# Imports

# Standard library
import json
import os

# Third party
from django.shortcuts import render

# Custom
from query.core import create_query, process_query
from .forms import QueryFieldsForm
from .models import QueryFieldsModel

def prototype_ui(request):

        # return render(request, "base.html")

        view_variables = {}
        # view_variables["fields"] = prepopulate_function()
        view_variables["fields"] = {

            "gender": ["M", "F", "All"],
            "modality": ["FlowWeighted", "DiffusionWeighted", "T1Weighted", "T2Weighted", "All"],
            "is_control": ["Yes", "No", "All"]
        }

        if "POST" == request.method:

            # Do query to Sebastian's code with form fields from request
            # view_variables["query"] = sebs_query_function(form_fields)

            # Mock
            view_variables["query"] = {
                
                "age_lower":20,
                "age_upper":55,
                "gender":"F",
                "modality": "T1Weighted",
                "is_control": "No"
            }

            return render(request, "query_results.html", view_variables)

        else:
            # GET request

            return render(request, "query_blank.html", view_variables)

def get_mock_results():

    modified_filename = "{0}{1}query_prototype{1}modified_query_results.json".format(os.getcwd(), os.sep)
    with open(modified_filename, "r") as input_file:
        query_results = json.loads(input_file.read())

    return query_results

def get_manual_results():

    # a. Prepare data for query
    # (NOTE: This should be done in future in form data cleaning function)
    age_lower = int(form.cleaned_data["age_lower"])
    age_upper = int(form.cleaned_data["age_upper"])
    gender = form.cleaned_data["gender"].lower()
    modality = "http://purl.org/nidash/nidm#" + form.cleaned_data["modality"]
    diagnosis = ""

    # b. Create a SPARQL query string with the query fields
    sparql_query = create_query(
        (age_lower, age_upper),
        gender,
        modality,
        diagnosis,
        "" )

    print("SPARQL QUERY")
    print(sparql_query)
    
    # b. Query the graph database for datasets and subjects that fit 
    # the field criteria
    query_results = process_query(sparql_query)

    return query_results

def get_correct_results(p_form):

    # a. Create a SPARQL query string with the query fields
    sparql_query = create_query(
        (p_form.cleaned_data["age_lower"], p_form.cleaned_data["age_upper"]),
        p_form.cleaned_data["gender"],
        p_form.cleaned_data["modality"],
        p_form.cleaned_data["diagnosis"],
        "" )

    print("SPARQL QUERY")
    print(sparql_query)

    # b. Query the graph database for datasets and subjects that fit 
    # the field criteria
    query_results = process_query(sparql_query)

    return query_results

def process_results_into_datasets(p_query_results):

    # 1. Gather dataset info and add subjects to each dataset dictionary
    dataset_keys = {}
    datasets = []
    for subject in p_query_results["results"]["bindings"]:
        if subject["title"] not in dataset_keys:
            dataset_keys[subject["title"]] = len(dataset_keys)
            datasets.append({
                "title": subject["title"],
                "description": subject["description"],
                "subjects": []
            })
        index = dataset_keys[subject["title"]]
        datasets[index]["subjects"].append({
            "id":        len(datasets[index]["subjects"]) + 1,
            "age":       subject["age"]["value"],
            "modality":  subject["image"]["value"],
            "gender":    subject["gender"]["value"],
            "diagnosis": subject["siri"]["value"]
        })

    return datasets


def formgenerated_query(request):

    # 1. POST request handling
    if "POST" == request.method:
        
        # A. Create a form object based on data in the POST request
        form = QueryFieldsForm(request.POST)
        
        # B. If form field data is valid, get query results from the fields
        if form.is_valid():

            # I. Look in the database to see if this query has already been performed
            query_results = QueryFieldsModel.find_query_in_db(form.cleaned_data)
            
            # II. If not and a new query must be performed            
            if not query_results:

                # Mock results (NOTE: To be removed)
                # query_results = get_mock_results()

                # Manually prepared results
                # query_results = get_manual_results()

                # Correct flow
                query_results = get_correct_results(form)
                # with open(os.getcwd() + os.sep + "correct_results.json", "w") as output_file:
                #     json.dump(query_results, output_file)

                # Solution for adding extra fields to the database:
                # https://stackoverflow.com/questions/58642207/save-extra-fields-to-django-model-apart-from-the-fields-which-were-present-in-dj

                # c. Save the form data to the database without commit
                query_model_instance = form.save(commit=False)

                # d. Add in the query results to the model object
                query_model_instance.results = query_results

                # e. Save the model object with query results to the database
                query_model_instance.save()

            # III. Respond with the form fields and query results
            results_for_template = process_results_into_datasets(query_results)
            return render(
                request,
                "query_results_new.html",
                { 
                    "form": form,
                    "results": results_for_template,
                    "query": True 
                }
            )

    # 2. GET request handling
    
    # A. Create a blank query form
    form = QueryFieldsForm()

    # B. Respond with the blank form fields
    return render(request, 'new_base.html', {"form": form, "results": [], "query": False})
 