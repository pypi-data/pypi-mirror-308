import SALib.analyze.sobol
import SALib.sample.sobol
import sklearn
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
import sklearn.feature_selection as fs
import sklearn.model_selection as ms
import sklearn.preprocessing as preprocessing
import sklearn
import time
import tqdm
import json
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import SharedMemory
from typing import Tuple
from sklearn.base import clone
import multiprocessing as mp
from enum import IntEnum



"""
This script is the output of the research paper submitted to the Noise Control Engineering Journal. It permits the user
to supply the machine learners and the data to process into a series of accuracy, speed, and qualitative metrics to 
determine what learners are the best for the prediction of the data provided. To avoid the use of global parameters, 
a class is created to hold the information that is required to be passed between the various functions.
"""


def create_np_array_from_shared_mem(shared_mem: SharedMemory, shared_data_dtype: np.dtype,
                                    shared_data_shape: Tuple[int, ...]) -> np.ndarray:
    return np.ndarray(shape=shared_data_shape, dtype=shared_data_dtype, buffer=shared_mem.buf)


def get_learner_accuracy(args):
    """
    This function will extract the learner's accuracy from the arugments of the function.
    """

    #   TODO: Can we be more explicit in the arugments rather than using the array object, or is this a requirement for multi-threading?
    try:
        import warnings
        warnings.filterwarnings("ignore")

        #   Extract the objects from the argument passed to the function
        learner = args[0]
        names = args[1]
        sub = args[2]
        split = args[3]
        idx_train = args[4]
        idx_test = args[5]
        idx_feat = args[6]
        X = create_np_array_from_shared_mem(args[7][0], args[7][1], args[7][2])
        y = create_np_array_from_shared_mem(args[8][0], args[8][1], args[8][2])

        #   Get the information about the learner
        ll = LearnerLabel(learner)

        #   Scale the data using the standard scaler, which is used to facilitate the use of the normal distribution
        #   functions within the sensitivity analysis library.
        ss = preprocessing.StandardScaler()
        X_train = X[idx_train].copy()
        X_test = X[idx_test].copy()
        y_train = y[idx_train]
        y_test = y[idx_test]
        X_train_scaled = ss.fit_transform(X_train)
        X_test_scaled = ss.transform(X_test)

        #   Run the machine learning
        learner.fit(X_train_scaled[:, idx_feat], y_train)
        y_pred = learner.predict(X_test_scaled[:, idx_feat])
        accuracy = metrics.accuracy_score(y_test, y_pred)

        output = {'learner name': [], 'learner parameters': [], 'fold index': [], 'included': [], 'accuracy': []}
        for c in names:
            output[c] = []
        output['learner name'].append(ll.learner_name)
        output['learner parameters'].append(ll.learner_params_csvsafe)
        output['fold index'].append(split)
        output['included'].append(len(sub))
        for c in names:
            output[c].append(1 if c in sub else 0)
        output['accuracy'].append(accuracy)
        return pd.DataFrame(output)
    except Exception as ee:
        #   What would cause this exception to be thrown? We need to be more specific in the exception if possible.
        return repr(ee)

