from typing import Annotated

from scripts.dbcontrol import DBControl, NotFoundException

from fastapi import FastAPI, Path, Request, status
from fastapi.responses import JSONResponse

from scripts.models import TaskSchemaIn, TaskSchema, TaskTypeSchemaIn, TaskTypeSchema

from sqlalchemy.exc import IntegrityError

"""
TODO:
html/css ui
universal server config
docker container for a full app
middleware
async/await
separate error handler for a whole project
session dependency database
organize tests
"""
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
    def __init__(self, db_filepath = "sqlite:///database.db") -> None:
        # База данных для хранения задач
        self.db_filepath = db_filepath
        self.db_control = DBControl(self.db_filepath)
        
        # Основное приложение FastAPI
        self.app = FastAPI(title="Tasker Raider")
        
        self._register_routes()
        
                    
    def _register_routes(self):
        
        @self.app.exception_handler(IntegrityError)
        async def integrity_exception_handler(request: Request, exc: IntegrityError):
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"error": f"{exc.detail}"}
            )
            
        @self.app.exception_handler(NotFoundException)
        async def not_found_exception_handler(request: Request, exc: NotFoundException):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": "Not found"}
            )
        
        @self.app.get("/healthcheck", status_code=status.HTTP_200_OK)
        def healthcheck() -> str:
            return "operational"
        
        
        # CREATE     
        @self.app.post("/type", status_code=status.HTTP_201_CREATED)    
        def add_type(tasktype: TaskTypeSchemaIn | TaskTypeSchema) -> TaskTypeSchema | None:            
            return self.db_control.add_type(tasktype)
            
        @self.app.post("/task", status_code=status.HTTP_201_CREATED)    
        def add_task(task: TaskSchemaIn | TaskSchema) -> TaskSchema | None:
            return self.db_control.add_task(task)
        
        
        # READ   
        @self.app.get("/type/{type_id}", status_code=status.HTTP_200_OK)
        def get_type(type_id: Annotated[int, Path(ge=0)]) -> TaskTypeSchema | None:
            return self.db_control.get_type(type_id)
            
        @self.app.get("/task/{task_id}", status_code=status.HTTP_200_OK)
        def get_task(task_id: Annotated[int, Path(ge=0)]) -> TaskSchema | None:
            return self.db_control.get_task(task_id)
            
        @self.app.get("/types", status_code=status.HTTP_200_OK)
        def get_type_list() -> list[TaskTypeSchema] | None:
            return self.db_control.get_type_list()
                       
        @self.app.get("/tasks", status_code=status.HTTP_200_OK)
        def get_task_list() -> list[TaskSchema] | None:
            return self.db_control.get_task_list()
        
        
        # UPDATE    
        @self.app.put("/type", status_code=status.HTTP_200_OK)
        def update_type(tasktype: TaskTypeSchema) -> TaskTypeSchema | None:
            return self.db_control.update_type(tasktype)
            
        @self.app.put("/task", status_code=status.HTTP_200_OK)
        def update_task(task: TaskSchema) -> TaskSchema | None:
            return self.db_control.update_task(task)
        
        
        # DELETE    
        @self.app.delete("/type/{type_id}", status_code=status.HTTP_200_OK)
        def delete_type(type_id: Annotated[int, Path(ge=0)]) -> TaskTypeSchema | None:
            return self.db_control.delete_type(type_id)
            
        @self.app.delete("/task/{task_id}", status_code=status.HTTP_200_OK)
        def delete_task(task_id: Annotated[int, Path(ge=0)]) -> TaskSchema | None:
            return self.db_control.delete_task(task_id)
            
        @self.app.delete("/types", status_code=status.HTTP_200_OK)
        def clear_all_types() -> int | None:
            return self.db_control.clear_all_types()
         
        @self.app.delete("/tasks", status_code=status.HTTP_200_OK)
        def clear_all_tasks() -> int | None:            
            return self.db_control.clear_all_tasks() 