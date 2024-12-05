def _retorno():
    return ")= Verificação da validade dos valores resultou em erro, confira novamente os valores fornecidos na função. =("

def soma(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    else:
        return _retorno()


def subtracao(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    else:
        return _retorno()
    
def multiplicacao(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a * b
    else:
        return _retorno()
    
def divisao(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a / b
    else:
        return _retorno()
    
def potencia(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a ** b
    else:
        return _retorno()