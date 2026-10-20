import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("result.csv", index_col=0)

plt.boxplot(df["metric"], showfliers=False)
plt.title("Sequences metric values")
plt.ylabel("metric value")
plt.ylim(0.4, 1.3)
plt.savefig("boxplot.pdf", dpi=150)
