"""
Referral Success Prediction Model
AI Powered Smart Hospital Referral System
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_validate
from sklearn.model_selection import RandomizedSearchCV

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

from sklearn.model_selection import (
    train_test_split
)

from src.preprocessing.preprocess import (
    prepare_referral_dataset
)


# ----------------------------------------
# Load Prepared Dataset
# ----------------------------------------

X, y = prepare_referral_dataset()

print("Dataset Shape")
print("X:", X.shape)
print("y:", y.shape)


# ----------------------------------------
# Train-Test Split
# ----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ----------------------------------------
# Display Split
# ----------------------------------------

print("\nTRAINING DATA")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTEST DATA")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)


# ----------------------------------------
# Target Distribution
# ----------------------------------------

print("\nTraining Target Distribution")

print(
    y_train
    .value_counts(
        normalize=True
    )
    .mul(100)
    .round(2)
)


print("\nTest Target Distribution")

print(
    y_test
    .value_counts(
        normalize=True
    )
    .mul(100)
    .round(2)
)


# ----------------------------------------
# Baseline Model
# Logistic Regression + Scaling
# ----------------------------------------

model = Pipeline([
    (
        "scaler",
        StandardScaler()
    ),

    (
        "logistic_regression",
        LogisticRegression(
            max_iter=2000,
            random_state=42
        )
    )
])


# ----------------------------------------
# Training
# ----------------------------------------

model.fit(
    X_train,
    y_train
)


# ----------------------------------------
# Predictions
# ----------------------------------------

y_pred = model.predict(
    X_test
)

y_probability = model.predict_proba(
    X_test
)[:, 1]


# ----------------------------------------
# Model Performance
# ----------------------------------------

print("\n==============================")
print("LOGISTIC REGRESSION")
print("==============================")


print(
    "Accuracy:",
    round(
        accuracy_score(
            y_test,
            y_pred
        ),
        4
    )
)


print(
    "Precision:",
    round(
        precision_score(
            y_test,
            y_pred
        ),
        4
    )
)


print(
    "Recall:",
    round(
        recall_score(
            y_test,
            y_pred
        ),
        4
    )
)


print(
    "F1 Score:",
    round(
        f1_score(
            y_test,
            y_pred
        ),
        4
    )
)


print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            y_probability
        ),
        4
    )
)


# ----------------------------------------
# Classification Report
# ----------------------------------------

print("\nClassification Report")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# ----------------------------------------
# Confusion Matrix
# ----------------------------------------

print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)

# ----------------------------------------
# Random Forest Model
# ----------------------------------------

rf_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    min_samples_leaf=5,
    random_state=42,
    n_jobs=-1
)


# ----------------------------------------
# Training
# ----------------------------------------

rf_model.fit(
    X_train,
    y_train
)


# ----------------------------------------
# Predictions
# ----------------------------------------

rf_pred = rf_model.predict(
    X_test
)

rf_probability = rf_model.predict_proba(
    X_test
)[:, 1]


# ----------------------------------------
# Evaluation
# ----------------------------------------

print("\n==============================")
print("RANDOM FOREST")
print("==============================")


print(
    "Accuracy:",
    round(
        accuracy_score(
            y_test,
            rf_pred
        ),
        4
    )
)


print(
    "Precision:",
    round(
        precision_score(
            y_test,
            rf_pred
        ),
        4
    )
)


print(
    "Recall:",
    round(
        recall_score(
            y_test,
            rf_pred
        ),
        4
    )
)


print(
    "F1 Score:",
    round(
        f1_score(
            y_test,
            rf_pred
        ),
        4
    )
)


print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            rf_probability
        ),
        4
    )
)


# ----------------------------------------
# Classification Report
# ----------------------------------------

print("\nRandom Forest Classification Report")

print(
    classification_report(
        y_test,
        rf_pred
    )
)


# ----------------------------------------
# Confusion Matrix
# ----------------------------------------

print("\nRandom Forest Confusion Matrix")

print(
    confusion_matrix(
        y_test,
        rf_pred
    )
)

# ----------------------------------------
# Random Forest Feature Importance
# ----------------------------------------

feature_importance = pd.DataFrame({
    "feature": X_train.columns,
    "importance": rf_model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("\n==============================")
print("TOP 15 FEATURE IMPORTANCE")
print("==============================")

print(
    feature_importance.head(15).to_string(
        index=False
    )
)

# ----------------------------------------
# Ablation Study
# ----------------------------------------

print("\n==============================")
print("ABLATION STUDY")
print("==============================")


def train_ablation_model(
    X,
    y,
    remove_features,
    model_name
):

    X_ablation = X.drop(
        columns=remove_features,
        errors="ignore"
    )

    X_train_a, X_test_a, y_train_a, y_test_a = train_test_split(
        X_ablation,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    model_a = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    )

    model_a.fit(
        X_train_a,
        y_train_a
    )

    pred_a = model_a.predict(
        X_test_a
    )

    prob_a = model_a.predict_proba(
        X_test_a
    )[:, 1]

    accuracy = accuracy_score(
        y_test_a,
        pred_a
    )

    f1 = f1_score(
        y_test_a,
        pred_a
    )

    roc_auc = roc_auc_score(
        y_test_a,
        prob_a
    )

    print(f"\n{model_name}")

    print(
        "Features:",
        X_ablation.shape[1]
    )

    print(
        "Accuracy:",
        round(accuracy, 4)
    )

    print(
        "F1:",
        round(f1, 4)
    )

    print(
        "ROC-AUC:",
        round(roc_auc, 4)
    )

    return {
        "model": model_name,
        "features": X_ablation.shape[1],
        "accuracy": accuracy,
        "f1": f1,
        "roc_auc": roc_auc
    }

# ----------------------------------------
# Cross Validation
# ----------------------------------------

print("\n==============================")
print("5-FOLD CROSS VALIDATION")
print("==============================")


cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


cv_scores = cross_validate(
    rf_model,
    X,
    y,
    cv=cv,
    scoring=[
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc"
    ],
    n_jobs=-1
)


print("\nCross Validation Results")


print(
    "Accuracy:",
    round(
        cv_scores["test_accuracy"].mean(),
        4
    ),
    "+/-",
    round(
        cv_scores["test_accuracy"].std(),
        4
    )
)


print(
    "Precision:",
    round(
        cv_scores["test_precision"].mean(),
        4
    ),
    "+/-",
    round(
        cv_scores["test_precision"].std(),
        4
    )
)


print(
    "Recall:",
    round(
        cv_scores["test_recall"].mean(),
        4
    ),
    "+/-",
    round(
        cv_scores["test_recall"].std(),
        4
    )
)


print(
    "F1:",
    round(
        cv_scores["test_f1"].mean(),
        4
    ),
    "+/-",
    round(
        cv_scores["test_f1"].std(),
        4
    )
)


print(
    "ROC-AUC:",
    round(
        cv_scores["test_roc_auc"].mean(),
        4
    ),
    "+/-",
    round(
        cv_scores["test_roc_auc"].std(),
        4
    )
)

# ----------------------------------------
# Random Forest Hyperparameter Tuning
# ----------------------------------------

print("\n==============================")
print("RANDOM FOREST HYPERPARAMETER TUNING")
print("==============================")


param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [8, 12, 16, 20, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 5, 10],
    "max_features": ["sqrt", "log2"]
}


rf_base = RandomForestClassifier(
    random_state=42,
    n_jobs=-1
)


search = RandomizedSearchCV(
    estimator=rf_base,
    param_distributions=param_grid,
    n_iter=10,
    scoring="f1",
    cv=3,
    random_state=42,
    n_jobs=-1,
    verbose=1
)


search.fit(
    X_train,
    y_train
)


print("\nBEST PARAMETERS")

print(
    search.best_params_
)


print("\nBEST CV F1")

print(
    round(
        search.best_score_,
        4
    )
)


best_rf = search.best_estimator_

# ----------------------------------------
# Final Tuned Model Evaluation
# ----------------------------------------

tuned_pred = best_rf.predict(
    X_test
)

tuned_probability = best_rf.predict_proba(
    X_test
)[:, 1]


print("\n==============================")
print("TUNED RANDOM FOREST")
print("==============================")


print(
    "Accuracy:",
    round(
        accuracy_score(
            y_test,
            tuned_pred
        ),
        4
    )
)


print(
    "Precision:",
    round(
        precision_score(
            y_test,
            tuned_pred
        ),
        4
    )
)


print(
    "Recall:",
    round(
        recall_score(
            y_test,
            tuned_pred
        ),
        4
    )
)


print(
    "F1 Score:",
    round(
        f1_score(
            y_test,
            tuned_pred
        ),
        4
    )
)


print(
    "ROC-AUC:",
    round(
        roc_auc_score(
            y_test,
            tuned_probability
        ),
        4
    )
)


print("\nConfusion Matrix")

print(
    confusion_matrix(
        y_test,
        tuned_pred
    )
)