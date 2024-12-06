from stairs_resource_model.res_time_model import ResTimeModel
from stairs_storage import MschmAdapter

def get_resource(work_name:str, work_volume:float, unit:str):
    db_wrapper = MschmAdapter(url="postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test")
    res_time_model = ResTimeModel(dbwrapper=db_wrapper)
    res_data = res_time_model.get_resources_volumes(work_name=work_name, work_volume=work_volume, measurement=unit)
    return res_data

def get_time(work_unit:dict, worker_and_resource_list:list, mode="0.5"):
    db_wrapper = MschmAdapter(url="postgresql+psycopg2://testuser:pwd@10.32.15.30:25432/test")
    res_time_model = ResTimeModel(dbwrapper=db_wrapper)
    time = res_time_model.estimate_time(work_unit=work_unit, worker_list=worker_and_resource_list, mode=mode)
    return time