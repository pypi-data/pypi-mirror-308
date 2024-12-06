<!-- ![logo do projeto](assets/logo.png){width="300" .classe-css} -->
# Pacote Python TB - Notas Musicais

Notas musicais é um CLI para ajudar na formação de escalas e acordes
Temos dois comandos disponíveis: `escala` e `acorde`

{% include "templates/instalacao.md" %}

## Como usar?
### Escalas
Você pode chamar a escala via linha de comando. Por exemplo:
```bash
{{ commands.run }} escala
```
Retornando os graus e as notas correspondentes a essa escala:
```
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━┓
┃ I ┃ II ┃ III ┃ IV ┃ V ┃ VI ┃ VII ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━┩
│ C │ D  │ E   │ F  │ G │ A  │ B   │
└───┴────┴─────┴────┴───┴────┴─────┘
```

#### Alteração da tônica da escala

O primeiro parametro do CLI é a tônica da escala que deseja exibir. Desta forma, você pode alterar a escala retornada. Por exemplo, a escala de `F#`:
```bash
{{ commands.run }} escala F#
```
Retornando:
```
┏━━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ I  ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃
┡━━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ F# │ G# │ A#  │ B  │ C# │ D# │ F   │
└────┴────┴─────┴────┴────┴────┴─────┘
```

#### Alteração a tonalidade da escala

Você pode alterar a tonalidade da escala também! Esse é o segundo parâmetro da linha de comando. Por exemplo, a escala de `B` maior:
```bash
{{ commands.run }} escala B maior
```
Retornando:
```
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━━┳━━━━┳━━━━━┓
┃ I ┃ II ┃ III ┃ IV ┃ V  ┃ VI ┃ VII ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━━╇━━━━╇━━━━━┩
│ B │ C# │ D#  │ E  │ F# │ G# │ A#  │
└───┴────┴─────┴────┴────┴────┴─────┘
```

## Acordes
Você pode chamar o acorde via linha de comando. Por exemplo:
```bash
{{ commands.run }} acorde
```
Retornando os graus e as notas correspondentes da tríade:
```
┏━━━┳━━━━━┳━━━┓
┃ I ┃ III ┃ V ┃
┡━━━╇━━━━━╇━━━┩
│ C │ E   │ G │
└───┴─────┴───┘
```

#### Alteração da tríade

O primeiro parametro do CLI é a cifra da tríade que deseja exibir. Desta forma, você pode alterar a tríade retornada. Por exemplo, a tríade de `F#`:
```bash
{{ commands.run }} acorde F#
```
Retornando:
```
┏━━━━┳━━━━━┳━━━━┓
┃ I  ┃ III ┃ V  ┃
┡━━━━╇━━━━━╇━━━━┩
│ F# │ A#  │ C# │
└────┴─────┴────┘
```

#### Alteração do tipo da tríade - Menor

Você pode alterar o tipo da tríade também! Por exemplo, a tríade de si menor - `Bm`:
```bash
{{ commands.run }} acorde Bm
```
Retornando:
```
┏━━━┳━━━━━━┳━━━━┓
┃ I ┃ III- ┃ V  ┃
┡━━━╇━━━━━━╇━━━━┩
│ B │ D    │ F# │
└───┴──────┴────┘
```

#### Alteração do tipo da tríade - Aumentada

Outro tipo de tríade é a aumentada! Por exemplo, a tríade de sol aumentada - `G+`:
```bash
{{ commands.run }} acorde G+
```
Retornando:
```
┏━━━┳━━━━━┳━━━━┓
┃ I ┃ III ┃ V+ ┃
┡━━━╇━━━━━╇━━━━┩
│ G │ B   │ D# │
└───┴─────┴────┘
```

#### Alteração do tipo da tríade - Diminuta

Outro tipo de tríade é a diminuta! Por exemplo, a tríade de lá sustenida diminuta - `A#°`:
```bash
{{ commands.run }} acorde A#°
```
Retornando:
```
┏━━━━┳━━━━━━┳━━━━┓
┃ I  ┃ III- ┃ V- ┃
┡━━━━╇━━━━━━╇━━━━┩
│ A# │ C#   │ E  │
└────┴──────┴────┘
```
## Campo Harmônico
Você pode chamar o campo harmônico via linha de comando. Por exemplo:
```bash
{{ commands.run }} campo-harmonico
```
Retornando, por padrão, os graus e as cifras correspondentes do campo harmônico de `C` maior:
```
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━┳━━━━━━┓
┃ I ┃ ii ┃ iii ┃ IV ┃ V ┃ vi ┃ vii° ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━╇━━━━━━┩
│ C │ Dm │ Em  │ F  │ G │ Am │ B°   │
└───┴────┴─────┴────┴───┴────┴──────┘
```
#### Alteração da tônica da campo harmônico

O primeiro parametro do CLI é a tônica da campo harmônico que deseja exibir. Desta forma, você pode alterar o campo harmônico retornado. Por exemplo, o campo harmônico de `A`:
```bash
{{ commands.run }} campo-harmonico A
```
Retornando:
```
┏━━━┳━━━━┳━━━━━┳━━━━┳━━━┳━━━━━┳━━━━━━┓
┃ I ┃ ii ┃ iii ┃ IV ┃ V ┃ vi  ┃ vii° ┃
┡━━━╇━━━━╇━━━━━╇━━━━╇━━━╇━━━━━╇━━━━━━┩
│ A │ Bm │ C#m │ D  │ E │ F#m │ G#°  │
└───┴────┴─────┴────┴───┴─────┴──────┘
```

#### Alteração a tonalidade do campo harmônico

Você pode alterar a tonalidade do campo harmônico também! Esse é o segundo parâmetro da linha de comando. Por exemplo, o campo harmônico de `G#` menor:
```bash
{{ commands.run }} campo-harmonico G# menor
```
Retornando:
```
┏━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━━┳━━━━┳━━━━━┓
┃ i   ┃ II° ┃ III ┃ iv  ┃ v   ┃ VI ┃ VII ┃
┡━━━━━╇━━━━━╇━━━━━╇━━━━━╇━━━━━╇━━━━╇━━━━━┩
│ G#m │ A#° │ B   │ C#m │ D#m │ E  │ F#  │
└─────┴─────┴─────┴─────┴─────┴────┴─────┘
```

## Mais informações sobre o CLI

Para descobrir mais opções, você pode usar a flag `--help`:
```bash
{{ commands.run }} --help
                                                                                                                
 Usage: notas-musicais [OPTIONS] COMMAND [ARGS]...                                                              
                                                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.          │
│ --show-completion             Show completion for the current shell, to copy it  │
│                               or customize the installation.                     │
│ --help                        Show this message and exit.                        │
╰──────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────╮
│ escala                                                                           │
│ acorde                                                                           │
│ campo-harmonico                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────╯

```