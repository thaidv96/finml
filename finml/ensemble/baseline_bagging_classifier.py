from copy import deepcopy
from ..data_sampler.pseudo_sequential_bootstrap import pseudo_sequential_bootstrap
import numpy as np

class BaselineBaggingClassifier:
    def __init__(self, estimator, n_estimators=10, max_samples=100):
        self.estimators = [deepcopy(estimator) for _ in range(n_estimators)]
        self.max_samples = max_samples
    def fit(self, X, y, features=None):
        if not features:
            features = X.columns
        for estimator in self.estimators:
            idx = pseudo_sequential_bootstrap(X, self.max_samples)
            estimator.fit(X.loc[idx, features], y.loc[idx])
        return self
    def predict_proba(self, X):
        return np.mean([estimator.predict_proba(X) for estimator in self.estimators], axis=0)


