import pandas as pd
import numpy as np

file = "./data/pnad_trimestral_trimestre_012026.parquet"


regions_ufs = {
    "Sul": [41, 42, 43],
    "Sudeste": [31, 32, 33, 35],
    "CentroOeste": [50, 51, 52, 53],
    "Norte": [11, 12, 13, 14, 15, 16, 17],
    "Nordeste": [21, 22, 23, 24, 25, 26, 27, 28, 29],
}
regions_names = list(regions_ufs.keys())
regions: dict[str, dict[str, float]] = {}


carteira_assinada = "V4029"
# carteira_assinada_opcoes = [1, # sim
#                           2] # não

renda = "VD4019"
renda_norm = "VD4019_norm"


def clip_and_normalize(df: pd.DataFrame, c):
    df = df.dropna(subset=[renda]).copy()
    df[renda_norm] = df[renda].clip(0, c) / c
    return df


def get_regions(df: pd.DataFrame, C: float):
    for region_name in regions_names:
        region_df = df[df["UF"].isin(regions_ufs[region_name])]
        n_formal = (region_df[carteira_assinada] == 1).sum()
        n_informal = (region_df[carteira_assinada] == 2).sum()

        regions[region_name] = {
            "informal_count": n_informal,
            "informal_mean": region_df.loc[
                region_df[carteira_assinada] == 2, renda_norm
            ].mean(),
            "informal_std": region_df.loc[
                region_df[carteira_assinada] == 2, renda_norm
            ].std(ddof=0),
            "formal_count": n_formal,
            "formal_mean": region_df.loc[
                region_df[carteira_assinada] == 1, renda_norm
            ].mean(),
            "formal_std": region_df.loc[
                region_df[carteira_assinada] == 1, renda_norm
            ].std(ddof=0),
            "sens_count": 1.0,
            "sens_formal_mean": 1 / (n_formal - 1),
            "sens_formal_std": 1 / np.sqrt(n_formal - 1),
            "sens_informal_mean": 1 / (n_informal - 1),
            "sens_informal_std": 1 / np.sqrt(n_informal - 1),
        }
    return regions


def get_Sta(regions):
    groups = [
        (region, formality)
        for region in regions_names
        for formality in ["formal", "informal"]
    ]
    Sta = []
    stat_kinds = ["count", "mean", "std"]

    for region, formality in groups:
        for stat_kind in stat_kinds:
            Sta.append(regions[region][f"{formality}_{stat_kind}"])

    return Sta


def get_Sen(regions):
    groups = [
        (region, formality)
        for region in regions_names
        for formality in ["formal", "informal"]
    ]
    Sen = []
    stat_kinds = ["count", "mean", "std"]

    for region, formality in groups:
        for stat_kind in stat_kinds:
            if stat_kind == "count":
                Sen.append(1.0)
                continue
            Sen.append(regions[region][f"sens_{formality}_{stat_kind}"])

    return Sen


def main():
    df = pd.read_parquet(file)
    df = clip_and_normalize(df, 30_000)
    regions = get_regions(df, 30_000)
    Sta = get_Sta(regions)
    print(len(Sta))
    Sen = get_Sen(regions)
    print(len(Sen))


if __name__ == "__main__":
    main()
