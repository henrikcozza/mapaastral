import json, os, base64
from unidecode import unidecode
from kerykeion import KrInstance, MakeSvgInstance 
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderSVG, renderPM
import io
import xml.dom.minidom

def hello(event, context):
    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    nome = 'Cassio Vilela'
    day = '15'
    mes ='05'
    year ='1982'
    hour = '07'
    minute ='25'
    cidade = 'Varginha. MG'
    lng = -45.4302777777778
    lat = -21.5513888888889

    result = generate_chart(nome,year,mes,day,hour,minute,cidade,lat,lng)

    response = {"statusCode": 200, "body": result}

    return response

def generate_chart(nome,year,mes,day,hour,minute,cidade,lat,lng):
    pessoa = KrInstance(nome, int(year), int(mes), int(day), int(hour), int(minute),cidade,lat=lat,lng=lng,  zodiac_type = 'Tropic',online=True, ephemered_file_folder = os.path.dirname(os.path.abspath(__file__))+'/ephemerides')
    # print(pessoa.chiron['house'])
    # import pdb; pdb.set_trace()
    name = MakeSvgInstance(pessoa,template_type='extended',lang='PT')
    nome = '_'.join(nome.split(' '))
    svg = name.makeSVG('/tmp',nome, raw=True)
    print('fim do programa')
    return svg

if '__main__' == __name__:
    output = hello({},{})
    svg_io = io.BytesIO(output['body'].encode('utf-8'))
    drawing = svg2rlg(svg_io)
    out = renderPDF.drawToFile(drawing,'file.pdf',autoSize=1)
    # out = renderSVG.drawToFile(drawing,'file.svg')
    # out = renderPM.drawToFile(drawing,'file.png')
    # import pdb; pdb.set_trace()

    print('\n\n\n\n',out,'\n\n')

