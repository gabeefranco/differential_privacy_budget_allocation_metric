from data import get_regions, clip_and_normalize
import pandas as pd
from t_tests import t
from dp import epsilon_dp

df = pd.read_csv("result.csv", index_col=0)

bud_cols = [f"bud_{i}" for i in range(1, 13)]

top10 = df.nsmallest(10, "metric").copy()
top10["sequence"] = top10[bud_cols].astype(str).agg(",".join, axis=1)

print("TOP 10 MELHORES SCORES")
i = 1
for row in top10.itertuples():
    print(f"{i}. [{row.sequence}] = {row.metric}")
    i += 1

print("\n=================\n")
print("SCORES NOTÁVEIS")

mask = (df[bud_cols] == 1.0).all(axis=1)
score = df.loc[mask, "metric"].iloc[0]

print(f"EQUAL SPLIT = {score}")


FILE = "./data/pnad_trimestral_trimestre_012026.parquet"
C = 46_366  # teto constitucional (salário de ministros da suprema corte)


def get_informal_sta(regions):
    return (
        regions["Sudeste"]["informal_count"],
        regions["Sudeste"]["informal_mean"],
        regions["Sudeste"]["informal_std"],
        regions["Nordeste"]["informal_count"],
        regions["Nordeste"]["informal_mean"],
        regions["Nordeste"]["informal_std"],
    )


def get_informal_sen(regions):
    return (
        regions["Sudeste"]["sens_count"],
        regions["Sudeste"]["sens_informal_mean"],
        regions["Sudeste"]["sens_informal_std"],
        regions["Nordeste"]["sens_count"],
        regions["Nordeste"]["sens_informal_mean"],
        regions["Nordeste"]["sens_informal_std"],
    )


# comparação a ser feita: sudeste formal vs nordeste formal
def get_formal_sta(regions):
    return (
        regions["Sudeste"]["formal_count"],
        regions["Sudeste"]["formal_mean"],
        regions["Sudeste"]["formal_std"],
        regions["Nordeste"]["formal_count"],
        regions["Nordeste"]["formal_mean"],
        regions["Nordeste"]["formal_std"],
    )


def get_formal_sen(regions):
    return (
        regions["Sudeste"]["sens_count"],
        regions["Sudeste"]["sens_formal_mean"],
        regions["Sudeste"]["sens_formal_std"],
        regions["Nordeste"]["sens_count"],
        regions["Nordeste"]["sens_formal_mean"],
        regions["Nordeste"]["sens_formal_std"],
    )


def us(bud_sequence, sen_sequence):
    result = 0
    for i in range(12):
        result += sen_sequence[i] / bud_sequence[i]
    return result


def ue(sta_true, bud, sen):
    result = [0.0, 0.0]
    for i in range(1000):
        sta_noisy = []
        for i in range(12):
            sta_noisy.append(epsilon_dp(sta_true[i], bud[i], sen[i]))

        t_true_informal = t(*sta_true[0:6])
        t_true_formal = t(*sta_true[6:12])
        t_noisy_informal = t(*sta_noisy[0:6])
        t_noisy_formal = t(*sta_noisy[6:12])
        result[0] += abs(t_true_informal - t_noisy_informal)
        result[1] += abs(t_true_formal - t_noisy_formal)

    result[0] = result[0] / 1000
    result[1] = result[1] / 1000

    return result


def get_new_notable_scores(sequences):
    regions = get_regions(df, C)

    informal_sta = get_informal_sta(regions)
    formal_sta = get_formal_sta(regions)
    informal_sen = get_informal_sen(regions)
    formal_sen = get_formal_sen(regions)

    n = 0
    for name, bud in sequences.items():
        n += 1
        metric = 0
        sta = informal_sta + formal_sta
        sen = informal_sen + formal_sen
        us_result = us(bud, sen)
        ue_result = ue(sta, bud, sen)
        metric += us_result
        metric += ue_result[0] + ue_result[1]
        metric = metric / 14.0
        print(f"{name} = {metric}")


df = pd.read_parquet(FILE)
df = clip_and_normalize(df, C)

sequences = {
    "DECREASING GEOMETRIC SERIES": [1.54, 1.41, 1.3, 1.19, 1.09, 1.0, 0.92, 0.84, 0.77, 0.71, 0.65, 0.59],
    "INCREASING GEOMETRIC SERIES": [0.59, 0.65, 0.71, 0.77, 0.84, 0.92, 1.0, 1.09, 1.19, 1.3, 1.41, 1.54],
    "DECREASING TAYLOR SERIES": [0.08, 0.41, 1.02, 1.70, 2.12, 2.12, 1.76, 1.26, 0.79, 0.44, 0.22, 0.10],
    "INCREASING TAYLOR SERIES": [0.10, 0.22, 0.44, 0.79, 1.26, 1.76, 2.12, 2.12, 1.70, 1.02, 0.41, 0.08]
}

get_new_notable_scores(sequences)

df = pd.read_parquet(FILE)
df['VD4019_norm'] = df['VD4019']
regions = get_regions(df, C)
print("antes de normalizar")
print(f"nordeste: {regions['Nordeste']}")
print(f"sudeste: {regions['Sudeste']}")

df = clip_and_normalize(df, C)
regions = get_regions(df, C)
print("depois de normalizar")
print(f"nordeste: {regions['Nordeste']}")
print(f"sudeste: {regions['Sudeste']}")
