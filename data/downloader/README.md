# Download dos dados da PNAD Contínua

Biblioteca: pnadium ([Link do PyPI](https://pypi.org/project/pnadium/))

```sh
pip install pnadium
```

## Código

```python
import pnadium

cols = ["V1028", "V2001", "V2005", "V2007", "V2009", "V2010", "VD4019"]

# dados do 1º trimestre de 2026
pnad_01_2026 = pnadium.baixar_microdados(
    ano=2026, periodo=1, caminho="./", salvar=True, variaveis=cols
)
```

## Significado de cada variável

Para obter as variáveis e o significado de cada uma, executei o script:

```python
import pnadium

variaveis_trimestral = pnadium.consultar_variaveis()
print(variaveis_trimestral.to_string())
```

Para analisar os resultados e facilitar leitura, redirecionei o output desse script para um arquivo (`python variaveis.py > variaveis.txt`)

## Variavéis do exemplo

- `V1028`: Peso do domicílio e das pessoas com calibragem por projeção da população
- `V2001`: Número de pessoas no domicílio;
- `V2005`: Condição da pessoa no domicílio (Responsável, cônjuge, filho(a), etc);
- `V2007`: Sexo da pessoa;
- `V2009`: Idade da pessoa em anos;
- `V2010`: Cor ou raça da pessoa;
- `VD4019`: Rendimento mensal habitual de todos os trabalhos para pessoas de 14 anos ou mais de idade;
