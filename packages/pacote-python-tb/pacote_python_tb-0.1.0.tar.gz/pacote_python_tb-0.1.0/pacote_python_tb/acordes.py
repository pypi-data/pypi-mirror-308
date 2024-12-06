from pacote_python_tb.escalas import NOTAS, escala

GRAUS = {
    'maior': ['I', 'III', 'V'],
    'menor': ['I', 'III-', 'V'],
    'diminuto': ['I', 'III-', 'V-'],
    'aumentado': ['I', 'III', 'V+'],
}

ACORDES = {
    'm': {'tonalidade': 'menor', 'grau': 'menor', 'ajuste_quinta': 0},
    '°': {'tonalidade': 'menor', 'grau': 'diminuto', 'ajuste_quinta': -1},
    '+': {'tonalidade': 'maior', 'grau': 'aumentado', 'ajuste_quinta': +1},
}


def acorde(cifra: str):
    """
    Examples:
        >>> acorde('C')
        {'notas': ['C', 'E', 'G'], 'graus': ['I', 'III', 'V']}

        >>> acorde('C+')
        {'notas': ['C', 'E', 'G#'], 'graus': ['I', 'III', 'V+']}

        >>> acorde('C°')
        {'notas': ['C', 'D#', 'F#'], 'graus': ['I', 'III-', 'V-']}

        >>> acorde('Cm')
        {'notas': ['C', 'D#', 'G'], 'graus': ['I', 'III-', 'V']}
    """
    for sufixo, propriedades in ACORDES.items():
        if sufixo in cifra:
            tonica = cifra.split(sufixo)[0]
            tonalidade = propriedades['tonalidade']
            grau = propriedades['grau']
            ajuste_quinta = propriedades['ajuste_quinta']
            triade = obter_triade(tonica, tonalidade, ajuste_quinta)
            break
    else:
        tonica = cifra
        tonalidade = 'maior'
        grau = 'maior'
        triade = obter_triade(tonica, tonalidade)

    return {'notas': triade, 'graus': GRAUS[grau]}


def obter_triade(tonica: str, tonalidade: str, ajuste_quinta: int = 0):
    intervalos = (0, 2, 4)
    notas_escala = escala(tonica, tonalidade)['notas']
    tonica = tonica.upper()
    posicao_tonica = notas_escala.index(tonica)
    triade = []

    for intervalo in intervalos:
        posicao_nota = (posicao_tonica + intervalo) % len(notas_escala)
        triade.append(notas_escala[posicao_nota])

    if ajuste_quinta:
        triade[2] = semitom(triade[2], ajuste_quinta)

    return triade


def semitom(nota, intervalo):
    posicao = NOTAS.index(nota) + intervalo
    return NOTAS[posicao % len(NOTAS)]
