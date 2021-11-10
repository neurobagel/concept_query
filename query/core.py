import json

import pandas as pd
import requests

from . import constants


def create_query(age: tuple = (None, None),
                 gender: str = None,
                 image: str = None,
                 diagnosis: str = None,
                 tool: str = None,
                 control: bool = False,
                 moca: tuple = (None, None),
                 updrs: tuple = (None, None),
                 mmse: tuple = (None, None)) -> str:
    """

    Parameters
    ----------
    age :
    gender :
    image :
    diagnosis :
    tool :

    Returns
    -------

    """
    # select_str = ''
    q_body = ''
    filter_body = ''
    if isinstance(age, tuple) and not age == (None, None) and not age == ('', ''):
        # select_str += f' ?{AGE_VAR}'
        # Ensure that age has default lower and upper bounds
        # TODO: revisit this and replace this solution with one that just doesn't add the filter condition.
        age = tuple((default_val if age_val is None else age_val for age_val, default_val in zip(age, [0, 100])))
        filter_body += '\n' + f'FILTER (?{constants.AGE.var} > {age[0]} && ?{constants.AGE.var} < {age[1]}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.AGE.rel} ?{constants.AGE.var} }}'

    if gender is not None and not gender == '':
        # select_str += f' ?{GENDER_VAR}'
        filter_body += '\n' + f'FILTER (?{constants.GENDER.var} = "{gender}").'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.GENDER.rel} ?{constants.GENDER.var} }}'

    if image is not None and not image == '':
        # select_str += f' ?{IMAGE_VAR}'
        filter_body += '\n' + f'FILTER (?{constants.IMAGE.var} = <{image}>).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.IMAGE.rel} ?{constants.IMAGE.var} }}'

    if diagnosis is not None and not diagnosis == '' and not control:
        # select_str += ' ?diagnosis'
        filter_body += '\n' + f'FILTER (?{constants.DIAGNOSIS.var} = <{diagnosis}>).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.DIAGNOSIS.rel} ?{constants.DIAGNOSIS.var} }}'

    if control:
        # We are searching for this graph pattern but we do not return it to the user
        # TODO: revisit this decision. Maybe we want to return the control status to the user
        q_body += '\n' + f'?siri {constants.CONTROL.rel} ?<{constants.CONTROL.var}>.'

    if tool is not None:
        pass

    # Add parkinson specific tools
    if isinstance(moca, tuple) and not moca == (None, None) and not moca == ('', ''):
        # Ensure that age has default lower and upper bounds
        # TODO: revisit this and replace this solution with one that just doesn't add the filter condition.
        moca = tuple((default_val if moca_val is None else moca_val for moca_val, default_val in zip(moca, [0, 100])))
        filter_body += '\n' + f'FILTER (?{constants.MOCA.var} > {moca[0]} && ?{constants.MOCA.var} < {moca[1]}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.MOCA.rel} ?{constants.MOCA.var} }}'

    if isinstance(updrs, tuple) and not updrs == (None, None) and not updrs == ('', ''):
        # Ensure that updrs has default lower and upper bounds
        # TODO: revisit this and replace this solution with one that just doesn't add the filter condition.
        updrs = tuple((default_val if updrs_val is None else updrs_val for updrs_val, default_val in zip(updrs, [0, 100])))
        filter_body += '\n' + f'FILTER (?{constants.UPDRS.var} > {updrs[0]} && ?{constants.UPDRS.var} < {updrs[1]}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.UPDRS.rel} ?{constants.UPDRS.var} }}'

    if isinstance(mmse, tuple) and not mmse == (None, None) and not mmse == ('', ''):
        # Ensure that mmse has default lower and upper bounds
        # TODO: revisit this and replace this solution with one that just doesn't add the filter condition.
        mmse = tuple((default_val if mmse_val is None else mmse_val for mmse_val, default_val in zip(mmse, [0, 100])))
        filter_body += '\n' + f'FILTER (?{constants.MMSE.var} > {mmse[0]} && ?{constants.MMSE.var} < {mmse[1]}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.MMSE.rel} ?{constants.MMSE.var} }}'

    # Temporary override
    select_str = '?age ?gender ?image ?diagnosis ?dataset_id ?title ?description ?repo ?moca ?updrs ?mmse'

    q_preamble = constants.DEFAULT_CONTEXT + f'''
    SELECT DISTINCT ?siri {select_str} 
    WHERE {{
        ?siri a prov:Person.
        ?siri {constants.PROJECT.rel} ?{constants.PROJECT.var}.

        ?{constants.PROJECT.var} a nidm:Project;
            dctypes:title ?title;
            nidm:fromDataRepository ?repo;
            nidm:hasDatasetID ?dataset_id
        OPTIONAL {{ ?{constants.PROJECT.var} dctypes:description ?description;}}
    '''
    query = '\n'.join([q_preamble, q_body, filter_body, '}'])

    return query


def process_query(query_str: str) -> list:
    """

    Parameters
    ----------
    query_str :

    Returns
    -------

    """
    response = requests.post(url=constants.QUERY_URL, data=query_str, headers=constants.QUERY_HEADER, auth=constants.QUERY_AUTH)
    if not response.ok:
        raise Exception(f"Query request unsuccessful ({response.status_code}): {response.content.decode('utf-8')}")

    _results = json.loads(response.content.decode('utf-8'))
    return [{k: v['value'] for k, v in res.items()} for res in _results['results']['bindings']]


def agg_dataset_info(query_results: list) -> list:
    """

    Parameters
    ----------
    query_results : list
        The list of query results returned from a successful SPARQL query run by `process_query`

    Returns
    -------
    dataset_table : list
        A list of dictionaries, where each dictionary represents a dataset. Each dataset is described by its
        title, dataset_id, the number of subjects, list of modalities, and list of diagnoses.
    """
    # Hardcode the columns. This ensures that even if a column is all None and thus excluded from the SPARQL response
    # We still have it in the dataframe we pass on to the view function
    # TODO: review this and maybe find a better solution for handling all None data
    columns = ['siri', 'age', 'gender', 'image', 'diagnosis', 'dataset_id',  'title', 'description', 'repo']
    # Turn the results into a dataframe
    results_df = pd.DataFrame(query_results, columns=columns)
    # break down the data by dataset
    datasets = results_df['dataset_id'].unique()
    dataset_table = []
    for dataset in datasets:
        data_df = results_df.query('dataset_id==@dataset')
        dataset_table.append(dict(n_subjects=data_df['siri'].nunique(),
                                  diagnoses=list(data_df['diagnosis'].dropna().unique()),
                                  modalities=list(data_df['image'].dropna().unique()),
                                  title=data_df['title'].unique(),
                                  dataset_id=dataset,
                                  repo=data_df['repo'].unique()[0]
                                  )
                             )
        # TODO: also add description here. It will not be included as a column if none of the datasets has a description
    return dataset_table
