# operacoes.py

def somar(expressao: str) -> str:
    expressao = expressao.strip()
    if '+' in expressao:
        partes = expressao.split('+')
        if len(partes) == 2:
            parte1, parte2 = partes[0].strip(), partes[1].strip()
            if parte1.isdigit() and parte2.isdigit():
                return str(int(parte1) + int(parte2))
    return "Operação inválida"


def subtrair(expressao: str) -> str:
    expressao = expressao.strip()
    if expressao == "":
        return "Operação inválida"
    for char in expressao:
        if not (char.isdigit() or char == '-' or char.isspace()):
            return "Operação inválida"
    partes = expressao.split('-')
    if len(partes) == 1:
        return "Operação inválida"
    try:
        resultado = int(partes[0].strip())
    except ValueError:
        return "Operação inválida"
    for parte in partes[1:]:
        parte = parte.strip()
        if parte and parte.isdigit():
            resultado -= int(parte)
        else:
            return "Operação inválida"
    return str(resultado)


def multiplicar(expressao: str) -> str:
    expressao = expressao.strip()
    if '*' in expressao:
        partes = expressao.split('*')
        if len(partes) == 2:
            parte1, parte2 = partes[0].strip(), partes[1].strip()
            if parte1.isdigit() and parte2.isdigit():
                return str(int(parte1) * int(parte2))
    return "Operação inválida"


def dividir(expressao: str) -> str:
    expressao = expressao.strip()
    if '/' in expressao:
        partes = expressao.split('/')
        if len(partes) == 2:
            parte1, parte2 = partes[0].strip(), partes[1].strip()
            if parte1.isdigit() and parte2.isdigit():
                divisor = int(parte2)
                if divisor == 0:
                    return "Erro: divisão por zero"
                return str(int(parte1) / divisor)
    return "Operação inválida"