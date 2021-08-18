'''
Linear regression

Rhedintza Audryna

Main file for linear regression and model selection.
'''

import numpy as np
from sklearn.model_selection import train_test_split
import util


class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Class for representing a dataset, performs train/test
        splitting.

        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        parameters_dict = util.load_json_file(dir_path, "parameters.json")
        self.pred_vars = parameters_dict["predictor_vars"]
        self.name = parameters_dict["name"]
        self.dependent_var = parameters_dict["dependent_var"]
        self.training_fraction = parameters_dict["training_fraction"]
        self.seed = parameters_dict["seed"]
        self.labels, data = util.load_numpy_array(dir_path, "data.csv")
        self.training_data, self.testing_data = train_test_split(data,
                                                                 train_size=self.training_fraction, test_size=None,
                                                                 random_state=self.seed)


class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.

        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns (of the
              original data array) used in the model.
        '''

        self.labels = dataset.labels
        self.pred_vars = pred_vars
        self.dep_var = dataset.dependent_var
        self.y_n = dataset.training_data[:, self.dep_var]
        self.X = util.prepend_ones_column(
            dataset.training_data[:, self.pred_vars])
        self.beta = util.linear_regression(self.X, self.y_n)
        self.R2 = self.get_R2(self.y_n, self.X)

    def get_R2(self, y_n, X):
        '''
        Calculates the R-squared of the model

        Inputs: 
            y_n: (array) array of actual dependent variable values
            X: (array) 2D array of predictor variable values with prepended 1s column

        Returns: 
            (float) R-squared of the model
        '''

        yhats = util.apply_beta(self.beta, X)

        numerator = np.sum((y_n - yhats) ** 2)
        denominator = np.sum((y_n - np.mean(y_n)) ** 2)

        return 1 - numerator / denominator

    def __repr__(self):
        '''
        Format model as a string.
        '''

        s = "{} ~ {}".format(self.labels[self.dep_var], round(self.beta[0], 6))

        for i, var in enumerate(self.pred_vars):
            if self.beta[i+1] < 0:
                s = s + \
                    " - {} * {}".format(abs(round(self.beta[i+1], 6)),
                                        self.labels[var])
            elif self.beta[i+1] > 0:
                s = s + \
                    " + {} * {}".format(round(self.beta[i+1], 6),
                                        self.labels[var])

        return s


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''

    models = [Model(dataset, [pred_var]) for pred_var in dataset.pred_vars]

    return models


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''

    model = Model(dataset, dataset.pred_vars)

    return model


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''

    max_model = None
    max_R2 = 0

    for i, v1 in enumerate(dataset.pred_vars):
        for v2 in dataset.pred_vars[i+1:]:
            model = Model(dataset, [v1, v2])
            if model.R2 > max_R2:
                max_model = model
                max_R2 = model.R2

    return max_model


def forward_selection(dataset):
    '''
    Given a dataset with P predictor variables, uses forward selection to
    select models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''

    models = []
    pred_vars_avail = dataset.pred_vars[:]
    pred_vars_used = []
    num_vars = len(dataset.pred_vars)

    for _ in range(num_vars):
        max_R2 = 0
        max_model = None
        max_variable = None
        for var in pred_vars_avail:
            model = Model(dataset, pred_vars_used + [var])
            if model.R2 > max_R2:
                max_model = model
                max_R2 = model.R2
                max_variable = var
        pred_vars_used.append(max_variable)
        pred_vars_avail.remove(max_variable)
        models.append(max_model)

    return models


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''

    y_n = dataset.testing_data[:, model.dep_var]
    X = util.prepend_ones_column(dataset.testing_data[:, model.pred_vars])

    return model.get_R2(y_n, X)
