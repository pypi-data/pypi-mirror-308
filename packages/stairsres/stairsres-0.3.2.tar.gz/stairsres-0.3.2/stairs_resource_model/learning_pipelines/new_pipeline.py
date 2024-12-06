from stairs_storage import MschmAdapter
from stairs_resource_model.model.networks import EgoWorkNet, EgoPerformanceNet
import json

class JournalPipeline:
    def __init__(self, work_name, measurement, journal, URL) -> None:
        self.work_name = work_name
        self.journal = journal
        self.measurement = measurement
        self.res_names = list(journal[measurement[0]][work_name].keys())
        self.adapter = MschmAdapter(URL)


    def fit_perfomance(self):
        root = self.res_names
        print(root)
        leaves = self.work_name
        print(leaves)

        bn_05_perf = EgoPerformanceNet(root=root, leaves=[leaves], measurement=self.measurement)



        nodes = root + [leaves]
        info = {"types": {
            node: "cont" for node in nodes
        }, "signs": {
            node: "pos" for node in nodes
        }}

        bn_05_perf.add_nodes(info)
        bn_05_perf.fit(data=None)
        
        work_name = self.work_name.replace('/', '#')
        work_name = work_name.replace('*', '#')
        work_name = work_name.replace('+', '#')
        work_name = work_name.replace('-', '#')
        work_name = work_name.replace('"', '#')
        mes_name = self.measurement[0].replace('.', '')
        bn_05_perf.save(bn_name=f'perfomance_new_learning/{work_name, mes_name}_05')
        file = open(f'perfomance_new_learning/{work_name, mes_name}_05.json')
        model = json.load(file)
        self.adapter.save_perf_model({self.work_name: model}, measurement_type=self.measurement[0])
    def fit_res_model(self):
        root = self.work_name
        print(root)
        leaves = self.res_names
        print(leaves)

        bn_05_res = EgoWorkNet(root=[root], leaves=leaves, measurement=self.measurement)


        nodes = [root] + leaves
        info = {"types": {
            node: "cont" for node in nodes
        }, "signs": {
            node: "pos" for node in nodes
        }}

        bn_05_res.add_nodes(info)
        bn_05_res.fit(data=None)
    
        work_name = self.work_name.replace('/', '#')
        work_name = work_name.replace('*', '#')
        work_name = work_name.replace('+', '#')
        work_name = work_name.replace('-', '#')
        work_name = work_name.replace('"', '#')
        mes_name = self.measurement[0].replace('.', '')
        bn_05_res.save(bn_name=f'res_new_learning/{work_name, mes_name}_05')
        file = open(f'res_new_learning/{work_name, mes_name}_05.json')
        model = json.load(file)
        self.adapter.save_res_model(name=self.work_name, model=model,measurement_type=self.measurement[0])
       


        
