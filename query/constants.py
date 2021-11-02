from collections import namedtuple
import re

from requests.auth import HTTPBasicAuth


DEFAULT_CONTEXT = '''
PREFIX afni: <http://purl.org/nidash/afni#>
PREFIX ants: <http://stnava.github.io/ANTs/>
PREFIX bids: <http://bids.neuroimaging.io/>
PREFIX birnlex: <http://bioontology.org/projects/ontologies/birnlex/>
PREFIX crypto: <http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions#>
PREFIX datalad: <http://datasets.datalad.org/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX dctypes: <http://purl.org/dc/dcmitype/>
PREFIX dicom: <http://neurolex.org/wiki/Category:DICOM_term/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX freesurfer: <https://surfer.nmr.mgh.harvard.edu/>
PREFIX fsl: <http://purl.org/nidash/fsl#>
PREFIX ilx: <http://uri.interlex.org/base/>
PREFIX ncicb: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX ncit: <http://ncitt.ncit.nih.gov/>
PREFIX ndar: <https://ndar.nih.gov/api/datadictionary/v2/dataelement/>
PREFIX nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
PREFIX nidm: <http://purl.org/nidash/nidm#>
PREFIX niiri: <http://iri.nidash.org/>
PREFIX nlx: <http://uri.neuinfo.org/nif/nifstd/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX onli: <http://neurolog.unice.fr/ontoneurolog/v3.0/instrument.owl#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX pato: <http://purl.obolibrary.org/obo/pato#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX scr: <http://scicrunch.org/resolver/>
PREFIX sio: <http://semanticscience.org/ontology/sio.owl#>
PREFIX spm: <http://purl.org/nidash/spm#>
PREFIX vc: <http://www.w3.org/2006/vcard/ns#>
PREFIX xml: <http://www.w3.org/XML/1998/namespace>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''

# We may want to turn the prefixed string into a URI or take a URI and turn it into a prefixed string
# The two following maps should allow us to do that
default_context_map = {}
for line in DEFAULT_CONTEXT.splitlines():
    if line == '':
        continue
    groups =  re.search(r'(?<=PREFIX)\s+(?P<prefix>\w+:)\s(?P<iri><http\w*://\S+>)', line).groupdict()
    default_context_map[groups['prefix']] = groups['iri']

default_context_inverse_map = {v: k for k, v in default_context_map.items()}

DOG_ROOT = 'http://star.braindog.net'
DOG_DB = 'demo_integration'
DOG_PORT = 5820
QUERY_URL = f'{DOG_ROOT}:{DOG_PORT}/{DOG_DB}/query'
QUERY_HEADER = {'Content-Type': 'application/sparql-query', 'Accept': 'application/sparql-results+json'}
QUERY_AUTH = HTTPBasicAuth('admin', 'admin')

# Store domains in named tuples
Domain = namedtuple('Domain', ['var', 'rel'])
# Core domains
AGE = Domain('age', 'nidm:hasAge')
GENDER = Domain('gender', 'nidm:hasGender')
DIAGNOSIS = Domain('diagnosis', 'nidm:hasDiagnosis')
IMAGE = Domain('image', 'nidm:hadImageContrastType')
TOOL = Domain('tool', '')
PROJECT = Domain('project', 'nidm:isPartOfProject')
CONTROL = Domain('control', 'nidm:isSubjectGroup')

CATEGORICAL_DOMAINS = [
    GENDER,
    DIAGNOSIS,
    IMAGE
]