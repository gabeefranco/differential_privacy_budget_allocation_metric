import numpy as np


def epsilon_dp(x, epsilon, sensitivity):
    return x + np.random.laplace(loc=0, scale=(sensitivity / epsilon))


if __name__ == "__main__":
    from data import get_regions

    regions = get_regions()

    result = regions["Sul"]["informal_count"]

    epsilon = 1
    # count query
    sensitivity = 1

    query_count = 10
    for i in range(query_count):
        print(epsilon_dp(result, epsilon / query_count, sensitivity))
