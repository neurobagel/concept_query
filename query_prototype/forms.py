# Author: Jonathan Armoza
# Creation date: October 28, 2021
# Purpose: Form definitions for the concept query demo

# Third party
from django import forms

# Custom
from .models import QueryFieldsModel


# Forms
class QueryFieldsForm(forms.ModelForm):
    # TODO: refactor the hardcoded fields here
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

