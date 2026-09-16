from typing import List, Type, Annotated
from enum import Enum

from scripts.dbcontrol import DBControl, NotFoundException

from fastapi import FastAPI, APIRouter, Query, HTTPException, Path

from scripts.models import TaskSchemaIn, TaskSchema, TaskTypeSchemaIn, TaskTypeSchema

"""
TODO:
html/css ui
tests
universal server config
return adequate status codes
health check route
internationalization (different languages)
separate data structures for requests/decode_responses
docker container for a full app
"""
# TODO: сделать более красивый и структурированный возврат bulk методов (json)
# TODO: нормальные http статус коды для результатов реквестов
# TODO: сделать нормальную асинхронщину
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
        
        # TODO: need to catch exceptions instead of return "error"    
        
        # CREATE     
        @self.app.post("/type")    
        def add_type(tasktype: TaskTypeSchemaIn | TaskTypeSchema) -> dict[str, TaskTypeSchema | None]:
            res = self.db_control.add_type(tasktype)
            if res:
                return({"success": res})
            else:
                return({"error": None})
            
        @self.app.post("/task")    
        def add_task(task: TaskSchemaIn | TaskSchema) -> dict[str, TaskSchema | None]:
            res = self.db_control.add_task(task)
            if res:
                return({"success": res})
            else:
                return({"error": None})
        
        
        # READ   
        @self.app.get("/type/{type_id}")
        def get_type(type_id: Annotated[int, Path(ge=0)]) -> dict[str, TaskTypeSchema | None]:
            res = self.db_control.get_type(type_id)
            if res:
                return({"success": res})
            else:
                return({"error": None})
            
        @self.app.get("/task/{task_id}")
        def get_task(task_id: Annotated[int, Path(ge=0)]) -> dict[str, TaskSchema | None]:
            res = self.db_control.get_task(task_id)
            if res:
                return({"success": res})
            else:
                return({"error": None})
            
        @self.app.get("/type_list")
        def get_type_list() -> dict[str, list[TaskTypeSchema] | None]:
            res = self.db_control.get_type_list()
            if res:
                return({"success": res})
            else:
                return({"error": None})
        
        @self.app.get("/task_list")
        def get_task_list() -> dict[str, list[TaskSchema] | None]:
            res = self.db_control.get_task_list()
            if res:
                return({"success": res})
            else:
                return({"error": None})
        
        
        # UPDATE    
        @self.app.put("/type")
        def update_type(tasktype: TaskTypeSchema) -> dict[str, TaskTypeSchema | None]:
            res = self.db_control.update_type(tasktype)
            if res:
                return({"success": res})
            else:
                return({"error": None})
            
        @self.app.put("/task")
        def update_task(task: TaskSchema) -> dict[str, TaskSchema | None]:
            res = self.db_control.update_task(task)
            if res:
                return({"success": res})
            else:
                return({"error": None})
        
        
        # DELETE    
        @self.app.delete("/type/{type_id}")
        def delete_type(type_id: Annotated[int, Path(ge=0)]) -> dict[str, TaskTypeSchema | None]:
            res = self.db_control.delete_type(type_id)
            if res:
                return({"success": res})
            else:
                return({"error": None})  
            
        @self.app.delete("/task/{task_id}")
        def delete_task(task_id: Annotated[int, Path(ge=0)]) -> dict[str, TaskSchema | None]:
            res = self.db_control.delete_task(task_id)
            if res:
                return({"success": res})
            else:
                return({"error": None})
            
        @self.app.delete("/type_list")
        def clear_all_types() -> str:
            try:
                self.db_control.clear_all_types()
                return "success"
            except NotFoundException as e:
                print(f"error: {e}")
                return "error"
         
        @self.app.delete("/task_list")
        def clear_all_tasks() -> str:
            try:
                self.db_control.clear_all_tasks()
                return "success"
            except NotFoundException as e:
                print(f"error: {e}")
                return "error"       