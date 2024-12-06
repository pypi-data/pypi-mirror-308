import random
import math
import scipy
import numpy as np
from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_squared_error as mse
from bamt_light.nodes.gaussian_node import GaussianNode


class EgoNode(GaussianNode):
    def __init__(self, name, regressor=None):
        if regressor is None:
            regressor = LinearRegression()
        super(EgoNode, self).__init__(name, regressor)
        self.type = 'Gaussian EgoNode' + f" ({type(self.regressor).__name__})"

    def fit_parameters(self, data, **kwargs):
        parents = self.cont_parents
        if parents:
            if data is not None and len(data) > 5:
                self.regressor.fit(data[parents].values, data[self.name].values, **kwargs)
                predicted_value = self.regressor.predict(data[parents].values)
                variance = mse(data[self.name].values, predicted_value, squared=False)
            else:
                self.regressor.fit(**kwargs)
                variance = 0
            return {
                "mean": np.nan,
                "regressor_obj": self.regressor,
                "regressor": type(self.regressor).__name__,
                "variance": variance,
                "serialization": None,
            }
        else:
            if data is not None:
                mean_base = np.mean(data[self.name].values)
                variance = np.var(data[self.name].values)
            else:
                mean_base = 0
                variance = 0
            return {
                "mean": mean_base,
                "regressor_obj": None,
                "regressor": None,
                "variance": variance,
                "serialization": None,
            }

    def get_dist(self, node_info, pvals):
        var = node_info["variance"]
        if pvals:
            for el in pvals:
                if str(el) == "nan":
                    return np.nan
            model = node_info["regressor_obj"]

            if type(self).__name__ == "CompositeContinuousNode":
                pvals = [int(item) if isinstance(item, str) else item for item in pvals]
            cond_mean = model.predict(np.array(pvals).reshape(1, -1))
            return cond_mean, var
        else:
            return node_info["mean"], math.sqrt(var)

    def choose(self, node_info, pvals):
        """
        Return value from Logit node
        params:
        node_info: nodes info from distributions
        pvals: parent values
        """

        cond_mean, var = self.get_dist(node_info, pvals)
        return random.gauss(cond_mean, var)

    def predict(self, node_info, pvals):
        """
        Return prediction from Logit node
        params:
        node_info: nodes info from distributions
        pvals: parent values
        """

        if pvals is not None:
            for el in pvals:
                if str(el) == "nan":
                    return np.nan
            model = node_info["regressor_obj"]
            mean = model.predict(pvals)
            variance = node_info["variance"]
            if variance:
                return scipy.stats.norm.ppf(self.quantile, loc=mean, scale=math.sqrt(variance))
            else:
                return mean
        else:
            return [node_info["mean"]] * len(pvals)
