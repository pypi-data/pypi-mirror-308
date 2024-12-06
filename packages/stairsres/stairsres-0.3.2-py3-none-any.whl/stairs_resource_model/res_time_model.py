import math
from stairs_resource_model.model.networks import EgoWorkNet, EgoPerformanceNet

from typing import Literal
from stairs_resource_model.schema import ResourceDict, WorkerReqs, WorkUnit


class ResTimeModel:
    def __init__(self, dbwrapper):
        self.wrapper = dbwrapper

    def get_resources_volumes(self,
                              work_name: str,
                              work_volume: float,
                              measurement: str,
                              shift: float = 11.) -> WorkerReqs:
        """
        Method to calculate new volumes for resources given a volume of work
        :param work_name: name for a work
        :param work_volume: volume for a work
        :param measurement: measurement for a work
        :param shift: amount of time staff works per day
        :return: dict with staff min_count and max_count.
        Max_count means a max possible value for resources, vice versa for min.
        """
        bn_params = self.wrapper.get_res_model(name=work_name, measurement_type=measurement)
        bn = EgoWorkNet()
        if not bn_params:
            print("Database returns None object.")
            return None
        bn.load(bn_params)
        res = bn.leaves
        worker_reqs = {'worker_reqs': []}
        for r in res:
            params, _ = bn.get_dist(r, {bn.root: work_volume})
            if len(params) > 1:
                _, numbers, hours = params[0], params[1], params[2]
                worker_reqs['worker_reqs'].append({'kind': r,
                                                   'volume': 3 * math.ceil(numbers / hours),
                                                   'min_count': math.ceil(numbers / hours),
                                                   'max_count': 5 * math.ceil(numbers / hours)})
            else:
                volume = bn.distributions[r]["regressor_obj"].coef_[0]
                worker_reqs['worker_reqs'].append({'kind': r,
                                                   'volume': 3 * math.ceil(volume / shift),
                                                   'min_count': math.ceil(volume / shift),
                                                   'max_count': 5 * math.ceil(volume / shift)})
        return worker_reqs

    def get_time(self, work_volume: dict, resources: dict, quantile: str, measurement: str) -> int:
        q = 0.5
        if quantile == '0.9':
            q = 0.1
        if quantile == '0.1':
            q = 0.9
        work_name = next(iter(work_volume))
        bn_params = self.wrapper.get_perf_model(name=work_name, measurement_type=measurement)
        model_work_name, model_res_names = next((k[1], [r[0] for r in bn_params['edges']]) for k in bn_params['edges'])
        bn = EgoPerformanceNet()
        bn.load(bn_params)
        test_data = {res_bn_name: resources[res_name] for res_bn_name in model_res_names for res_name in resources if
                     res_name in res_bn_name}
        mu, var = bn.get_dist(model_work_name, test_data)
        return math.ceil(work_volume[work_name] / mu[0])  # max(math.ceil(work_volume[work_name] / mu), 1)

    def estimate_time(self,
                      work_unit: WorkUnit,
                      worker_list: list[ResourceDict],
                      mode: Literal["0.5", "0.1", "0.9"] = '0.5') -> int:
        """
        Method to get time for given resources and work volume

        :param work_unit: work_name and its volume and its measurement
        :param worker_list: resources for work
        :param mode: quantile for calculation
        :return: number of shifts required to make work
        """
        if not worker_list:
            return 0
        if work_unit['volume'] == 0:
            return 0
        work_name = work_unit['name']
        work_volume = work_unit['volume']
        work_measurement = work_unit['measurement']
        res_dict = {req['name']: req['_count'] for req in worker_list}
        return self.get_time(work_volume={work_name: work_volume}, resources=res_dict, measurement=work_measurement,
                             quantile=mode)
