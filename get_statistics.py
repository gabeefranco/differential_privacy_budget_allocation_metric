import pandas as pd

file = "./dados/pnad_trimestral_trimestre_012026.parquet"


regions_ufs = {
    "Sul": [41, 42, 43],
    "Sudeste": [31, 32, 33, 35],
    "Centro-Oeste": [50, 51, 52, 53],
    "Norte": [11, 12, 13, 14, 15, 16, 17],
    "Nordeste": [21, 22, 23, 24, 25, 26, 27, 28, 29],
}
regions_names = list(regions_ufs.keys())
regions: dict[str, dict[str, int]] = {}


carteira_assinada = "V4029"
# carteira_assinada_opcoes = [1, # sim
#                           2] # não

renda = "VD4019"

df = pd.read_parquet(file)

print(f"TOTAL: {df.shape[0]}")
print(f"QUANTIDADE DE INFORMAIS: {(df[carteira_assinada] == 2).sum()}")
print(f"QUANTIDADE DE FORMAIS: {(df[carteira_assinada] == 1).sum()}")
print("\n")


for region_name in regions_names:
    region_df = df[df["UF"].isin(regions_ufs[region_name])]
    regions[region_name] = {
        "informal_count": (region_df[carteira_assinada] == 2).shape[0],
        "informal_mean": region_df.loc[region_df[carteira_assinada] == 2, renda].mean(),
        "informal_std": region_df.loc[region_df[carteira_assinada] == 2, renda].std(),
        "formal_count": (region_df[carteira_assinada] == 1).shape[0],
        "formal_mean": region_df.loc[region_df[carteira_assinada] == 1, renda].mean(),
        "formal_std": region_df.loc[region_df[carteira_assinada] == 1, renda].std(),
    }

for region_name in regions_names:
    print(f"REGIÃO: {region_name}")
    for key, value in regions[region_name].items():
        print(f"{key}: {value}")
    print("------------------------------")
    print("")
