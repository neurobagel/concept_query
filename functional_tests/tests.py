import pytest
from selenium import webdriver


# NOTE: the `live_server` fixture is defined as part of pytest-django and doesn't need to be created anywhere.
# This is not very well documented unfortunately


@pytest.fixture(scope='module')
def driver():
    driver = webdriver.Firefox()
    yield driver
    driver.quit()


def test_user_can_run_an_empty_cohort_query(driver, live_server):
    # I am a new user and want to check out the cohort definition tool
    # I navigate to the cohort_definition URL
    driver.get(live_server.url + '/query_interface/form')

    # On the page, I see that the title of the app is "Cohort definition tool"
    assert driver.title == 'Cohort Definition Tool'

    # and I can see an interface on the left side of the window for defining my cohort,
    # and on the right I see an empty area with a notification saying
    # "please define a cohort and run a query to see results"

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
