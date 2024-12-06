from stairs_storage import MschmAdapter
from stairs_resource_model.model.networks import EgoWorkNet
from bamt_light.networks import ContinuousBN
import json



class TTKPipeline:
    def __init__(self, work_name, measurement, bn_serialzed, URL) -> None:
        self.work_name = work_name
        # self.journal = journal
        self.bn_json = bn_serialzed
        self.measurement = measurement.strip()
        # self.res_names = list(journal[work_name][measurement].keys())
        self.adapter = MschmAdapter(URL)

    def from_bn(self):
        bn = ContinuousBN()
        bn.load(self.bn_json)
        bn_05_perf = EgoWorkNet.from_bn(bn, self.measurement)
        bn_05_perf.save(bn_name=f'tmp/{self.work_name}_{self.measurement}_05')
        file = open(f'tmp/{self.work_name}_{self.measurement}_05.json')
        model = json.load(file)
        return model

    def fit_perfomance(self):
        model = self.from_bn()
        self.adapter.save_perf_model({self.work_name: model}, measurement_type=self.measurement)

    def fit_res_model(self):
        model = self.from_bn()
        self.adapter.save_res_model(name=self.work_name, model=model, measurement_type=self.measurement)