"""import pandas as pd
import matplotlib.pyplot as plt

# load real snapshot data
df = pd.read_csv("data/processed/modeling_table.csv", parse_dates=["snapshot_date"])

# pick a real snapshot from the middle
row = df.sort_values("snapshot_date").iloc[len(df)//2]
snapshot = row["snapshot_date"]

feature_start = snapshot - pd.DateOffset(months=6)
label_end = snapshot + pd.DateOffset(months=2)

plt.figure(figsize=(8, 2))
plt.plot([feature_start, snapshot], [1, 1])
plt.plot([snapshot, label_end], [1, 1])
plt.scatter([snapshot], [1])
plt.yticks([])
plt.xlabel("Time")
plt.title("Time-Aware Snapshot Design (Real Account Example)")
plt.tight_layout()
plt.savefig("temporal_backbone.png")
plt.show()"""


"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

train = pd.read_csv("data/processed/train.csv")

target = "label"
drop_cols = ["account_id", "snapshot_date", target]
features = [c for c in train.columns if c not in drop_cols]

X = pd.get_dummies(train[features], drop_first=True)
y = train[target]

pipe = Pipeline([("scaler", StandardScaler()),("model", LogisticRegression(max_iter=1000))])

pipe.fit(X, y)

coefs = pipe.named_steps["model"].coef_[0]

imp = (pd.DataFrame({
        "feature": X.columns,
        "importance": np.abs(coefs)
    }).sort_values("importance", ascending=False).head(15))

plt.figure(figsize=(6, 4))
plt.barh(imp["feature"], imp["importance"])
plt.gca().invert_yaxis()
plt.title("Top Feature Importances (Logistic Regression)")
plt.xlabel("Absolute Coefficient Magnitude")
plt.tight_layout()
plt.savefig("feature_importance.png")
plt.show()"""



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve

df = pd.read_csv("data/processed/val_with_preds.csv")

y_true = df["label"].values
y_score = df["pred_proba"].values

precision, recall, _ = precision_recall_curve(y_true, y_score)

plt.figure(figsize=(5, 4))
plt.plot(recall, precision)
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.title("Precision–Recall Curve (Validation Set)")
plt.tight_layout()
plt.savefig("precision_recall_curve.png")
plt.show()
