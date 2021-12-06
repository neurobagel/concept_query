import pytest

from query_interface.forms import QueryFieldsForm


def test_empty_query_form_is_valid():
    form = QueryFieldsForm(data={})
    assert form.is_valid(), 'The empty query form did not validate'


@pytest.mark.parametrize("form_field",
                         ("age_lower",
                          "age_upper",
                          "gender",
                          "diagnosis",
                          "modality",
                          "is_control"
                          )
                         )
def test_form_exposes_expected_field(form_field):
    form = QueryFieldsForm()
    assert form_field in form.fields, f'"{form_field}" was not in the query form fields'


def test_age_cannot_be_negative():
    test_data = {'age_lower': -1, 'age_upper': -1}
    form = QueryFieldsForm(data=test_data)
    assert not form.is_valid(), 'a negative age value did not invalidate the age form field'


def test_upper_age_cannot_be_greater_than_lower_age():
    test_data = {'age_lower': 2, 'age_upper': 1}
    form = QueryFieldsForm(data=test_data)
    assert not form.is_valid(), 'form not invalid if lower age > upper age'


def test_that_diagnostic_choices_are_sorted_alphabetically():
    form = QueryFieldsForm()
    diagnosis = form['diagnosis'].field
    choices = [label for code, label in diagnosis._get_choices()]
    assert choices == sorted(choices), f'The diagnosis choices are not sorted alphabetically: \n{choices}'