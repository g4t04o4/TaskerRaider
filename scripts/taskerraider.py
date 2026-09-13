from typing import List, Type
from enum import Enum

from scripts.dbcontrol import DBControl

from fastapi import FastAPI, APIRouter, HTTPException

from scripts.models import TaskSchema, TaskTypeSchema, BaseModel

"""
TODO:
html/css ui
tests
universal server config
POST variables through post body
validate data
return adequate status codes
health check route
internationalization (different languages)
separate data structures for requests/decode_responses
docker container for a full app
"""
# TODO: сделать выбор дедлайна на календарике и выбор типа задачи из выпадающего списка
# TODO: сделать операцию изменения уже существующей записи
# TODO: сделать более красивый и структурированный возврат bulk методов (json)
# TODO: при удалении уже удалённой строки не кидает ошибку
# TODO: нормальные http статус коды для результатов реквестов
"""
Маленькое FastAPI приложение для менеджмента задач

Функционал:
    добавить задачу
    изменить задачу
        отметить задачу как выполненную
    удалить задачу
    показать все задачи отсортированно по времени/срочности/иному критерию
    
Дополнительно:
    можно хранить тип задачи: работа/бытовое/досуг/саморазвитие и структурировать задачи по этим типам
        причина создать вторую таблицу в бд и сделать связь между ними
    
    
Задача содержит в себе название задачи, её краткое описание и дату/время, к которой она должна быть сделана (+тип задачи)
"""


class TaskerRaider:
    def __init__(self) -> None:
        # База данных для хранения задач
        self.db_filepath = "sqlite:///database.db"
        self.db_control = DBControl(self.db_filepath)
        
        # Основное приложение FastAPI
        self.app = FastAPI(title="Tasker Raider")
        
        self.router = APIRouter()
        
        self._register_routes()
        
    def _register_routes(self):        
             
        @self.app.post("/type")    
        def add_type(tasktype: TaskTypeSchema) -> dict[str, str]:
            res = self.db_control.add_type(tasktype)
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not add type"})
            
        @self.app.get("/type")
        def get_type(id: int) -> dict[str, str]:
            res = self.db_control.get_type(id)
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not get type"})
            
        @self.app.delete("/type")
        def delete_type(id: int) -> dict[str, str]:
            res = self.db_control.delete_type(id)
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not delete type"})
            
        @self.app.post("/types")
        def bulk_add_types(types: List[TaskTypeSchema]) -> dict[str, str]:
            res = self.db_control.bulk_add_types(types)
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not add type"})
            
        @self.app.get("/types")
        def get_type_list() -> dict[str, str]:
            res = self.db_control.get_type_list()
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not get type"})
            
        @self.app.delete("/types")
        def clear_all_types():
            res = self.db_control.clear_all_types()
            if res:
                return({"result": f"{res}"})
            else:
                return({"error": "could not delete type"})