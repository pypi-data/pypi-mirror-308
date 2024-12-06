import json
import numpy as np
from sklearn.linear_model import LinearRegression



class JournalModel:
    def __init__(self, root, leaf, measurement):
        self.root = root
        self.leaf = leaf
        self.measuarement = measurement


    @staticmethod
    def get_journal():
        with open('D:/stairs-resource-model/auxiliary_data/res_mapped_with_new_orientation.json') as f:
            journal = json.load(f)
        return journal

    def fit(self, hours=11.0):
        pass

    def predict(self, data):
        pass


class WorkJournal(JournalModel):
    def __init__(self, root, leaf,  measurement):
        super().__init__(root=root, leaf=leaf, measurement=measurement)
        self.productivity = None
        self.numbers = None
        self.hours = None

    def fit(self, hours=11.0):
        journal = self.get_journal()
        self.productivity = journal[self.measuarement[0]][self.root[0]][self.leaf[0]]['productivity']
        self.numbers = journal[self.measuarement[0]][self.root[0]][self.leaf[0]]['number']
        self.hours = hours


    def predict(self, data):
        return [self.productivity, self.numbers, self.hours]


class PerformanceJournal(JournalModel):
    def __init__(self, root, leaf, measurement):
        super().__init__(root=root, leaf=leaf, measurement=measurement)
        self.hours = None
        self.productivity = None
        self.numbers = None

    def fit(self, hours=11.0):
        journal = self.get_journal()
        numbers = {}
        for r in self.root:
            numbers[r] = journal[self.measuarement[0]][self.leaf[0]][r]['number']
        self.numbers = numbers
        self.productivity = journal[self.measuarement[0]][self.leaf[0]][self.root[0]]["productivity"]
        self.hours = hours

    def predict(self, data):
        min_numbers = []
        for i, node in enumerate(self.root):
            min_number = data[0, i] / self.numbers[node]
            min_numbers.append(min_number)
        coef = self.hours*min(min_numbers)
        performance = [coef * self.productivity]

        return performance
