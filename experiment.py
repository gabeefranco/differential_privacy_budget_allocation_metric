import sys
from data import get_regions, clip_and_normalize
import pandas as pd
from t_tests import t
from dp import epsilon_dp

FILE = "./data/pnad_trimestral_trimestre_012026.parquet"
C = 46_366  # teto constitucional (salário de ministros da suprema corte)


def generate_sequences(length=12, total=12, granularity=0.5):
    units = int(total / granularity)
    min_value = 1  # 0.5 na escala de granularidade

    def generate(position, remaining, sequence):
        if position == length - 1:
            if remaining >= min_value:
                yield tuple(sequence + [remaining])
            return

        # Precisamos deixar pelo menos 1 para cada posição restante
        max_value = remaining - (length - position - 1) * min_value

        for value in range(min_value, max_value + 1):
            yield from generate(position + 1, remaining - value, sequence + [value])

    for sequence in generate(0, units, []):
        yield tuple(value * granularity for value in sequence)


# comparação a ser feita: sudeste informal vs nordeste informal
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


df = pd.read_parquet(FILE)
df = clip_and_normalize(df, C)
regions = get_regions(df, C)

sequences = []
if sys.argv[1] == "real":
    sequences = generate_sequences()
elif sys.argv[1] == "teste":
    sequences = [
        [1 for _ in range(12)],
        [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
        [2 for _ in range(12)],
    ]

informal_sta = get_informal_sta(regions)
formal_sta = get_formal_sta(regions)
informal_sen = get_informal_sen(regions)
formal_sen = get_formal_sen(regions)

print(informal_sen)
print(formal_sen)

results = []
best_metric = sys.float_info.max

n = 0
for bud in sequences:
    n += 1
    metric = 0
    sta = informal_sta + formal_sta
    sen = informal_sen + formal_sen
    us_result = us(bud, sen)
    ue_result = ue(sta, bud, sen)
    metric += us_result
    metric += ue_result[0] + ue_result[1]
    metric = metric / 14.0
    print(f"n={n}; metric={metric}")
    results.append([*bud, metric])
    if metric < best_metric:
        best_metric = metric

print(f"melhor metrica: {best_metric}")

# gera um dataframe do pandas com cada valor de bud de cada sequência, seguido do resultado da metrica para aquela sequência
cols = [f"bud_{i}" for i in range(1, 13)]
cols.append("metric")

result_df = pd.DataFrame(results, columns=cols)
result_df.to_csv("result.csv")

print("Dados salvos em result.csv")
