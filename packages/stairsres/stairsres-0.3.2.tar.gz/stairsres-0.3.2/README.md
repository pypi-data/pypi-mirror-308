# stairs-resource-model
>Модуль сопоставление материально-человеческих ресурсов (МСЧМ).

## Интеграция
### Оценка ресурсной команды
Данная функциональность реализована через класс, наследующий Job `StairsResourceModelGetResourcesJob`. Он импортируется по следующем пути:
```python
from stairs-resource-model.stairs_resource_model.jobs import StairsResourceModelGetResourcesJob
```
В его методе `run` принимаются следующие параметры:
  - `work_name: str` - имя работы
  - `measurement: float` - единица измерения
  - `volume: float` - объем работы

Метод `run` записывает в хранилище результат в формате модели `StairsResourceModelGetResourcesResult`, она импортируется по следующему пути:
```python
from stairs-resource-model.stairs_resource_model.jobs import StairsResourceModelGetResourcesResult
```
Описание полей модели:
  - `result: list[StairsResourceModelGetResourcesItem]` - описание параметра, 
    путь импорта `from stairs-resource-model.stairs_resource_model.jobs import StairsResourceModelGetResourcesItem`
    - `kind: str` - тип ресурса
    - `volume: int` - объем ресурса
    - `min_count: int` - минимальная оценка
    - `max_count: int` - максимальная оценка
  
### Оценка времени
Данная функциональность реализована через класс, наследующий Job `StairsResourceModelEstimateTimeJob`. Он импортируется по следующем пути:
```python
from stairs-resource-model.stairs_resource_model.jobs import StairsResourceModelEstimateTimeJob
```
В его методе `run` принимаются следующие параметры:
- `work_unit: WorkUnit`, путь для импорта: `from stairs-resource-model.stairs_resource_model.schema import WorkUnit`
    - `name: str` - имя работы
    - `volume: float ` - объем работы
    - `measurement: str` - единица измерения
- `workers: list[ResourceDict]`, путь для импорта: `from stairs-resource-model.stairs_resource_model.schema import ResourceDict`
    - `name: str` - имя ресурса
    - `_count: int` - количество ресурса

Метод `run` записывает в хранилище результат в формате модели `StairsResourceModelEstimateTimeResult`, она импортируется по следующему пути:
```python
from stairs-resource-model.stairs_resource_model.jobs import StairsResourceModelEstimateTimeResult
```
Описание полей модели:
- `result: int` - оценка времени
