import pytest

from query_interface.models import QueryFieldsModel


@pytest.mark.django_db
def test_that_no_query_instance_exists_yet():
    query_instance = QueryFieldsModel()
    results = query_instance.find_query_in_db(query_instance.__dict__)
    assert results is None

# TODO
# - test that a previously run query is accessible in the database