
# Imports

# Third party
from django.db import models

from query.core import process_query

# Custom
from .query_choices import *

# Create your models here.

# subject CharField
# age (float) FloatField
# gender (string) CharField
# modality (nidm:imagetypes) CharField
# diagnosis (snomded IRI) URLField
# isControl (bool) BooleanField

# class Subject(models.Model):
    
#     # Fields
#     age = models.FloatField()
#     diagnosis = models.URLField()
#     gender = models.CharField(max_length=10)
#     isControl = models.BooleanField()
#     modality = models.CharField(max_length=30)
    
#     # Relationships
#     dataset = models.ForeignKey('DatasetMetadata', on_delete=models.CASCADE)

# class DatasetMetadata(models.Model):

#     title = models.CharField(max_length=30)
#     description = models.TextField(max_length=200)

class QueryFieldsModel(models.Model):

    # Query fields
    age_lower = models.FloatField()
    age_upper = models.FloatField()
    gender = models.CharField(choices=gender_choices, max_length=30)
    modality = models.CharField(choices=modality_choices, max_length=60)
    diagnosis = models.CharField(max_length=200)
    is_control = models.CharField(choices=is_control_choices, max_length=30)

    # Results json
    results = models.JSONField(default=dict)

    # def __str__(self):
    #     return "Bob Wiley"

    @staticmethod
    def find_query_in_db(p_query_fields: dict) -> dict:

        # 0. Get a reference to all QueryFieldsModel instances in the database
        model_instances = QueryFieldsModel.objects.all()

        # 1. Check the database for saved queries that match the given one
        for instance in model_instances:
            if QueryFieldsModel.model_matches_form_data(p_query_fields, instance):
                return instance.results
        
        # 2. Return nothing, otherwise
        return None

    @staticmethod
    def model_matches_form_data(p_form_data: dict, p_model: models.Model) -> bool:
        return p_form_data["age_lower"]  == p_model.age_lower and \
               p_form_data["age_upper"]  == p_model.age_upper and \
               p_form_data["gender"]     == p_model.gender and \
               p_form_data["modality"]   == p_model.modality and \
               p_form_data["diagnosis"]  == p_model.diagnosis and \
               p_form_data["is_control"] == p_model.is_control
        