def run_rfe_sa(args):
    """
    Run recursive feature elimination with sensitivity analysis on a single learner.

    The Python "imap" function only allows for a single input parameter, 
    meaning all needed parameters must be passed within a single iterable.
    """
    try:
        import warnings
        warnings.filterwarnings("ignore")
        learner = args[0]
        min_features = args[1]
        names = args[2]
        split = args[3]
        idx_train = args[4]
        X = create_np_array_from_shared_mem(args[5][0], args[5][1], args[5][2])
        y = create_np_array_from_shared_mem(args[6][0], args[6][1], args[6][2])
        samples = args[7]
        jobs = args[8]

        ll = LearnerLabel(learner)
        if jobs > 0:
            params = ll.get_params()
            if 'n_jobs' in params:
                params['n_jobs'] = jobs
                ll.set_params(**params)
        ss = preprocessing.StandardScaler()
        X_train = X[idx_train]
        y_train = y[idx_train]
        X_train_scaled = ss.fit_transform(X_train)
        indices, x_local = [], X_train_scaled.copy()

        def get_importances(clf):
            nonlocal indices, x_local, names, samples, jobs
            x_copy = x_local.copy()
            names_copy = names.copy()
            for col in indices:
                x_copy = np.delete(x_copy, col, 1)
                names_copy = np.delete(names_copy, col)
            
            bounds = [[np.mean(x_copy[:, i]), max(np.std(x_copy[:, i]), np.finfo(float).eps)] for i in range(x_copy.shape[1])]
            dists = ['norm' for x in range(x_copy.shape[1])]

            problem = {
                'num_vars': x_copy.shape[1],
                'names': names_copy,
                'bounds': bounds,
                'dists': dists,
            }
            parameters = SALib.sample.sobol.sample(problem, samples)
            estimates = clf.predict(parameters)
            if jobs > 0:
                results = SALib.analyze.sobol.analyze(problem, estimates, parallel=True, n_processors=jobs)
            else:
                results = SALib.analyze.sobol.analyze(problem, estimates)
            total_sensitivity = results['ST']
            if np.isnan(np.sum(total_sensitivity)):
                raise Exception("The sensitivity analysis produced NaNs!")
            indices.append(np.argmin(total_sensitivity))
            return total_sensitivity
        
        selector = fs.RFE(learner, n_features_to_select=min_features, step=1, importance_getter=get_importances)
        if(np.isnan(np.sum(X_train_scaled))):
            raise Exception("Error - NaN!")
        selector = selector.fit(X_train_scaled, y_train)
        d = {'learner name': [ll.learner_name], 'learner parameters': [ll.learner_params_csvsafe], 'fold index': [split]}
        for i in range(len(names)):
            d[names[i]] = [selector.ranking_[i]]
        return pd.DataFrame(d)
    except Exception as ee:
        return repr(ee)


