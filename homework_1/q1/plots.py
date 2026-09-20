import pandas as pd
import matplotlib.pyplot as plt

scan_a = pd.read_csv("scan_posA.csv")
scan_b = pd.read_csv("scan_posB.csv")

plt.scatter(scan_a["x"], scan_a["y"], s=3, label="Scan A")
plt.scatter(scan_b["x"], scan_b["y"], s=3, label="Scan B")

plt.xlabel("x (m)")
plt.ylabel("y (m)")
plt.axis("equal")
plt.legend()
plt.grid()

plt.show()
