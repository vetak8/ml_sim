from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class Node:
    """Decision tree node."""
    feature: int = None
    threshold: float = None
    n_samples: int = None
    left: Node = None
    right: Node = None
    mse: float = None
    value: int = None


@dataclass
class DecisionTreeRegressor:
    """Decision tree regressor."""
    max_depth: int
    min_samples_split: int = 2

    def fit(self, X: np.ndarray, y: np.ndarray) -> DecisionTreeRegressor:
        """Build a decision tree regressor from the training set (X, y)."""
        self.n_features_ = X.shape[1]
        self.tree_ = self._split_node(X, y)
        return self

    def _mse(self, y: np.ndarray) -> float:
        """Compute the mse criterion for a given set of target values."""
        squared_error = np.square(y - np.mean(y))
        return np.mean(squared_error)

    def _weighted_mse(self, y_left: np.ndarray, y_right: np.ndarray) -> float:
        """Compute the weighted mse criterion for a two given sets of target values"""
        n = len(y_left) + len(y_right)
        mse_left = self._mse(y_left)
        mse_right = self._mse(y_right)
        return (mse_left * len(y_left)) / n + (mse_right * len(y_right)) / n

    def _split(self, X: np.ndarray, y: np.ndarray, feature: int) -> float:
        """Find the best split for a node (one feature)"""
        best_threshold = None
        best_metric = float('inf')

        unique_values = np.unique(X[:, feature])
        if len(unique_values) == 1:
            return None, None  # Handle case where all values are the same

        for split_value in unique_values:
            left_indices = X[:, feature] <= split_value
            right_indices = X[:, feature] > split_value

            left_y, right_y = y[left_indices], y[right_indices]
            metric = self._weighted_mse(left_y, right_y)

            if metric < best_metric:
                best_metric = metric
                best_threshold = split_value
        return best_threshold, best_metric

    def _best_split(self, X: np.ndarray, y: np.ndarray) -> tuple[int, float]:
        """Find the best split for a node (one feature)"""
        best_feature = None
        best_threshold = None
        best_metric = float('inf')
        same_values_y = np.all(y == y[0])

        for feature in range(X.shape[1]):
            threshold, metric = self._split(X, y, feature)
            if same_values_y or metric is None:
                continue
            if metric < best_metric:
                best_metric = metric
                best_feature = feature
                best_threshold = threshold
        return best_feature, best_threshold


    def _split_node(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> Node:
        """Split a node and return the resulting left and right child nodes."""
        if depth == self.max_depth or len(X) < self.min_samples_split:
            return Node(
                feature=None,
                threshold=None,
                n_samples=len(X),
                value=int(np.round(np.mean(y))),  # Use mean value of y for leaf node
                mse=self._mse(y)
            )

        if len(np.unique(y)) == 1:
            # All target values are the same, return leaf node with the mean value of y
            return Node(
                feature=None,
                threshold=None,
                n_samples=len(X),
                value=int(np.round(np.mean(y))),
                mse=self._mse(y)
            )

        best_feature, best_threshold = self._best_split(X, y)
        left_indices = X[:, best_feature] <= best_threshold
        right_indices = ~left_indices
        left_node = self._split_node(X[left_indices], y[left_indices], depth + 1)
        right_node = self._split_node(X[right_indices], y[right_indices], depth + 1)
        return Node(feature=best_feature,
                    threshold=best_threshold,
                    n_samples=len(X),
                    mse=self._mse(y),
                    value=int(np.round(np.mean(y))),
                    left=left_node,
                    right=right_node)
        
    def as_json(self) -> str:
        """Convert the decision tree to a JSON-like string."""
        return self._as_json(self.tree_)
    
    def _as_json(self, node: Node) -> str:
        """Recursively convert the decision tree node to a JSON-like string."""
        if node.left is None and node.right is None:
            # Leaf node
            return f'{{"value": {node.value}, "n_samples": {node.n_samples}, "mse": {node.mse:.2f}}}'
        else:
            # Internal node
            left_json = self._as_json(node.left)
            right_json = self._as_json(node.right)
            return f'{{"feature": {node.feature}, "threshold": {node.threshold}, "n_samples": {node.n_samples}, "mse": {node.mse:.2f}, "left": {left_json}, "right": {right_json}}}'
            
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict regression target for X.
    
        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            The input samples.
    
        Returns
        -------
        y : array of shape (n_samples,)
            The predicted values.
        """
        predictions = np.array([self._predict_one_sample(sample) for sample in X])
        return predictions
    
    
    def _predict_one_sample(self, features: np.ndarray) -> int:
        """Predict the target value of a single sample."""
        return self._traverse_tree(self.tree_, features)
    
    
    def _traverse_tree(self, node: Node, features: np.ndarray) -> int:
        """Traverse the decision tree to predict the target value."""
        if node.left is None and node.right is None:
            # Leaf node, return the value
            return node.value
        else:
            if features[node.feature] <= node.threshold:
                return self._traverse_tree(node.left, features)
            else:
                return self._traverse_tree(node.right, features)

    
