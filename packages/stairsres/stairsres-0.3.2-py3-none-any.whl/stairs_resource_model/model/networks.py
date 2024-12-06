import os
from sklearn.linear_model import LinearRegression
import pandas as pd
import pickle
from copy import deepcopy
from bamt_light.networks.base import BaseNetwork
from bamt_light.utils import serialization_utils
from concurrent.futures import ThreadPoolExecutor

from .node import EgoNode
from stairs_resource_model.regressor.journal import WorkJournal, PerformanceJournal


class EgoBaseNet(BaseNetwork):
    def __init__(self, root: list = None, leaves: list = None, measurement: str = None, quantile: str = '0.5'):
        super(EgoBaseNet, self).__init__()

        if root is None:
            self.root = []
        else:
            self.root = root

        if leaves is None:
            self.leaves = []
        else:
            self.leaves = leaves
        self.measurement = measurement
        self.quantile = quantile

    def add_nodes(self, descriptor):
        self.descriptor = descriptor
        vertices = []

        for vertex, _ in self.descriptor['types'].items():
            node = EgoNode(name=vertex)
            vertices.append(node)

        self.nodes = vertices

    def update_nodes(self):
        vertices = []
        for node in self.nodes:
            new_node = EgoNode(name=node.name)
            new_node.cont_parents = node.cont_parents
            new_node.disc_parents = node.disc_parents
            new_node.children = node.children
            vertices.append(new_node)
        self.nodes = vertices

    def fit_parameters(self, data, **kwargs):
        def worker(node):
            return node.fit_parameters(data, **kwargs)

        pool = ThreadPoolExecutor(2)
        for node in self.nodes:
            future = pool.submit(worker, node)
            self.distributions[node.name] = future.result()

    def fit(self, data=None, **kwargs):
        edges_list = [(i, j) for i in self.root for j in self.leaves]
        self.set_structure(edges=edges_list)
        self.update_nodes()

        # if self.regressor is None:
        #     mono_list = [1] * len(self.root)
        #     self.regressor = cb.CatBoostRegressor(monotone_constraints=mono_list,
        #                                           allow_const_label=True)
        if self.regressor is None:
            self.regressor = LinearRegression()

        regressors = {}
        for node in self.leaves:
            regressors[node] = deepcopy(self.regressor)
        self.set_regressor(regressors)

        self.fit_parameters(data=data, **kwargs)

    def __update_path(self, models_dir):
        for node_name in self.leaves:
            model_num = self.distributions[node_name]["regressor_obj"].split('/')[-1]
            new_path = os.path.join(models_dir, self.name + '/' + model_num)
            self.distributions[node_name]["regressor_obj"] = new_path

    def sample(
            self,
            n,
            models_dir=None,
            progress_bar=True,
            evidence=None,
            as_df=True,
            predict=False,
            parall_count=1,
            filter_neg=True
    ):
        if models_dir:
            self.__update_path(models_dir=models_dir)
        res = super().sample(
            n=n,
            models_dir=None,
            progress_bar=progress_bar,
            evidence=evidence,
            as_df=as_df,
            predict=predict,
            parall_count=parall_count,
            filter_neg=True
        )
        if as_df:
            for col in res.columns:
                for i in range(len(res[col])):
                    if res[col][i] < 0:
                        res[col][i] = 0
        else:
            for key in res:
                for i in range(len(res[key])):
                    if res[key][i] < 0:
                        res[key][i] = 0
        return res

    @staticmethod
    def from_bn(bn, measurement):
        for node in bn.nodes_names:
            if not bn[node].children:
                root = node
                break
        leaves = [node for node in bn.nodes_names if node != root]
        # nodes = root + [leaves]
        info = {"types": {
            node: "cont" for node in bn.nodes_names
        }, "signs": {
            node: "pos" for node in bn.nodes_names
        }}

        ego_bn = EgoPerformanceNet(root=[root], leaves=leaves, measurement=measurement)
        ego_bn.add_nodes(info)
        ego_bn.set_structure(edges=bn.edges)
        ego_bn.update_nodes()
        ego_bn.distributions = bn.distributions
        return ego_bn

    def predict(self,
                test,
                models_dir=None,
                parall_count=1,
                progress_bar=True):
        if models_dir:
            self.__update_path(models_dir=models_dir)

        columns = list(set(self.nodes_names) - set(test.columns.to_list()))
        if not columns:
            print("Test data is the same as train.")
            return {}

        for node in self.nodes:
            node.quantile = float(self.quantile)
        output = {}
        for node in self.nodes:
            if node.name in test.columns.to_list():
                output[node.name] = test[node.name]
            else:
                parents = node.cont_parents
                if not parents:
                    pvals = None
                else:
                    pvals = test[parents]
                node_data = self.distributions[node.name]
                output[node.name] = node.predict(node_data, pvals=pvals)

        for key in output:
            for i in range(len(output[key])):
                if output[key][i] < 0:
                    output[key][i] = 0
        output_df = pd.DataFrame.from_dict(output, orient="columns")
        output_df.dropna(inplace=True)

        return output_df

    def get_params_for_db(self):
        new_weights = {str(key): self.weights[key] for key in self.weights}
        distribution_for_db = self.distributions.copy()

        for node_name in distribution_for_db.keys():
            if distribution_for_db[node_name]['regressor_obj'] is not None:
                model = distribution_for_db[node_name]['regressor_obj']
                ex_b = pickle.dumps(model, protocol=4)
                model_ser = ex_b.decode("latin1")

                distribution_for_db[node_name]['regressor_obj'] = model_ser
                distribution_for_db[node_name]['serialization'] = 'pickle'

        params_for_db = {
            "info": self.descriptor,
            "edges": self.edges,
            "parameters": distribution_for_db,
            "weights": new_weights,
        }

        return params_for_db

    def from_dict(self, model_structure: dict, models_dir: str = "/"):
        self.add_nodes(model_structure["info"])
        self.set_structure(edges=model_structure["edges"])
        if not self.use_mixture:
            for node_data in model_structure["parameters"].values():
                if "hybcprob" not in node_data.keys():
                    continue
                else:
                    # Since we don't have information about types of nodes, we
                    # should derive it from parameters.
                    if any(
                            list(node_keys.keys()) == ["covars", "mean", "coef"]
                            for node_keys in node_data["hybcprob"].values()
                    ):
                        print(
                            f"This crucial parameter is not the same as father's parameter: use_mixture."
                        )
                        return

        # check if edges before and after are the same.They can be different in
        # the case when user sets forbidden edges.
        if not self.has_logit:
            if not all(
                    edges_before == [edges_after[0], edges_after[1]]
                    for edges_before, edges_after in zip(model_structure["edges"], self.edges)
            ):
                print(
                    f"This crucial parameter is not the same as father's parameter: has_logit."
                )
                return

        deserializer = serialization_utils.Deserializer(models_dir)

        to_deserialize = {}
        # separate logit and gaussian nodes from distributions to deserialize bn's models
        for node_name in model_structure["parameters"].keys():
            if (
                    "Gaussian" in self[node_name].type
                    or "Logit" in self[node_name].type
                    or "ConditionalLogit" in self[node_name].type
                    or "ConditionalGaussian" in self[node_name].type
            ):
                if model_structure["parameters"][node_name].get("serialization", False):
                    to_deserialize[node_name] = [
                        self[node_name].type,
                        model_structure["parameters"][node_name],
                    ]
                elif "hybcprob" in model_structure["parameters"][node_name].keys():
                    to_deserialize[node_name] = [
                        self[node_name].type,
                        model_structure["parameters"][node_name],
                    ]
                else:
                    continue

        deserialized_parameters = deserializer.apply(to_deserialize)
        distributions = model_structure["parameters"].copy()

        for serialized_node in deserialized_parameters.keys():
            distributions[serialized_node] = deserialized_parameters[serialized_node]

        self.set_parameters(parameters=distributions)

        return True


