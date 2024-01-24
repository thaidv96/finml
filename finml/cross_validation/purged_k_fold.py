from sklearn.model_selection._split import _BaseKFold
import numpy as np

class PurgedKFold(_BaseKFold):
    """
    Extend KFold to work with labels that span intervals
    The train is purged of observations overlapping test-label intervals
    Test set is assumed contiguous (shuffle=False), w/o training samples in between
    """
    def __init__(self, n_splits=3 , pct_embargo=0.):
        super(PurgedKFold, self).__init__(n_splits, shuffle=False, random_state=None)
        self.pct_embargo = pct_embargo
        self.n_splits = n_splits

    def split(self, X, y=None, groups=None):
        mbrg = int(X.shape[0] * self.pct_embargo)
        test_starts = [(i[0], i[-1] + 1) for i in np.array_split(np.arange(X.shape[0]), self.n_splits)]
        for i, j in test_starts:
            t0 = X.index[i] # start of test set
            if j+mbrg <= X.shape[0]:
                t1 = X.index[j+mbrg]
            else:
                t1 = X.index[-1]
            test_indices = X.index[i:j]
            # Left part
            train_indices = X[X['t1']<t0].index.tolist()
            # Right part
            start_right_index = X[t1:].index[0]
            train_indices += X[start_right_index:].index.tolist()
            yield train_indices, test_indices