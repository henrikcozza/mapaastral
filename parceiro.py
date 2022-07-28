from kerykeion import KrInstance, MakeSvgInstance


nome = input("Digite o nome da pessoa: ")
day = input("Digite o dia de nascimento da pessoa: ")
mes = input("Digite o mes de nascimento da pessoa: ")
year = input("Digite o ano de nascimento da pessoa: ")
hour = input("Digite a hora de nascimento da pessoa descontando horario de verão: ")
minute = input("Digite os minutos do nascimento da pessoa: ")
cidade = input("Digite a cidade de nascimento da pessoa: ")
timezone = input("Digite o timezone da regiao de nascimento da pessoa: ")

pessoa_1 = KrInstance(nome, int(year), int(mes), int(day), int(hour), int(minute), cidade, tz_str=timezone, zodiac_type = 'Tropic')

nome = input("Digite o nome da pessoa: ")
day = input("Digite o dia de nascimento da pessoa: ")
mes = input("Digite o mes de nascimento da pessoa: ")
year = input("Digite o ano de nascimento da pessoa: ")
hour = input("Digite a hora de nascimento da pessoa descontando horario de verão: ")
minute = input("Digite os minutos do nascimento da pessoa: ")
cidade = input("Digite a cidade de nascimento da pessoa: ")
timezone = input("Digite o timezone da regiao de nascimento da pessoa: ")

pessoa_2 = KrInstance(nome, int(year), int(mes), int(day), int(hour), int(minute), cidade, tz_str=timezone, zodiac_type = 'Tropic')

name = MakeSvgInstance(pessoa_1,chart_type='Composite',second_obj=pessoa_2, template_type='extended',lang='PT', new_settings_file='kr.config.json')
name.makeSVG()
print('fim do programa')