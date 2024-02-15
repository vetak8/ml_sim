from typing import Callable, Union, Tuple
import numpy as np
from sklearn.tree import DecisionTreeRegressor

class GradientBoostingRegressor:
    '''
    Функция реализует градиентный бустинг
    '''
    def __init__(
        self,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        min_samples_split=2,
        loss="mse",
        verbose=False,
    ):
        self.trees_ = []
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.loss = loss
        self.verbose = verbose
        self.base_pred_ = None

    def _mse(self,y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[float, np.ndarray]:
        """Mean squared error loss function and gradient."""
        error = y_pred - y_true
        loss = np.mean(error ** 2)
        grad = error
        return loss, grad

    def _validate_loss_function(self, loss: Union[str, Callable]) -> Callable:
        '''Validate loss function'''
        if isinstance(loss, str):
            if loss == 'mse':
                return self._mse
        elif callable(loss):
            return loss
        else:
            raise ValueError('Loss must be a callable function')

    def fit(self, X: np.ndarray, y: np.ndarray) -> 'GradientBoostingRegressor':
        """Fit the model to the data."""
        self.base_pred_ = np.mean(y)
        y_pred = np.full_like(y, self.base_pred_, dtype=np.float64)


        loss_func = self._validate_loss_function(self.loss)

        for _ in range(self.n_estimators):
            loss, grad = loss_func(y, y_pred)
            tree = DecisionTreeRegressor(max_depth=self.max_depth,
                                          min_samples_split=self.min_samples_split)
            tree.fit(X, -grad)
            self.trees_.append(tree)
            y_pred += self.learning_rate * tree.predict(X)
            
            if self.verbose:
                print(f"Iteration: {_ + 1}, Loss: {loss}")
        
        return self

    def predict(self, X):
        """Predict the target of new data.

        Args:
            X: array-like of shape (n_samples, n_features)

        Returns:
            y: array-like of shape (n_samples,)
            The predict values.

        """
        predictions = np.full(X.shape[0], self.base_pred_)
        for tree in self.trees_:
            predictions += self.learning_rate * tree.predict(X)
        return predictions

if __name__ == '__main__':
    
