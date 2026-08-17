from data import regions_names
import math


def t(n1, mean1, std1, n2, mean2, std2):
    return (mean1 - mean2) / math.sqrt(
        (math.pow(std1, 2) / n1) + (math.pow(std2, 2) / n2)
    )


def run_all_t_tests(regions):
    tests = {}
    for name1 in regions_names:
        for name2 in regions_names:
            region1 = regions[name1]
            region2 = regions[name2]
            if name1 != name2:
                tests[f"{name1}_informal_{name2}_informal"] = t(
                    region1["informal_count"],
                    region1["informal_mean"],
                    region1["informal_std"],
                    region2["informal_count"],
                    region2["informal_mean"],
                    region2["informal_std"],
                )
                tests[f"{name1}_formal_{name2}_formal"] = t(
                    region1["formal_count"],
                    region1["formal_mean"],
                    region1["formal_std"],
                    region2["formal_count"],
                    region2["formal_mean"],
                    region2["formal_std"],
                )
            tests[f"{name1}_formal_{name2}_informal"] = t(
                region1["formal_count"],
                region1["formal_mean"],
                region1["formal_std"],
                region2["informal_count"],
                region2["informal_mean"],
                region2["informal_std"],
            )
            tests[f"{name1}_informal_{name2}_formal"] = t(
                region1["informal_count"],
                region1["informal_mean"],
                region1["informal_std"],
                region2["formal_count"],
                region2["formal_mean"],
                region2["formal_std"],
            )

    return tests


if __name__ == "__main__":
    from data import get_regions

    regions = get_regions()
    print(run_all_t_tests(regions))
