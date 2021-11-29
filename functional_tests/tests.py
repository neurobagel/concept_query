import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


# NOTE: the `live_server` fixture is defined as part of pytest-django and doesn't need to be created anywhere.
# This is not very well documented unfortunately


@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_user_can_run_an_empty_cohort_query(driver, live_server):
    # TODO: find a better way to assert the location of elements (left / right)

    # I am a new user and want to check out the cohort definition tool
    # I navigate to the cohort_definition URL
    driver.get(live_server.url + '/query_interface/form')

    # On the page, I see that the title of the app is "Cohort Definition Tool"
    assert driver.title == 'Cohort Definition Tool'

    # and I can see a query interface on the left side of the window for defining my cohort,
    vp_width = driver.get_window_size().get('width')
    query_interface = driver.find_element(By.ID, 'query-fields-column')
    assert query_interface.rect.get('x') < 0.05 * vp_width

    # and on the right I see an empty area for the results
    results_view = driver.find_element(By.ID, 'query-results-column')
    assert vp_width - (results_view.rect.get('x') + results_view.rect.get('width')) < 0.05 * vp_width
    # the results area has a note saying "Click 'Query Metadata' for results"
    assert "Click 'Query Metadata' for results" in results_view.text

    # The interface allows me to define age, gender, diagnosis, and modality. I leave all of them emtpy

    # Below the query interface, I see a button labeled with "run query". I click on it to run my query

    # On the right side I can now see cards for each dataset that matches my cohort criteria

    # Above the results section, I see summary statistics for the total number of subjects and datasets included
    # in my cohort

    # Each dataset card has a checkbox that I can select and deselect to include or exclude the dataset from the
    # download list

    # below the results view section I see a button labeled "Download results". I click it to download a csv
    # with the results of my cohort query

    # I have now downloaded a csv

    # I am happy and leave the app to go and tell my friends about this excellent experience
    pass
