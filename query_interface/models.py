# Third party
from django.db import models

# Custom
from .query_choices import *


# TODO: move this helper somewhere else or find a way to do it in django
def sort_choice_tuples(p_choices):
    return sorted(p_choices, key=lambda x: x[1])


class QueryFieldsModel(models.Model):

    # Query fields
    age_lower = models.FloatField(null=True )
    age_upper = models.FloatField(null=True )
    gender = models.CharField(choices=sort_choice_tuples(gender_choices), max_length=200)
    modality = models.CharField(choices=sort_choice_tuples(modality_choices), max_length=200)
    diagnosis = models.CharField(choices=sort_choice_tuples(diagnosis_choices), max_length=200)
    is_control = models.CharField(choices=sort_choice_tuples(is_control_choices), max_length=200)
    # Parkinson specific things
    moca_lower = models.FloatField(null=True)
    moca_upper = models.FloatField(null=True)
    updrs_lower = models.FloatField(null=True)
    updrs_upper = models.FloatField(null=True)
    mmse_lower = models.FloatField(null=True)
    mmse_upper = models.FloatField(null=True)

    # Results json
    results = models.JSONField(default=dict)

    # TODO: move these static methods somewhere else
    @staticmethod
    def find_query_in_db(p_query_fields: dict) -> dict:

        # 0. Get a reference to all QueryFieldsModel instances in the database
        model_instances = QueryFieldsModel.objects.all()

        # 1. Check the database for saved queries that match the given one
        for instance in model_instances:
            if QueryFieldsModel.model_matches_form_data(p_query_fields, instance):
                return instance
        
        # 2. Return nothing, otherwise
        return None

    @staticmethod
    def model_matches_form_data(p_form_data: dict, p_model: models.Model) -> bool:
        return p_form_data["age_lower"]  == p_model.age_lower and \
               p_form_data["age_upper"]  == p_model.age_upper and \
               p_form_data["gender"]     == p_model.gender and \
               p_form_data["modality"]   == p_model.modality and \
               p_form_data["diagnosis"]  == p_model.diagnosis and \
               p_form_data["is_control"] == p_model.is_control and \
               p_form_data["moca_lower"] == p_model.moca_lower and \
               p_form_data["moca_upper"] == p_model.moca_upper and \
               p_form_data["updrs_lower"] == p_model.updrs_lower and \
               p_form_data["updrs_upper"] == p_model.updrs_upper and \
               p_form_data["mmse_lower"] == p_model.mmse_lower and \
               p_form_data["mmse_upper"] == p_model.mmse_upper