class ProcessingPipeline:
    def __init__(
            self, learners: list = None, cross_validator: ms._split._BaseKFold = None, features: pd.DataFrame = None,
            target: np.ndarray = None
    ):
        """
        This function creates and initializes the various parameters that are required for the pipeline to function
        using the sensitivity analysis to generate the importance of each feature.
        :param learners: np.ndarray
            The collection of learners that we will process with the pipeline
        :param cross_validator:
            The cross-validation technique to apply that defines the training and testing datasets for each iteration
        :param features:
            The collection of features that predict the target
        :param target:
            The target of each set of predictors in the features
        """

        #   Initialize the elements of the class that will hold the data for the use in sensitivity analysis and the
        #   determination of the most important features
        self._indices = None
        self._x_local = None
        self._y_local = None

        if features is not None:
            self.features = features
        else:
            self._feature_names = None
            self._features = None

        self._cross_validator = cross_validator
        self._scaler = preprocessing.StandardScaler()
        self._learners = learners
        if learners is not None:
            self._validate_learners()

        if target is not None:
            self._target = target
            # self._target_numeric_mapping = self._get_numeric_mapping(self.target.tolist())
        else:
            self._target = None
            self._target_numeric_mapping = None

        self._results = pd.DataFrame()
        self._accuracy_data = pd.DataFrame()

    def load_results(self, path: str):
        """
        This function will take the path that is provided to the function and load the data into the interface for the
        class to be able to process and analyze additional learners. It also provides the ability to examine the data
        that has been calculated previously and conduct analyses to determine optimal feature count, plot the data,
        or other analyses defined in the class.
        :param path: str
            The path to the file that will be loaded into the interface
        """

        self.set_results(pd.read_csv(path))

    def set_results(self, df:pd.DataFrame):
        """
        This function assignes the passed-in dataframe to the results file.
        You are responsible for ensuring it is of the correct format!
        :param df: pandas DataFrame
            The DataFrame assigned as the results
        """

        self._results = df

    def add_learner(self, new_learner):
        """
        This function provides a method to add a learner to the pipeline list of learners outside of a new constructor
        call.
        :param new_learner:
            The learner to be added to the pipeline
        """

        self._learners.append(new_learner)
        self._validate_learners()

    def run_feature_elimination(self, minimum_feature_count: int = 3, groups=None, samples:int=64, n_jobs:int=-1, job_source:'LearnerParallelization' = 0, verbose: bool = False):
        """
        This pipeline processes the machine learners using a recursive feature elimination to determine the best
        combination of features to optimize the features.

        :param minimum_feature_count:
            The number of features to select prior to returning from the function
        :param groups:
            The array-like object that defines the groups of features used in either the StratifiedGroupKFold or
            GroupKFold cross-validation classes
        :param samples:
            An integer that defines how many samples in generate in the sensitivity analysis
        :param n_jobs:
            Define the number of processes the system will use to parallelize the task.
        :param job_source:
            Define whether parallelization will happen ACROSS learners and cv splits, or WITHIN learners (those
            applicable - which have internal parallelization)
        :param verbose:
            A boolean that will add a DataFrame to the output of the model that possesses significant information
            regarding the analysis and the selected features from the recursive feature elimination.

        """

        #   Get the list of learners that have not yet be run
        learners_to_process = self._get_unprocessed_learners(self._results)

        X = self.features
        y = self._get_labels_numbered()

        X_dtype, y_dtype = self.features.dtype, y.dtype
        X_shape, y_shape = self.features.shape, y.shape
        X_bytes, y_bytes = self.features.nbytes, y.nbytes

        if isinstance(job_source, int):
            job_source = LearnerParallelization(job_source)
        elif isinstance(job_source, LearnerParallelization):
            pass
        else:
            job_source = LearnerParallelization.ACROSS

        if not isinstance(samples, int):
            if verbose:
                print('"samples" parameter is not an integer! Setting to 64.')
            samples = 64
        elif samples <= 1:
            if verbose:
                print('"samples" parameter is less than 2! Setting to 64.')
            samples = 64

        if not isinstance(n_jobs, int):
            n_jobs = 1
        else:
            if n_jobs == -1:
                n_jobs = int(mp.cpu_count() / 2)
            elif n_jobs < 1:
                n_jobs = 1
        
        if job_source == LearnerParallelization.ACROSS:
            jobs_sa = 0
        else:
            jobs_sa = n_jobs

        with SharedMemoryManager() as smm:
            X_mem = smm.SharedMemory(size=X_bytes)
            X_arr = create_np_array_from_shared_mem(X_mem, X_dtype, X_shape)
            X_arr[:] = self.features  # load the data into shared memory

            y_mem = smm.SharedMemory(size=y_bytes)
            y_arr = create_np_array_from_shared_mem(y_mem, y_dtype, y_shape)
            y_arr[:] = y  # load the data into shared memory

            params = []
            for learner in learners_to_process:
                for i, (train_index, test_index) in enumerate(self._cross_validator.split(self.features, y, groups=groups)):
                    params.append(
                        (clone(learner), 
                        minimum_feature_count, 
                        self.feature_names.tolist(), 
                        i, 
                        train_index, 
                        (X_mem, X_dtype, X_shape), 
                        (y_mem, y_dtype, y_shape), 
                        samples,
                        jobs_sa))

            del X_arr
            del y_arr
            if job_source == LearnerParallelization.ACROSS:
                n_procs = n_jobs # min(n_jobs, len(params))
                with mp.Pool(processes=n_procs) as pool:
                    print('mapping with {} processes...'.format(pool._processes))
                    results = tqdm.tqdm(pool.imap(run_rfe_sa, params), total=len(params))
                    t = tuple(results)
            else:
                t = []
                for i in tqdm.tqdm(range(len(params))):
                    t.append(run_rfe_sa(params[i]))
        strs = [x for x in t if isinstance(x, str)]
        if len(strs) > 0:
            raise Exception('|'.join(strs))
        else:
            df = pd.concat(t)
            self._results = pd.concat([self._results, df])

    def measure_accuracy(self, groups=None, n_jobs:int=-1, job_source:'LearnerParallelization' = 0, verbose: bool = False):
        """
        Once the class has been created, and the feature elimination processed (either by running the
        "run_feature_elimination" function or loading a DataFrame) we can begin to process the accuracy as a function
        of the number of features. This will take the feature selection matrix, average it for each learner and then
        build a model for each set of features.
        :param groups:
            Parameter that defines grouping that needs to be applied to the cross validation. This is only applied with
            the StratifiedGroupKFold or GroupKFold cross-validation classes
        :param n_jobs:
            Define the number of processes the system will use to parallelize the task.
        :param job_source:
            Define whether parallelization will happen ACROSS learners and cv splits, or WITHIN learners (those applicable - which have internal parallelization)
        :param verbose:
            Flag that defines how detailed the information used in the TQDM progress bar should be displayed.
        """
        
        learners_to_process = self._get_unprocessed_learners(self._accuracy_data)
        y = self._get_labels_numbered()

        X_dtype, y_dtype = self.features.dtype, y.dtype
        X_shape, y_shape = self.features.shape, y.shape
        X_bytes, y_bytes = self.features.nbytes, y.nbytes

        names = self.feature_names.tolist()

        if isinstance(job_source, int):
            job_source = LearnerParallelization(job_source)
        elif isinstance(job_source, LearnerParallelization):
            pass
        else:
            job_source = LearnerParallelization.ACROSS

        if not isinstance(n_jobs, int):
            n_jobs = 1
        else:
            if n_jobs == -1:
                n_jobs = int(mp.cpu_count() / 2)
            elif n_jobs < 1:
                n_jobs = 1

        with SharedMemoryManager() as smm:
            X_mem = smm.SharedMemory(size=X_bytes)
            X_arr = create_np_array_from_shared_mem(X_mem, X_dtype, X_shape)
            X_arr[:] = self.features  # load the data into shared memory

            y_mem = smm.SharedMemory(size=y_bytes)
            y_arr = create_np_array_from_shared_mem(y_mem, y_dtype, y_shape)
            y_arr[:] = y  # load the data into shared memory
            
            params = []
            for learner in learners_to_process:
                l = type(learner).__name__.split('(')[0]
                p = json.dumps(learner.get_params()).replace(',','|')
                ldf = self._results.loc[self._results['learner name'] == l]
                pldf = ldf.loc[ldf['learner parameters'] == p]
                for i, (idx_train, idx_test) in enumerate(self._cross_validator.split(self.features, y, groups=groups)): # groups must be the same between rfe and this...
                    ipldf = pldf.loc[pldf['fold index'] == i]
                    dropped = ipldf.drop(['learner name', 'learner parameters', 'fold index'], axis=1)
                    for j in range(1, dropped.values.max() + 1):
                        above = np.where(dropped.values[0] <= j)
                        features = dropped.columns[above].tolist()
                        idx_feat = np.array([names.index(x) for x in features])
                        params.append((clone(learner), names, features, i, idx_train, idx_test, idx_feat,
                                       (X_mem, X_dtype, X_shape), (y_mem, y_dtype, y_shape)))

            del X_arr
            del y_arr
            if job_source == LearnerParallelization.ACROSS:
                n_procs = n_jobs # min(n_jobs, len(params))
                with mp.Pool(processes=n_procs) as pool:
                    print('mapping with {} processes...'.format(pool._processes))
                    results = tqdm.tqdm(pool.imap(get_learner_accuracy, params), total=len(params))
                    t = tuple(results)
            else:
                t = []
                for i in tqdm.tqdm(range(len(params))):
                    t.append(get_learner_accuracy(params[i]))
        df = pd.concat(t)
        self._accuracy_data = pd.concat([self._accuracy_data, df])
    
    def _get_labels_numbered(self):
        """
        This method converted the class labels to numbers if necessary.

        To share memory across processes, the given data must be in numerical form.
        """
        if isinstance(self.target[0], str):
            classes = list(sorted(set(self.target.tolist())))
            return np.array([classes.index(x) for x in self.target])
        else:
            return self.target

    @property
    def feature_names(self):
        return self._feature_names

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, values):
        if not isinstance(values, pd.DataFrame):
            raise ValueError("The features are expected to be a DataFrame")
        if values.isnull().values.any():
            raise ValueError("There is at least one Not A Number value in the DataFrame representing the features.")

        self._feature_names = values.columns.values
        self._features = values.to_numpy()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        if not isinstance(value, pd.Series):
            raise ValueError("The target is expected to be a Series")

        self._target = value.to_numpy()
        self._target_numeric_mapping = self._get_numeric_mapping(list(self.value))

    @property
    def learners(self):
        return self._learners

    @learners.setter
    def learners(self, values):
        self._learners = values

        self._validate_learners()

    @property
    def target_numerics(self):
        return self._target_numeric_mapping

    @property
    def analysis_results(self):
        return self._results

    @property
    def accuracy_data(self):
        return self._accuracy_data

    def _find_learner(self, label):
        """
        This function takes the label, created from the results DataFrame, and locates the learner within the list of
        learners inside the class.

        :param label: Typeof LearnerLabel
            The details of the learner that needs to be located within the list of learners inside the class.
        :returns:
            The SKLearn Classifier machine learner that corresponds to the information in the label.
        """

        for learner in self.learners:
            if label == LearnerLabel(learner):
                return learner

    def _importance_getter(self, clf):
        """
        This function is the method used to determine the importance of each feature using the Sensitivity Analysis
        library (SALib) to evaluate the ranking of the features. This is made in accordance with the Recursive
        Feature Elimination function's documentation. The method requires that the features be scaled with the
        StandardScaler that will make the features fit onto a Gaussian distribution. This means that the bounds for
        the sensitivity analysis uses the mean and standard deviation for the limits of the determination of the test
        fields.

        :return:
        """
        #   Define the global variables that are passed between the different functions
        from SALib.sample.saltelli import sample
        from SALib.analyze.sobol import analyze
        x_copy = self._x_local.copy()

        #   Copy the names of the features within the DataFrame
        names_copy = self._feature_names.copy()
        for col in self._indices:
            x_copy = np.delete(x_copy, col, 1)
            names_copy = np.delete(names_copy, col)

        #   Define the bounds of the sampling - since the data has been scaled using the StandardScaler, the shape of
        #   the distribution is Gaussian, so we use the average and standard deviation for the bounds.
        bounds, dists = [], []
        for idx in range(x_copy.shape[1]):
            bounds.append([np.mean(x_copy[:, idx]), np.std(x_copy[:, idx])])
            dists.append('norm')

        #   Define the problem according to the Sensitivity Analysis Library
        problem = {
            'num_vars': x_copy.shape[1],
            'names': names_copy,
            'bounds': bounds,
            'dists': dists,
        }

        parameters = sample(problem, 64)
        estimates = clf.predict(parameters)
        mapped = np.array(self._apply_numeric_mapping(estimates, self._target_numeric_mapping))
        results = analyze(problem, mapped)
        total_sensitivity = results['ST']
        self._indices.append(np.argmin(total_sensitivity))

        return total_sensitivity

    @staticmethod
    def _apply_numeric_mapping(data: list, mapping: dict) -> list:
        """Applies a mapping dictionary to a list of strings to get integers."""
        output = []
        if not isinstance(data, (list, pd.Series, np.ndarray)):
            raise TypeError("Data must be in a list format!")
        else:
            for x in data:
                if not isinstance(x, str):
                    raise TypeError("The data contains non-string values!")
                output.append(mapping[x])
        return output

    @staticmethod
    def _get_numeric_mapping(data: list) -> dict:
        """From a list of strings, generates a mapping to a set of integers"""
        output, inc = {}, -1
        if not isinstance(data, (list, pd.Series, np.ndarray)):
            raise TypeError("Data must be in a list format!")
        else:
            for x in data:
                if not isinstance(x, str):
                    raise TypeError("The data contains non-string values!")
                if x not in output.keys():
                    inc += 1
                    output[x] = inc
        return output

    def _get_unprocessed_learners(self, df:pd.DataFrame):
        """
        This finds the list of the learners that do not exist in the internal DataFrame.

        :return:
        """

        if df.shape[0] == 0:
            return self.learners
    
        if 'learner name' not in df.columns or 'learner parameters' not in df.columns:
            raise Exception("The input dataframe does not contain the learner label columns!")

        unprocessed_learners = list()

        processed_learners = df[['learner name', 'learner parameters']].to_numpy()
        processed_labels = [LearnerLabel(name=x[0], params=x[1]) for x in processed_learners]

        for i in range(len(self.learners)):
            label = LearnerLabel(self.learners[i])
            if label not in processed_labels:
                unprocessed_learners.append(self.learners[i])

        return unprocessed_learners

    def _validate_learners(self):
        """
        This function examines the learners and ensures that the learners within the list were Sci-Kit Learn objects

        """
        from sklearn.base import ClassifierMixin

        for learner in self.learners:
            if not isinstance(learner, ClassifierMixin):
                raise TypeError("The learner is not a Sci-Kit Learn object.")