class EgoWorkNet(EgoBaseNet):
    def __init__(self, root: list = None, leaves: list = None, measurement: str = None, quantile: str = '0.5'):
        super(EgoWorkNet, self).__init__(root=root, leaves=leaves, measurement=measurement, quantile=quantile)
        if root:
            self.name = f'{self.root[0]}_ego_work_net_{self.quantile}'

    def load(self, input_dir: str, models_dir: str = "/"):
        super().load(input_data=input_dir, models_dir=models_dir)
        for node in self.nodes_names:
            if not self[node].cont_parents + self[node].disc_parents:
                self.root = node
                break
        self.leaves = [node for node in self.nodes_names if node != self.root]
        self.name = f'{self.root[0]}_ego_work_net_{self.quantile}'
        self.update_nodes()

    def from_dict(self, input_dict: dict, models_dir: str = "/"):
        super().from_dict(model_structure=input_dict, models_dir=models_dir)
        self.name = f'{self.root[0]}_ego_work_net_{self.quantile}'
        self.update_nodes()

    def fit(self, data=None, hours=11.0, **kwargs):
        if data is None or len(data) <= 5:
            edges_list = [(i, j) for i in self.root for j in self.leaves]
            self.set_structure(edges=edges_list)
            self.update_nodes()

            regressors = {}
            for leaf in self.leaves:
                regressor = WorkJournal(root=self.root, leaf=[leaf], measurement=self.measurement)
                regressors[leaf] = deepcopy(regressor)
            self.set_regressor(regressors)
            self.fit_parameters(data=data, hours=hours)
        else:
            super().fit(data=data, **kwargs)


class EgoPerformanceNet(EgoBaseNet):
    def __init__(self, root: list = None, leaves: list = None, measurement: str = None, quantile: str = '0.5'):
        super(EgoPerformanceNet, self).__init__(root=root, leaves=leaves, measurement=measurement, quantile=quantile)

    def load(self, input_dir: str, models_dir: str = "/"):
        super().load(input_data=input_dir, models_dir=models_dir)

        for node in self.nodes_names:
            if not self[node].children:
                self.root = node
                break

        self.leaves = [node for node in self.nodes_names if node != self.root]
        self.name = f'{self.root[0]}_ego_work_net_{self.quantile}'
        self.update_nodes()

    def from_dict(self, input_dict: dict, models_dir: str = "/"):
        super().from_dict(model_structure=input_dict, models_dir=models_dir)
        self.update_nodes()

    def fit(self, data=None, hours=11.0, **kwargs):
        if data is not None:
            super().fit(data=data, **kwargs)
        else:
            # todo: Check edges_list, weird directions
            edges_list = [(i, j) for i in self.root for j in self.leaves]
            self.set_structure(edges=edges_list)
            self.update_nodes()

            regressors = {}
            regressor = PerformanceJournal(root=self.root, leaf=self.leaves, measurement=self.measurement)
            regressors[self.leaves[0]] = regressor
            self.set_regressor(regressors)

            self.fit_parameters(data=data, hours=hours)
