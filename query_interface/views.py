# Author: Jonathan Armoza
# Creation date: October 25, 2021
# Purpose: Possible views for concept query demo

# Standard library
import ast
import csv

# Third party
from django.shortcuts import render
from django.http import HttpResponse

# Custom
from query.core import agg_dataset_info, create_query, process_query
from .forms import QueryFieldsForm
from .models import QueryFieldsModel
from .query_choices import *


# Helper functions
def filtered_query_results(p_filtered_data, p_query_results):
    # TODO: create docstring
    # This function creates the data for the csv download from the interface

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
		"diagnosis": {choice[0]: choice[1] for choice in diagnosis_choices},
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
				result["siri"]
            ]

            # II. Make sure age exists for each result before adding
            result_row.append("" if "age" not in result else result["age"])

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
    # TODO: add docstring
    # this function creates the SPARQL query from the form inputs in order to send it to the graph

    # a. Create a SPARQL query string with the query fields
    sparql_query = create_query(
        (p_form.cleaned_data["age_lower"], p_form.cleaned_data["age_upper"]),
        p_form.cleaned_data["gender"],
        p_form.cleaned_data["modality"],
        p_form.cleaned_data["diagnosis"],
        "",
        control=p_form.cleaned_data["is_control"],
        moca=(p_form.cleaned_data["moca_lower"], p_form.cleaned_data["moca_upper"]),
        updrs=(p_form.cleaned_data["updrs_lower"], p_form.cleaned_data["updrs_upper"]),
        mmse=(p_form.cleaned_data["mmse_lower"], p_form.cleaned_data["mmse_upper"]),
    )
    # TODO: replace the print statements with an actual logger
    print("SPARQL QUERY")
    print(sparql_query)

    # b. Query the graph database for datasets and subjects that fit 
    # the field criteria
    query_results = process_query(sparql_query)

    return query_results


# Views
def formgenerated_query(request):
    # TODO: add docstring
    # - generates the blank interface
    # - generates the results view once a response is coming in from the graph

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
            results_for_template = agg_dataset_info(query_results)

            # IV. Extra information for populating results on the page
            # TODO: revisit whether this should live in a separate place
            # see issue #74
            styles = {

            }

            # V. Summary stats of the search results
            stats = {

                "datasets": len(results_for_template),
                "subjects": sum([result["n_subjects"] for result in results_for_template])
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

    # A. Create a csv writer that writes to the http response
    writer = csv.writer(response)

    # B. Write the csv header and filtered query results
    for index in range(len(csv_data)):
        writer.writerow(csv_data[index])

    # C. Return response with csv file data
    return response