class LearnerLabel:
    """
    This is a helper class that will assist in describing the machine learner that is used in the pipeline class above.
    It holds the name of the class object, and the details of the hyper parameters of the model. Taken together, these
    elements should provide a unique way to identify the learner within the pipeline, make sure whether the learner
    has been tested, and assist in parallelization of the code.
    """

    def __init__(self, learner: sklearn.base.ClassifierMixin = None, name: str = None, params: [str, dict] = None):
        """
        Define the label based on the information passed through the constructor's arguments. We prefer the use of the
        learner object, as all things are defined there, but to facilitate use of the code we also provide a series of
        arguments that can define the learner's name and hyper-parameters from strings and dictionaries.
        :param learner:
            The classification learner
        :param name:
            The name of the class of the learner
        :param params:
            The dictionary or string listing the hyper-parameters of the machine learner
        """

        if learner is not None:
            self._learner_name = type(learner).__name__.split('(')[0]
            self._params = learner.get_params()
            
        else:
            if name is not None and params is not None:
                self._learner_name = name
                if isinstance(params, dict):
                    self._params = params
                elif isinstance(params, str):
                    d = LearnerLabel.json_to_params(params)
                    if d is not None:
                        self._params = d
                    else:
                        raise Exception("The parameter string could not be converted to a dictionary!")
                else:
                    raise ValueError("Parameters must either be a dictionary of hyper parameters for the learner "
                                     "or a JSON string")
            else:
                raise ValueError("You must supply either a learner or the name and parameters")
        if 'n_jobs' in self._params:
            self._params['n_jobs'] = None

    @property
    def learner_name(self):
        return self._learner_name

    @property
    def learner_parameters(self):
        return self._params

    @property
    def learner_params_as_str(self):
        return self.params_to_json()

    @property
    def learner_params_csvsafe(self):
        return self.learner_params_as_str.replace(',','|')

    def __eq__(self, other):
        """
        This function overrides the equals function for the generic object and permits the checking of the "other"
        argument with the current class. This is done by ensuring the learner names and the contents of the dictionary
        or string representation of the parameters are equivalent.
        :param other:
            The object to compare with the current class.
        :return:
            True of the same, false otherwise
        """
        if type(other) is type(self):
            a = self.learner_name == other.learner_name
            b = self._dict_equality(other)

            return a and b
        return False

    def _dict_equality(self, other):
        #   Check the number of keys, and that every key in self is in other
        k1 = list(sorted(self.learner_parameters.keys()))
        k2 = list(sorted(other.learner_parameters.keys()))

        for i in range(len(k1)):
            if k1[i] != k2[i]:
                return False
            elif self.learner_parameters[k1[i]] is not None and other.learner_parameters[k2[i]] is not None:
                if isinstance(other.learner_parameters[k2[i]], tuple) and isinstance(self.learner_parameters[k1[i]], list):
                    self.learner_parameters[k1[i]] = tuple(self.learner_parameters[k1[i]])
                if isinstance(other.learner_parameters[k2[i]], list) and isinstance(self.learner_parameters[k1[i]], tuple):
                    self.learner_parameters[k1[i]] = list(self.learner_parameters[k1[i]])
                if self.learner_parameters[k1[i]] != other.learner_parameters[k2[i]]:
                    return False

        return True

    def params_to_json(self):
        import json

        return json.dumps(self.learner_parameters)

    @staticmethod
    def json_to_params(value:str):
        import json

        try:
            v = json.loads(value)
            return v
        except json.JSONDecodeError as err:
            try:
                v = json.loads(value.replace('|',','))
                return v
            except json.JSONDecodeError as err:
                try:
                    elements = value.split(',')

                    v = dict()
                    for element in elements:
                        key, value = element.split(':')

                        while '{' in key and len(key) > 0:
                            key = key[1:]

                        while '}' in key and len(key) > 0:
                            key = key[:-1]

                        key = key.strip()[1:-1]

                        value = value.strip()
                        if value.isdecimal():
                            v[key] = float(value)
                        elif value.isdigit():
                            v[key] = int(value)
                        else:
                            if "'" in value:
                                v[key] = value.split("'")[1]
                            elif value == "None":
                                v[key] = None
                            else:
                                v[key] = value

                    return v
                except Exception as ee:
                    return None


