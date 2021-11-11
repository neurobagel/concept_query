# Author: Jonathan Armoza
# Creation date: October 28, 2021
# Purpose: Form definitions for the concept query demo

# Imports

# Third party
from django import forms

# Custom
from .models import QueryFieldsModel
from .query_choices import *

# Forms

# class QueryFieldsForm(forms.Form):

#     age_lower = forms.FloatField(label="Age lower bound", required=True)
#     age_upper = forms.FloatField(label="Age upper bound", required=True)
#     gender = forms.ChoiceField(choices=gender_choices, label="Gender", required=True)
#     modality = forms.ChoiceField(choices=modality_choices, label="Modality", required=True)
#     diagnosis = forms.URLField(label="Diagnosis", max_length=150)
#     is_control = forms.ChoiceField(choices=is_control_choices, label="Is Control", required=True)
    
class QueryFieldsForm(forms.ModelForm):

    class Meta:
        model = QueryFieldsModel
        fields = (
            "age_lower",
            "age_upper",
            "gender",
            "modality",
            "diagnosis",
            "is_control",
            "moca_lower",
            "moca_upper",
            "updrs_lower",
            "updrs_upper",
            "mmse_lower",
            "mmse_upper",
        )
    
    def __init__(self, *args, **kwargs):
        super(QueryFieldsForm, self).__init__(*args, **kwargs)
        self.fields["age_lower"].required = False
        self.fields["age_upper"].required = False
        self.fields["gender"].required = False
        self.fields["modality"].required = False
        self.fields["diagnosis"].required = False
        self.fields["is_control"].required = False
        self.fields["moca_lower"].required = False
        self.fields["moca_upper"].required = False
        self.fields["updrs_lower"].required = False
        self.fields["updrs_upper"].required = False
        self.fields["mmse_lower"].required = False
        self.fields["mmse_upper"].required = False

