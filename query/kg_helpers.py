"""
Collection of functions to help with knowledge graph API calls we need to do regularly
"""
import argparse
from datetime import datetime
import pathlib as pal
import textwrap
import sys

from . import constants
from .core import process_query


def get_unique_values(variable: str) -> list:
    """

    Parameters
    ----------
    variable : a valid prefixed or unprefixed property of a subject node (a prov:Person)

    Returns
    -------
    A list of literals or IRIs that are the unique objects of the target property
    """
    unique_q = f'''
    SELECT DISTINCT ?value
    WHERE {{
    ?siri a prov:Person;
        {variable} ?value.
    }}
    '''
    results = process_query(constants.DEFAULT_CONTEXT + unique_q)
    return [r.get('value') for r in results]


def get_query_choices():
    """
    Build tuples of unique choices for the different domains.
    The domains are at the moment hard coded.

    Returns
    -------
    domain_choices : dictionary with choice names as keys and list of unique choice values in tuples.
        Choice tuples take the form of `( RDF_UUID, human_readable_label )`
    """
    domains = (
        (constants.GENDER, 'gender_choices'),
        (constants.DIAGNOSIS, 'diagnosis_choices'),
        (constants.IMAGE, 'modality_choices'),
        (constants.CONTROL, 'is_control_choices')
    )

    domain_choices = {choice_name: [(val, val)  # TODO replace the second part of the tuple with a human readable label
                                    for val in get_unique_values(domain.rel)]
                      for domain, choice_name in domains}

    return domain_choices


# TODO: this function should not be necessary. We should replace this with some solid, like writing to the SQL db
def write_query_choices():
    """

    Returns
    -------

    """
    domain_choices = get_query_choices()
    doc_str = f'''"""
This is an automatically generated file.
It contains the unique choices for the categorical query domains that users can select from.
This file was last generated on {datetime.strftime(datetime.now(), '%A, %d. %B %Y, %H:%M (UTC)')}.

Don't change the contents of this file below this line.
In order to update the file, run:
python -m query.kg_helpers --update-choices
    """
    '''
    domain_strs = []
    for choice_name, choices in domain_choices.items():
        domain_strs.append(f'{choice_name} = (')
        for choice in choices:
            domain_strs.append(f'    ("{choice[0]}", "{choice[1]}"),')
        domain_strs.append('    (None, "All")\n)\n')

    choice_str = textwrap.dedent(doc_str) + '\n'.join(domain_strs)
    with open(pal.Path(__file__).parent.resolve() / '../query_prototype/query_choices.py', 'w') as f:
        f.write(choice_str)
    print('New query choices written')


def parse(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--update', required=True, action='store_true', default=False,
                        help='Use this flag to create a new query_choices.py file.')
    arguments = parser.parse_args(args)
    if arguments.update:
        write_query_choices()


if __name__ == '__main__':
    parse(sys.argv[1:])