class LearnerParallelization(IntEnum):
    ACROSS = 0
    WITHIN = 1

if __name__ == "__main__":
    import os, pathlib
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.neural_network import MLPClassifier
    from sklearn.svm import SVC

    random_state = 42
    learners = [
        # LogisticRegression(random_state=random_state, n_jobs=-1, C=1000, solver='newton-cg', multi_class="multinomial", max_iter=500),
        # KNeighborsClassifier(n_jobs=-1),
        # SVC(random_state=random_state, class_weight="balanced", probability=True, kernel='rbf', C=100.0, gamma=0.001),
        # RandomForestClassifier(random_state=random_state, n_jobs=-1),
        MLPClassifier(random_state=random_state, max_iter=100),
    ]
    cvv = StratifiedKFold(n_splits=2)
    p = pathlib.Path(os.path.abspath(__file__))
    df = pd.read_csv('{}/tests/data/Features_trimmed.csv'.format(p.parent.parent.parent))
    drops = ['time', 'CH_ID', 'SITE_ID', 'THET_DEG', 'THET_DEG_W_CC', 'THET_RAD', 'PROPELLER', 'ANGLE', 'thrust_lbs']
    y = df['PROPELLER'].to_numpy()
    labels = list(sorted(set(y)))
    y_num = [labels.index(x) for x in y]

    dropped = df.drop(drops, axis=1)
    Xx = dropped.to_numpy()

    # Sanity check
    if False:
        ss = StandardScaler()
        cv = StratifiedKFold()
        for i, (idx_train, idx_test) in enumerate(cv.split(X, y)):
            X_train, y_train = X[idx_train], y[idx_train]
            X_test, y_test = X[idx_test], y[idx_test]
            X_train_scaled = ss.fit_transform(X_train, y_train)
            X_test_scaled = ss.transform(X_test)
            ll = LogisticRegression(random_state=42, n_jobs=-1, C=1000, solver='newton-cg', multi_class="multinomial",
                                    max_iter=500)
            for learner in learners:
                learner.fit(X_train_scaled, y_train)
                score = learner.score(X_test_scaled, y_test)
                print('{} {} score: {}'.format(type(learner).__name__.split('(')[0], i, score))

    pp = ProcessingPipeline(learners, cvv, dropped, np.array(y_num))
    pp.run_feature_elimination(job_source=LearnerParallelization.WITHIN)
    res = pp._results.copy()

    unproc_1 = pp._get_unprocessed_learners(pp._results)

    pp2 = ProcessingPipeline(learners, cvv, dropped, np.array(y_num))
    pp2.set_results(res)
    unproc_2 = pp2._get_unprocessed_learners(pp2._results)

    saved = 'C:/Users/bowersga/Documents/temp.csv'
    res.to_csv(saved)
    pp3 = ProcessingPipeline(learners, cvv, dropped, np.array(y_num))
    pp3.load_results(saved)
    unproc_3 = pp3._get_unprocessed_learners(pp3._results)
    # pp.measure_accuracy(job_source=LearnerParallelization.WITHIN)
    print()
