# Author: Jonathan Armoza
# Creation date: October 25, 2021
# Purpose: Possible views for concept query demo

# Imports

# Standard library
import ast
import csv
import datetime
import json
import os

# Third party
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse # For large files

# Custom
from query.core import agg_dataset_info, create_query, process_query
from .forms import QueryFieldsForm
from .models import QueryFieldsModel
# from examine_query_results import examine_query_results
from .query_choices import *

# Class for streaming http response for large files
class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

# Helper functions

def filtered_query_results(p_filtered_data, p_query_results):

    # 0. Will store lists based on each subject in the query results that matches the filter
    csv_data = []

    # 1. Save the header as the first row
    header = [
        "dataset_id",
        "dataset_title",
        "subject_id",
        "age",
        "gender",
        "diagnosis",
        "modality"
    ]
    csv_data.append(header)

    # 2. Quickly construct a choices dictionary
    choices = {

        "gender": {choice[0]: choice[1] for choice in gender_choices},
        "siri": {choice[0]: choice[1] for choice in diagnosis_choices},
        "image": {choice[0]: choice[1] for choice in modality_choices},
        "is_control": {choice[0]: choice[1] for choice in is_control_choices}
    }

    # 3. Filter the query results
    for result in p_query_results:

        # A. Only subjects in the filter datasets are selected
        if result["dataset_id"] in p_filtered_data["datasets"]:

            # I. Each row will feature human-readable versions
            result_row = [
                result["dataset_id"],
                "\"" + result["title"] + "\"",
                str(len(csv_data)),
                result["age"],
            ]

            # II. Save extra field values if present in the subject data
            for field in choices.keys():
                if field in result:
                    result_row.append(result[field])
                else:
                    result_row.append("")

            # III. Save the row
            csv_data.append(result_row)

    return csv_data
            
def get_query_results(p_form):

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

def labels_from_choices(p_choices):

    return [choice[1] for choice in p_choices if "All" != choice[1]]

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

# Views

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

def formgenerated_query(request):

    # 1. POST request handling
    if "POST" == request.method:
        
        # A. Create a form object based on data in the POST request
        form = QueryFieldsForm(request.POST)
        
        # B. If form field data is valid, get query results from the fields
        if form.is_valid():

            # I. Look in the database to see if this query has already been performed
            query_model_instance = QueryFieldsModel.find_query_in_db(form.cleaned_data)
            if query_model_instance:
                query_results = query_model_instance.results
            
            # II. If not and a new query must be performed            
            if not query_model_instance:

                # a. Get SPARQL query results based on form inputs
                query_results = get_query_results(form)

                # b. Save the form data to the database without commit
                query_model_instance = form.save(commit=False)

                # c. Add in the query results to the model object
                query_model_instance.results = query_results

                # d. Save the model object with query results to the database
                query_model_instance.save()

            # III. Respond with the form fields and query results
            # results_for_template = process_results_into_datasets(query_results)
            results_for_template = agg_dataset_info(query_results)

            # IV. Extra information for populating results on the page
            styles = {

            }

            # V. Summary stats of the search results
            stats = {

                "datasets": len(results_for_template),
                "subjects": sum([result["n_subjects"] for result in results_for_template])
                # "gender": { 
                #     "labels": labels_from_choices(gender_choices),
                #     "data": ...
                # }
            }

            return render(
                request,
                "query_results_new.html",
                { 
                    "form": form,
                    "id": query_model_instance.id,
                    "query": True,
                    "results": results_for_template,
                    "stats": stats,
                    "styles": styles
                }
            )

    # 2. GET request handling
    
    # A. Create a blank query form
    form = QueryFieldsForm()

    # B. Respond with the blank form fields
    return render(request, 'new_base.html', {"form": form, "results": [], "query": False})

def download_csv(request):

    # 1. Get the dataset IDs in list form
    decoded_request = request.body.decode("utf-8")
    filtered_data = ast.literal_eval(decoded_request)

    # 2. Get the query results for the corresponding query
    query_model_instance = QueryFieldsModel.objects.get(pk=filtered_data["query"])
    query_results = query_model_instance.results

    # 3. Build filtered dataset for the csv file
    csv_data = filtered_query_results(filtered_data, query_results)

    # 4. Construct a CSV response
    # For how the csv django response works, see:
    # https://docs.djangoproject.com/en/3.2/howto/outputting-csv/
    response = HttpResponse(headers = {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment; filename=results_new.csv"
    })
    # 'attachment; filename="results_new.csv"'.format(datetime.datetime.now())
    # response["mime_type"] = "application/x-download"

    # A. Create a csv writer that writes to the http response
    writer = csv.writer(response)

    # B. Write the csv header and filtered query results
    for index in range(len(csv_data)):
        writer.writerow(csv_data[index])

    # # Streaming implementation
    # pseudo_buffer = Echo()
    # writer = csv.writer(pseudo_buffer)
    # response = StreamingHttpResponse(
    #     (writer.writerow(row) for row in csv_data),
    #     content_type="text/csv",
    #     mime_type='application/force-download'
    # )
    # response["Content-Disposition"] = "attachment; filename=\"results_new.csv\""

    # C. Return response with csv file data
    return response
