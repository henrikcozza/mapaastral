try:
  import unzip_requirements
except ImportError:
  pass

import json, os, base64, re
from kerykeion import KrInstance, MakeSvgInstance 
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import io, boto3, requests
from datetime import datetime

client = boto3.client('dynamodb')
SUCCESS      = 200
CLIENT_ERROR = 400
SERVER_ERROR = 500

def generate(event, context):
    
    response = json.loads(event['body'])
    print(event)
    date = response.get('data_birth',"")
    dia = ""
    mes = ""
    ano = ""
    hora = ""
    minuto = ""
    if len(response.get('hour_birth',"").split(':')) == 2:
        hora = response.get('hour_birth').split(':')[0]
        minuto = response.get('hour_birth').split(':')[1]
    if len(date.split('/')) == 3:
        dia = date.split('/')[0]
        mes = date.split('/')[1]
        ano = date.split('/')[2]
    try:
        data = {
            'captcha' : response.get('captcha'),
            'nome' : response.get('name'),
            'day' : dia,
            'mes' : mes,
            'year' : ano,
            'hour' : hora,
            'minute' : minuto,
            'cidade' : response.get('city_birth'),
            'lng' : float(response.get('longitude').replace(',','.')),
            'lat' : float(response.get('latitude').replace(',','.')),
            'email' : response.get('email')
        }
        print(data.get('lat'))
    except Exception as error:
        print(error)

    try:
        errors = validate(data)

    except ValueError as e:
        # this should only be an issue from reCAPTCHA,
        # so tell the client we couldn't process their request
        print('Validation Error', e)
        return response_return(SERVER_ERROR)

    if errors.keys():
        return response_return(CLIENT_ERROR, errors=errors)

    try:    
        result = generate_chart(data.get('nome'),data.get('year'),data.get('mes'),data.get('day'),data.get('hour'),data.get('minute'),data.get('cidade'),data.get('lat'),data.get('lng') )
        svg_io = io.BytesIO(result.encode('utf-8'))
        drawing = svg2rlg(svg_io)
        base_64_pdf = base64.b64encode(renderPDF.drawToString(drawing, autoSize=1))
        local = f"{data.get('cidade')}|lat:{str(data.get('lat'))}|long:{str(data.get('lng'))}"
        save_contact(data.get('nome'),data.get('email'),f"{data.get('day')}/{data.get('mes')}/{data.get('year')} {data.get('hour')}:{data.get('minute')}", local)
    except Exception as error:
        print(error)
        print('Ao gerar e salvar dados')
    
    response_data = {
        "statusCode": 200, 
        "body": base_64_pdf,
        "isBase64Encoded": True
    }

    return response_data

def response_return( statusCode, errors = None ):
    body = {
        'success': True if statusCode == SUCCESS else False,
    }
    if errors is not None:
        body['errors'] = errors
    return {
        'statusCode': statusCode,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }

def validate( data ):
    errors = {}
    # all the items in our data structure must have a value when leading and trailing whitespace is removed
    for k, v in data.items():
        # print(v)
        v = '' if v is None else str(v).strip()
        if not v:
            errors[k] = 'This is a required field'
    # very basic regex validation for email address
    if not errors.get('email') and not re.match("^[^@]+@[^@]+\.[^@.]+$", data['email']):
        errors['email'] = 'Invalid email address'
    # only do captcha validation if no other errors as we can only validate it once
    if not errors and not validateCaptcha(data['captcha']):
        errors['captcha'] = 'Invalid captcha response'
    return errors


def save_contact(name,email,nascimento,local):  
    today = datetime.now()
    data = client.put_item(
        TableName='usersTable',
        Item={
            'name':{
                'S': name
            },
            'email':{
                'S': email
            },
            'nascimento':{
                'S': nascimento
            },
            'local':{
                'S': local
            },
            'cadastro':{
                'S': today.strftime('%d/%m/%Y %H:%M')
            }
        }
    )

def generate_chart(nome,year,mes,day,hour,minute,cidade,lat,lng):
    pessoa = KrInstance(nome, int(year), int(mes), int(day), int(hour), int(minute),cidade,lat=lat,lng=lng,  zodiac_type = 'Tropic',online=True, ephemered_file_folder = os.path.dirname(os.path.abspath(__file__))+'/ephemerides')
    name = MakeSvgInstance(pessoa,template_type='extended',lang='PT')
    nome = '_'.join(nome.split(' '))
    svg = name.makeSVG('/tmp',nome, raw=True)
    return svg

def validateCaptcha( captchaResponse ):
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data = {
            'secret': os.environ.get('RECAPTCHA_SECRET'),
            'response': captchaResponse,
        }
    )
    if not response.ok:
        return False
    data = response.json()
    print('Captcha Response', data)
    return data['success']


if '__main__' == __name__:
    resp = generate({
      "body": {
            "data_birth":"26/12/1989",
            "hour_birth":"16:00",
            "captcha":"a",
            "name":"Henrique Conzatti",
            "city_birth":"Juazeiro. BA",
            "longitude":-40.5030555555556,
            "latitude":-9.41361111111111,
            "email":"henrique@conza.com.br"
        }
    },{})
    print(resp)
#     output = hello({},{})
#     svg_io = io.BytesIO(output['body'].encode('utf-8'))
#     drawing = svg2rlg(svg_io)
#     out = renderPDF.drawToString(drawing,'file.pdf',autoSize=1)
#     # out = renderSVG.drawToFile(drawing,'file.svg')
#     # out = renderPM.drawToFile(drawing,'file.png')
#     # import pdb; pdb.set_trace()

#     print('\n\n\n\n',out,'\n\n')

