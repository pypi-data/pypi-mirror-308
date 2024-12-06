from pacote_python_tb.acordes import obter_triade
from pacote_python_tb.escalas import escala


def campo_harmonico(tonica: str, tonalidade: str) -> dict[str, list[str]]:
    """
    Gera um campo harmônico com base em uma tônica e uma tonalidade

    Parameters:
        tonica: Primeiro grau do campo harmônico
        tonalidade: Tonalidade para o campo. Ex: maior, menor, etc

    Returns:
        Um campo harmonico

    Examples:
        >>> campo_harmonico('c', 'maior')
        {'acordes': ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'B°'], 'graus': ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']}

        >>> campo_harmonico('c', 'menor')
        {'acordes': ['Cm', 'D°', 'D#', 'Fm', 'Gm', 'G#', 'A#'], 'graus': ['i', 'II°', 'III', 'iv', 'v', 'VI', 'VII']}
    """
    notas, _graus = escala(tonica, tonalidade).values()
    acordes_campo_harmonico = []

    for nota in notas:
        acordes_campo_harmonico.append(_validar_triade_na_escala(nota, notas))

    return {
        'acordes': acordes_campo_harmonico,
        'graus': _obter_graus_campo_harmonico(acordes_campo_harmonico, _graus),
    }


def _validar_triade_na_escala(nota: str, notas_escala: list[str]) -> str:
    """
    Validar se as notas de um acorde estão na escala

    Parameters:
        nota: Nota a ser validada
        notas_escala: Notas da escala referência

    Returns:
        Cifra relativa ao campo harmônico

    Examples:
        >>> _validar_triade_na_escala('C', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'C'

        >>> _validar_triade_na_escala('D', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'Dm'

        >>> _validar_triade_na_escala('B', ['C', 'D', 'E', 'F', 'G', 'A', 'B'])
        'B°'
    """
    tonica, terca, quinta = obter_triade(nota, 'maior')
    nota_retorno = ''

    match terca in notas_escala, quinta in notas_escala:
        case True, True:
            nota_retorno = tonica
        case False, True:
            nota_retorno = f'{tonica}m'
        case False, False:
            nota_retorno = f'{tonica}°'

    return nota_retorno


def _obter_graus_campo_harmonico(
    acordes: list[str], graus: list[str]
) -> list[str]:
    """
    Converte o grau relativo a cifra

    Parameters:
        acordes: Acordes de um campo harmonico
        graus: Graus referente à tonica maior do campo harmonico

    Returns:
        Lista dos graus do campo harmônico

    Examples:
        >>> _obter_graus_campo_harmonico(['C', 'Dm', 'Em', 'F', 'G', 'Am', 'B°'], ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'])
        ['I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii°']

        >>> _obter_graus_campo_harmonico(['Cm', 'D°', 'D#', 'Fm', 'Gm', 'G#', 'A#'], ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII'])
        ['i', 'II°', 'III', 'iv', 'v', 'VI', 'VII']
    """
    graus_campo_harmonico = []

    for acorde, grau in zip(acordes, graus):
        if 'm' in acorde:
            grau = grau.lower()

        if '°' in acorde:
            if 'm' in acordes[0]:
                grau = f'{grau}°'
            else:
                grau = f'{grau.lower()}°'

        graus_campo_harmonico.append(grau)

    return graus_campo_harmonico
