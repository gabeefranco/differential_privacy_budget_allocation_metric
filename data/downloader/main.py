import pnadium

cols = [
    "UF",
    "V1028",
    "V2001",
    "V2005",
    "V2007",
    "V2009",
    "V2010",
    "V4029",
    "VD4019",
    "VD4002",
]

pnad_01_2026 = pnadium.baixar_microdados(
    ano=2026, periodo=1, caminho="../", salvar=True, variaveis=cols
)
