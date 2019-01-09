"""
This is a module containing time series classifiers
"""
import numpy as np
import pandas as pd
from xpandas.data_container import XSeries, XDataFrame
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted


class TSDummyClassifier(BaseEstimator):
    """ A dummy classifier to be used as a reference implementation.

    Parameters
    ----------
    strategy : str, default='most'
        A parameter defining the prediction strategy of the dummy classifier
        most: predicts the most frequent class in the dataset
        least: predicts the least frequent class in the dataset
    """
    def __init__(self, strategy='most'):
        self.strategy = strategy

    def fit(self, X, y):
        """ A reference implementation of a fitting function.

        Parameters
        ----------
        X : array-like, xpandas XDataFrame or XSeries, shape (n_samples, ...)
            The training input samples.
        y : array-like, xpandas XdataFrame Xseries, shape (n_samples,)
            The target values (class labels in classification)

        Returns
        -------
        self : object
            Returns self.
        """
        if isinstance(X, (XSeries, XDataFrame, pd.Series, pd.DataFrame)) or \
            isinstance(y, (XSeries, XDataFrame, pd.Series, pd.DataFrame)):
            # do custom checks as per fit() implementation requirements
            # checking that the first dimensions are equal and other basic stuff as per sklearn req.
            X, y = check_X_y(X, y, dtype=None, ensure_2d=False)
        else:
            # check as per sklearn default requirements
            X, y = check_X_y(X, y)
        # convert xpandas or pandas into primitive numpy array (implicit) and get counts
        unique, counts = np.unique(y, return_counts=True)
        # fitting (finding the value of dummy prediciton theta_) the model based on strategy
        if self.strategy == 'most':
            index = np.argmax(counts)
            self.theta_ = unique[index]
        elif self.strategy == 'least':
            index = np.argmin(counts)
            self.theta_ = unique[index]
        else:
            raise ValueError('Unknown Strategy')
        # let the model know that it is fitted
        self.is_fitted_ = True
        # `fit` should always return `self`
        return self

    def predict(self, X):
        """ A reference implementation of a predicting function.

        Parameters
        ----------
        X : array-like, xpandas XDataFrame or XSeries, shape (n_samples, ...)
            The training input samples.
        Returns
        -------
        y : ndarray, shape (n_samples,)
            Returns the dummy predictions
        """
        if isinstance(X, (XSeries, XDataFrame, pd.Series, pd.DataFrame)):
            # do custom checks as per predict() implementation requirements
            # basic stuff as per sklearn req.
            X = check_array(X, dtype=None, ensure_2d=False)
        else:
            # check as per sklearn default requirements
            X = check_array(X)
        check_is_fitted(self, 'is_fitted_')
        return np.ones(X.shape[0], dtype=np.int64) * self.theta_
