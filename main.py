import os
from time import timezone
from kerykeion import KrInstance, MakeSvgInstance


# nome = input("Digite o nome da pessoa: ")
# day = input("Digite o dia de nascimento da pessoa: ")
# mes = input("Digite o mes de nascimento da pessoa: ")
# year = input("Digite o ano de nascimento da pessoa: ")
# hour = input("Digite a hora de nascimento da pessoa descontando horario de verão: ")
# minute = input("Digite os minutos do nascimento da pessoa: ")
# cidade = input("Digite a cidade de nascimento da pessoa: ")
# timezone = input("Digite o timezone da regiao de nascimento da pessoa: ")

# nome = 'Ricardo Hida'
# day = '24'
# mes ='02'
# year ='1976'
# hour = '12'
# minute ='57'
# cidade = 'São Paulo'
# timezone = 'America/Sao_Paulo'
# lng = -46.6361111111111
# lat = -23.5475

# nome = 'Henrique Conzatti'
# day = '26'
# mes ='12'
# year ='1989'
# hour = '16'
# minute ='00'
# cidade = 'Juazeiro. BA'
# #usando timezone online
# # timezone = 'America/Bahia'
# lng = -40.5030555555556
# lat = -9.41361111111111



nome = 'Greta Kelly'
day = '12'
mes ='11'
year ='1929'
hour = '05'
minute ='31'
cidade = 'Viseu'
# timezone = 'America/New_York'
lng = -7.9
lat = 40.7333333333333



def generate_chart(nome,year,mes,day,hour,minute,cidade,lat,lng):
    # lat = float(lat.replace(',','.'))
    pessoa = KrInstance(nome, int(year), int(mes), int(day), int(hour), int(minute),cidade,lat=lat,lng=lng,  zodiac_type = 'Tropic',online=True, ephemered_file_folder = os.path.dirname(os.path.abspath(__file__))+'\ephemerides')
    # print(pessoa.chiron['house'])
    # import pdb; pdb.set_trace()
    name = MakeSvgInstance(pessoa,template_type='extended',lang='PT')
    res = name.makeSVG(output_folder='.',output_filename='teste.svg')
    print('fim do programa')
    return res

if __name__ == '__main__':
    result = generate_chart(nome,year,mes,day,hour,minute,cidade,lat,lng)

    print(result)