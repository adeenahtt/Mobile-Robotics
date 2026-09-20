import pandas as pd
import matplotlib.pyplot as plt

scanA = pd.read_csv("scan_posA.csv")
scanB = pd.read_csv("scan_posB.csv")

# Transform Scan B into Scan A's coordinate frame

theta = 180

scanB["x_transformed"] = -scanB["x"]
scanB["y_transformed"] = -scanB["y"] + 1.4

plt.scatter(scanA["x"], scanA["y"], s=5, label="Scan A")

plt.scatter(
    scanB["x_transformed"],
    scanB["y_transformed"],
    s=5,
    label="Transformed Scan B"
)

plt.axis("equal")
plt.legend()
plt.show()
