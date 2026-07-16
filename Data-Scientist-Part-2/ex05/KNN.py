import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


class DataSet:
    """Represents loaded training and test data"""
    def __init__(self, train: pd.DataFrame, test: pd.DataFrame) -> None:
        self.train: pd.DataFrame = train
        self.test: pd.DataFrame = test


class SplitData:
    """Represents split training and validation data"""
    def __init__(self, X_train: pd.DataFrame, X_val: pd.DataFrame, y_train: pd.Series, y_val: pd.Series, scaler: StandardScaler) -> None:
        self.X_train: pd.DataFrame = X_train
        self.X_val: pd.DataFrame = X_val
        self.y_train: pd.Series = y_train
        self.y_val: pd.Series = y_val
        self.scaler: StandardScaler = scaler


class Model:
    """Represents trained model with classifier and metrics"""
    def __init__(self, classifier: KNeighborsClassifier, accuracy: float, precision: float, recall: float, f1: float) -> None:
        self.classifier: KNeighborsClassifier = classifier
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

        if self.f1 >= 0.92:
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

        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train), columns=X_train.columns, index=X_train.index
        )
        X_val_scaled = pd.DataFrame(
            scaler.transform(X_val), columns=X_val.columns, index=X_val.index
        )

        return SplitData(X_train_scaled, X_val_scaled, y_train, y_val, scaler)

    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Error splitting data: {e}")
        return None


def find_best_k(sp: SplitData) -> tuple:
    """Find best k value by testing k from 1 to 30"""
    try:
        if sp is None:
            raise ValueError("Split data is None")

        accuracies = []

        for k in range(1, 30):
            knn = KNeighborsClassifier(n_neighbors=k)
            knn.fit(sp.X_train, sp.y_train)
            predictions = knn.predict(sp.X_val)
            accuracy = accuracy_score(sp.y_val, predictions)
            accuracies.append(accuracy)
            print(f"k={k}: accuracy={accuracy:.4f}")

        best_k = accuracies.index(max(accuracies)) + 1
        best_accuracy = max(accuracies)

        print(f"\nBest k: {best_k} with accuracy: {best_accuracy:.4f}")

        return best_k, accuracies

    except Exception as e:
        print(f"Error finding best k: {e}")
        return None, []


def display_chart(accuracies: list) -> None:
    """Plot accuracy vs k values"""
    try:
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, 30), accuracies, marker='o', linestyle='-', linewidth=2, markersize=4)
        plt.xlabel('k values', fontsize=12)
        plt.ylabel('accuracy', fontsize=12)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error plotting: {e}")
    except KeyboardInterrupt:
        pass


def train_and_evaluate(split_data: SplitData, best_k: int) -> Model:
    """Train KNN model with best k and return model with metrics"""
    try:
        if split_data is None:
            raise ValueError("Split data is None")

        model = KNeighborsClassifier(n_neighbors=best_k)
        model.fit(split_data.X_train, split_data.y_train)

        predictions = model.predict(split_data.X_val)

        return Model(
            classifier=model,
            accuracy=accuracy_score(split_data.y_val, predictions),
            precision=precision_score(split_data.y_val, predictions, average='weighted'),
            recall=recall_score(split_data.y_val, predictions, average='weighted'),
            f1=f1_score(split_data.y_val, predictions, average='weighted')
        )

    except ValueError as e:
        print(f"ValueError: {e}")
        return None
    except Exception as e:
        print(f"Error training model: {e}")
        return None


def save_predictions(model: Model, dataset: DataSet, scaler: StandardScaler) -> None:
    """Generate predictions and save to KNN.txt"""
    try:
        if model is None:
            raise ValueError("Model is None")

        if dataset is None:
            raise ValueError("Dataset is None")

        test_scaled = pd.DataFrame(
            scaler.transform(dataset.test), columns=dataset.test.columns, index=dataset.test.index
        )
        predictions = model.classifier.predict(test_scaled)

        with open("KNN.txt", "w") as f:
            for pred in predictions:
                f.write(f"{pred}\n")

        print("\n✅ Predictions saved to KNN.txt")

    except ValueError as e:
        print(f"ValueError: {e}")
    except IOError as e:
        print(f"IOError: Cannot write to KNN.txt - {e}")
    except Exception as e:
        print(f"Error saving predictions: {e}")


def main() -> None:
    """Predict the knight's alignment using KNN and find best k value."""
    try:
        if len(sys.argv) != 3:
            raise ValueError("Usage: python3 KNN.py <Train_knight.csv> <Test_knight.csv>")

        train_path = sys.argv[1]
        test_path = sys.argv[2]

        dataset = load_data(train_path, test_path)
        if dataset is None:
            sys.exit(1)

        sp = split_data(dataset)
        if sp is None:
            sys.exit(1)

        best_k, accuracies = find_best_k(sp)
        if best_k is None:
            sys.exit(1)

        display_chart(accuracies)

        model = train_and_evaluate(sp, best_k)
        if model is None:
            sys.exit(1)

        model.print_metrics()

        save_predictions(model, dataset, sp.scaler)

    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()