import json

import requests

from . import constants


def create_query(age: tuple = (None, None),
                 gender: str = None,
                 image: str = None,
                 diagnosis: str = None,
                 tool: str = None) -> str:
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
    if age is not None and not age == (None, None) and not age == ('', ''):
        # select_str += f' ?{AGE_VAR}'
        filter_body += '\n' + f'FILTER (?{constants.AGE.var} > {age[0]} && ?{constants.AGE.var} < {age[1]}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.AGE.rel} ?{constants.AGE.var} }}'

    if gender is not None and not gender == '':
        # select_str += f' ?{GENDER_VAR}'
        filter_body += '\n' + f'FILTER (?{constants.GENDER.var} = "{gender}").'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.GENDER.rel} ?{constants.GENDER.var} }}'

    if image is not None and not image == '':
        # select_str += f' ?{IMAGE_VAR}'
        filter_body += '\n' + f'FILTER (?{constants.IMAGE.var} = {image}).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.IMAGE.rel} ?{constants.IMAGE.var} }}'

    if diagnosis is not None and not diagnosis == '':
        # select_str += ' ?diagnosis'
        filter_body += '\n' + f'FILTER (?{constants.DIAGNOSIS.var} = <{diagnosis}>).'
    q_body += '\n' + f'OPTIONAL {{?siri {constants.DIAGNOSIS.rel} ?{constants.DIAGNOSIS.var} }}'

    if tool is not None:
        pass

    # Temporary override
    select_str = '?age ?gender ?image ?diagnosis'

    q_preamble = constants.DEFAULT_CONTEXT + f'''
    SELECT DISTINCT ?open_neuro_id ?siri {select_str} 
    WHERE {{
        ?siri a prov:Person.
        ?siri {constants.PROJECT.rel} ?{constants.PROJECT.var}.

        ?{constants.PROJECT.var} a nidm:Project;
            dctypes:title ?projectname;
            prov:Location ?project_location .
        BIND( strafter(?project_location,"openneuro/") AS ?open_neuro_id ) .
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
