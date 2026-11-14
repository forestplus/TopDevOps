"""Synthetic regression experiment for the TopDevOps MLflow lab."""
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("demo-regression")
X, y = make_regression(n_samples=1200, n_features=12, noise=18.0, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
for alpha in (0.1, 1.0, 10.0):
    with mlflow.start_run(run_name=f"ridge-alpha-{alpha}") as run:
        model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        metrics = {
            "mae": float(mean_absolute_error(y_test, pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
            "r2": float(r2_score(y_test, pred)),
        }
        mlflow.log_params({"model": "Ridge", "alpha": alpha, "n_features": X.shape[1], "train_rows": len(X_train)})
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(model, artifact_path="model", input_example=X_test[:3])
        print(f"Logged run {run.info.run_id}: {metrics}")
