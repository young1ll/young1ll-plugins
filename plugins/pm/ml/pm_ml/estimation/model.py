"""ML model for task estimation prediction."""

from typing import Dict, List, Any, Optional
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle
from pathlib import Path

from .features import extract_features, calculate_complexity_score


class EstimationModel:
    """Random Forest model for predicting task story points"""

    def __init__(self, model_path: Optional[Path] = None):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
        )
        self.scaler = StandardScaler()
        self.feature_names: List[str] = []
        self.is_trained = False

        if model_path and model_path.exists():
            self.load(model_path)

    def train(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Train model on historical tasks.

        Args:
            tasks: List of completed tasks with actual estimates

        Returns:
            Training metrics
        """
        # Filter tasks with valid estimates
        valid_tasks = [
            t for t in tasks
            if t.get("estimate_points") and t.get("estimate_points") > 0
        ]

        if len(valid_tasks) < 10:
            return {
                "error": "Need at least 10 tasks with estimates to train",
                "count": len(valid_tasks),
            }

        # Extract features
        X = []
        y = []

        for task in valid_tasks:
            features = extract_features(task, valid_tasks)
            X.append(list(features.values()))
            y.append(task["estimate_points"])

            if not self.feature_names:
                self.feature_names = list(features.keys())

        X = np.array(X)
        y = np.array(y)

        # Normalize features
        X_scaled = self.scaler.fit_transform(X)

        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True

        # Calculate training metrics
        train_score = self.model.score(X_scaled, y)
        predictions = self.model.predict(X_scaled)
        mae = np.mean(np.abs(predictions - y))

        return {
            "trained": True,
            "samples": len(valid_tasks),
            "r2_score": float(train_score),
            "mae": float(mae),
            "feature_count": len(self.feature_names),
        }

    def predict(
        self,
        task: Dict[str, Any],
        historical_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Predict story points for a task.

        Args:
            task: Task to estimate
            historical_tasks: Historical tasks for context

        Returns:
            Prediction result with confidence
        """
        if not self.is_trained:
            # Fallback to rule-based estimation
            complexity = calculate_complexity_score(task)
            return {
                "predicted_points": round(complexity),
                "confidence": 0.5,
                "method": "rule-based",
                "complexity_score": complexity,
            }

        # Extract features
        features = extract_features(task, historical_tasks)
        X = np.array([list(features.values())])
        X_scaled = self.scaler.transform(X)

        # Predict
        prediction = self.model.predict(X_scaled)[0]

        # Calculate confidence from tree variance
        tree_predictions = [tree.predict(X_scaled)[0] for tree in self.model.estimators_]
        std = np.std(tree_predictions)
        confidence = 1.0 / (1.0 + std)  # Higher std = lower confidence

        return {
            "predicted_points": round(prediction),
            "confidence": float(confidence),
            "method": "ml",
            "complexity_score": calculate_complexity_score(task),
            "raw_prediction": float(prediction),
        }

    def suggest_buffer(
        self,
        task: Dict[str, Any],
        historical_tasks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Suggest buffer time based on risk factors.

        Args:
            task: Task to analyze
            historical_tasks: Historical tasks for context

        Returns:
            Buffer suggestion
        """
        prediction_result = self.predict(task, historical_tasks)
        predicted_points = prediction_result["predicted_points"]
        confidence = prediction_result["confidence"]

        # Calculate buffer percentage based on confidence and complexity
        complexity = prediction_result["complexity_score"]

        # Lower confidence = higher buffer
        confidence_factor = (1.0 - confidence) * 0.3

        # Higher complexity = higher buffer
        complexity_factor = (complexity / 10.0) * 0.2

        buffer_percentage = confidence_factor + complexity_factor
        buffer_points = round(predicted_points * buffer_percentage)

        return {
            "base_estimate": predicted_points,
            "buffer_points": max(buffer_points, 1),
            "total_estimate": predicted_points + max(buffer_points, 1),
            "buffer_percentage": round(buffer_percentage * 100, 1),
            "confidence": confidence,
            "complexity": complexity,
        }

    def save(self, path: Path):
        """Save model to disk"""
        with open(path, "wb") as f:
            pickle.dump({
                "model": self.model,
                "scaler": self.scaler,
                "feature_names": self.feature_names,
                "is_trained": self.is_trained,
            }, f)

    def load(self, path: Path):
        """Load model from disk"""
        with open(path, "rb") as f:
            data = pickle.load(f)
            self.model = data["model"]
            self.scaler = data["scaler"]
            self.feature_names = data["feature_names"]
            self.is_trained = data["is_trained"]
