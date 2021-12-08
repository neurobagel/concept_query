import re

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


@pytest.mark.django_db
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

    # The interface allows me to define age, gender, diagnosis, and modality.
    assert driver.find_element(By.ID, 'div_id_age_lower').is_displayed()
    assert driver.find_element(By.ID, 'div_id_age_upper').is_displayed()
    assert driver.find_element(By.ID, 'div_id_gender').is_displayed()
    assert driver.find_element(By.ID, 'div_id_diagnosis').is_displayed()
    assert driver.find_element(By.ID, 'div_id_modality').is_displayed()
    # I leave all of them emtpy

    # Below the query interface, I see a button labeled with "run query". I click on it to run my query
    query_btn = driver.find_element(By.XPATH, '//button[normalize-space()="Query Metadata"]')
    assert query_btn.is_displayed()
    # I click on it to run my query
    query_btn.click()

    # On the right side I can now see cards for each dataset that matches my cohort criteria
    results_view = driver.find_element(By.ID, 'query-results-column')
    dataset_cards = results_view.find_elements(By.CLASS_NAME, 'card')
    assert dataset_cards

    # Above the results section, I see summary statistics for the total number of subjects and datasets included
    # in my cohort
    summary_stats = driver.find_element(By.ID, 'summary-stats')
    n_datasets_str = re.search(r'\d+(?= datasets)', summary_stats.text)
    assert n_datasets_str is not None

    # This number is equal to the number of cards on the page
    n_datasets = int(n_datasets_str.group())
    assert n_datasets == len(dataset_cards)

    # Each dataset card has a checkbox that I can select and deselect
    # TODO consider checking for all - might be overkill
    checkbox = dataset_cards[0].find_element(By.CLASS_NAME, 'dataset-checkbox')
    assert not checkbox.is_selected()
    checkbox.click()

    # TODO: finish the tests
    # to include or exclude the dataset from the download list

    # below the results view section I see a button labeled "Download results". I click it to download a csv
    # with the results of my cohort query

    # I have now downloaded a csv

    # I am happy and leave the app to go and tell my friends about this excellent experience
