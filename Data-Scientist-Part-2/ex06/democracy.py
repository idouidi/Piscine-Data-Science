import sys
import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class DataSet:
    """Represents loaded training and test data"""
    def __init__(self, train: pd.DataFrame, test: pd.DataFrame) -> None:
        self.train: pd.DataFrame = train
        self.test: pd.DataFrame = test


class SplitData:
    """Represents split training and validation data"""
    def __init__(self, X_train: pd.DataFrame, X_val: pd.DataFrame, y_train: pd.Series, y_val: pd.Series) -> None:
        self.X_train: pd.DataFrame = X_train
        self.X_val: pd.DataFrame = X_val
        self.y_train: pd.Series = y_train
        self.y_val: pd.Series = y_val


class Model:
    """Represents trained model with classifier and metrics"""
    def __init__(self, classifier: VotingClassifier, accuracy: float, precision: float, recall: float, f1: float) -> None:
        self.classifier: VotingClassifier = classifier
        self.accuracy: float = accuracy
        self.precision: float = precision
        self.recall: float = recall
        self.f1: float = f1

    def print_metrics(self) -> None:
        """Display metrics"""
        print(f"accuracy:  {self.accuracy:.4f}")
        print(f"precision: {self.precision:.4f}")
        print(f"recall:    {self.recall:.4f}")
        print(f"f1_score:  {self.f1:.4f}")

        if self.f1 >= 0.94:
            print("✅ F1-Score requirement: PASSED")
        else:
            print("⚠️  F1-Score requirement: FAILED")


def load_data(train_path: str, test_path: str) -> DataSet:
    """Load train and test data"""
    try:
        if not isinstance(train_path, str) or not isinstance(test_path, str):
            raise TypeError("Paths must be strings")

        if not os.path.exists(train_path) or not os.path.exists(test_path):
            raise FileNotFoundError(f"File does not exist: {train_path} or {test_path}")

        if not os.path.isfile(train_path) or not os.path.isfile(test_path):
            raise ValueError(f"Not a file: {train_path} or {test_path}")

        if not train_path.lower().endswith(".csv") or not test_path.lower().endswith(".csv"):
            raise ValueError(f"Files must be CSV format: {train_path} or {test_path}")

        df_train = pd.read_csv(train_path)
        df_test = pd.read_csv(test_path)

        df_train.columns = df_train.columns.str.strip()
        df_test.columns = df_test.columns.str.strip()

        return DataSet(df_train, df_test)

    except TypeError as e:
        print(f"TypeError: {e}")
        return None
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}")
        return None
    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Error loading files: {e}")
        return None


def split_data(dataset: DataSet) -> SplitData:
    """Split training data into 70% training and 30% validation"""
    try:
        if dataset is None:
            raise ValueError("Dataset is None")

        if "knight" not in dataset.train.columns:
            raise ValueError("'knight' column not found in training data")

        X = dataset.train.drop(columns="knight")
        y = dataset.train["knight"]

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.30, random_state=42
        )

        return SplitData(X_train, X_val, y_train, y_val)

    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Error splitting data: {e}")
        return None


def train_and_evaluate(sp: SplitData) -> Model:
    """Train a Voting classifier (KNN + Logistic Regression + Random Forest) and return model with metrics"""
    try:
        if sp is None:
            raise ValueError("Split data is None")

        knn = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=8))
        ])
        log_reg = Pipeline([
            ("scaler", StandardScaler()),
            ("log_reg", LogisticRegression(max_iter=1000))
        ])
        forest = RandomForestClassifier(n_estimators=100, random_state=42)

        model = VotingClassifier(
            estimators=[("knn", knn), ("log_reg", log_reg), ("forest", forest)],
            voting="hard"
        )
        model.fit(sp.X_train, sp.y_train)

        predictions = model.predict(sp.X_val)

        return Model(
            classifier=model,
            accuracy=accuracy_score(sp.y_val, predictions),
            precision=precision_score(sp.y_val, predictions, average='weighted'),
            recall=recall_score(sp.y_val, predictions, average='weighted'),
            f1=f1_score(sp.y_val, predictions, average='weighted')
        )

    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Error training model: {e}")
        return None


def save_predictions(model: Model, dataset: DataSet) -> None:
    """Generate predictions and save to Voting.txt"""
    try:
        if model is None:
            raise ValueError("Model is None")

        if dataset is None:
            raise ValueError("Dataset is None")

        predictions = model.classifier.predict(dataset.test)

        with open("Voting.txt", "w") as f:
            for pred in predictions:
                f.write(f"{pred}\n")

    except ValueError as e:
        print(f"ValueError: {e}")
    except IOError as e:
        print(f"IOError: Cannot write to Voting.txt - {e}")
    except Exception as e:
        print(f"Error saving predictions: {e}")


def main() -> None:
    """Predict the knight's alignment using a Voting classifier."""
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python3 democracy.py <Train_knight.csv> <Test_knight.csv>")

        train_path = sys.argv[1]
        test_path = sys.argv[2]

        dataset = load_data(train_path, test_path)
        if dataset is None:
            sys.exit(1)

        sp = split_data(dataset)
        if sp is None:
            sys.exit(1)

        model = train_and_evaluate(sp)
        if model is None:
            sys.exit(1)

        model.print_metrics()

        save_predictions(model, dataset)

    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
