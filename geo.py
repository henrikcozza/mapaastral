try:
  import unzip_requirements
except ImportError:
  pass

from unicodedata import normalize
import os, json, re


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def get_country(event, context):
  search = event['queryStringParameters']['find']
  with_out_acent = normalize('NFKD', search).encode('ASCII','ignore').decode('ASCII')
  search = with_out_acent.lower()
  paisesPath = os.environ['LAMBDA_TASK_ROOT'] + "/astralmapagen/data/paises.json"  
  paisesFile = open(paisesPath)
  paises = json.load(paisesFile)
  result = [pais for pais in paises['paises'] if search in normalize('NFKD', pais['PaisExt']).encode('ASCII','ignore').decode('ASCII').lower()]  
  teste = paises['paises'][0]['PaisExt']
  print(search, normalize('NFKD',teste).encode('ASCII','ignore').decode('ASCII').lower())
  return json.dumps(result)

def get_city(event, context):
  country = event['queryStringParameters']['country']
  search = event['queryStringParameters']['find']
  with_out_acent = normalize('NFKD', search).encode('ASCII','ignore').decode('ASCII')
  search = with_out_acent.lower()
  cidadesPath = os.environ['LAMBDA_TASK_ROOT'] + "/astralmapagen/data/cidades.json"  
  cidadesFile = open(cidadesPath)
  cidades = json.load(cidadesFile, cls=LazyDecoder)
  result = [cidade for cidade in cidades[country] if search in normalize('NFKD', cidade['text']).encode('ASCII','ignore').decode('ASCII').lower()]  
  return json.dumps(result)
