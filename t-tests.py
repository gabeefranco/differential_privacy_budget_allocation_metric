from get_statistics import get_regions, regions_names
import math

regions = get_regions()


def t(n1, mean1, std1, n2, mean2, std2):
    return (mean1 - mean2) / math.sqrt(
        (math.pow(std1, 2) / n1) + (math.pow(std2, 2) / n2)
    )


def run_all_t_tests():
    tests = {}
    for name1 in regions_names:
        for name2 in regions_names:
            if name1 != name2:
                tests[f"{name1}_formais_{name2}_informais"] = t(
                    regions[name1]["formal_count"],
                    regions[name1]["formal_mean"],
                    regions[name1]["formal_std"],
                    regions[name2]["informal_count"],
                    regions[name2]["informal_mean"],
                    regions[name2]["informal_std"],
                )
                tests[f"{name1}_informais_{name2}_informais"] = t(
                    regions[name1]["informal_count"],
                    regions[name1]["informal_mean"],
                    regions[name1]["informal_std"],
                    regions[name2]["informal_count"],
                    regions[name2]["informal_mean"],
                    regions[name2]["informal_std"],
                )
                tests[f"{name1}_informais_{name2}_formais"] = t(
                    regions[name1]["informal_count"],
                    regions[name1]["informal_mean"],
                    regions[name1]["informal_std"],
                    regions[name2]["formal_count"],
                    regions[name2]["formal_mean"],
                    regions[name2]["formal_std"],
                )
                tests[f"{name1}_formais_{name2}_formais"] = t(
                    regions[name1]["formal_count"],
                    regions[name1]["formal_mean"],
                    regions[name1]["formal_std"],
                    regions[name2]["formal_count"],
                    regions[name2]["formal_mean"],
                    regions[name2]["formal_std"],
                )

    return tests


print(run_all_t_tests())
