from typing import Annotated, Generator

from scripts.dbcontrol import DBControl, NotFoundException, Base

from fastapi import FastAPI, APIRouter, Path, Response, status, HTTPException, Depends

from scripts.models import TaskSchemaIn, TaskSchema, TaskTypeSchemaIn, TaskTypeSchema

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from pydantic import ValidationError

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
# TODO: сделать нормальную асинхронщину
# TODO: убрать ошибки из импортов
# TODO: сделать нормальный return логов ошибок вместо return None (jsoncontent)
# TODO: сделать exception handler для самых основных ошибок https://fastapi.tiangolo.com/tutorial/handling-errors/
# TODO: update методы не работают

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
        
        self.db_control.create_tables_from_metadata()
        
        self.db_session = Annotated[Session, Depends(self.db_control.get_session)]
        
        # Основное приложение FastAPI
        self.app = FastAPI(title="Tasker Raider")
        
        self._register_routes() 
        
    def _register_routes(self): 
        
        
        # @self.app.middleware("http")
        # def mwp():
        #     pass
             
        
        @self.app.get("/healthcheck", status_code=status.HTTP_200_OK)
        def healthcheck() -> str:
            return "operational"
        
        # CREATE     
        @self.app.post("/type", status_code=status.HTTP_201_CREATED)    
        def add_type(tasktype: TaskTypeSchemaIn | TaskTypeSchema) -> TaskTypeSchema | None:
            try:
                res = self.db_control.add_type(tasktype)
                return res
            except ValidationError as e:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            
        @self.app.post("/task", status_code=status.HTTP_201_CREATED)    
        def add_task(task: TaskSchemaIn | TaskSchema, response: Response) -> TaskSchema | None:
            try:
                res = self.db_control.add_task(task)
                return res
            except ValidationError as e:
                response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
            except IntegrityError as e:
                response.status_code = status.HTTP_409_CONFLICT
        
        
        # READ   
        @self.app.get("/type/{type_id}", status_code=status.HTTP_200_OK)
        def get_type(type_id: Annotated[int, Path(ge=0)], response: Response) -> TaskTypeSchema | None:
            try:
                res = self.db_control.get_type(type_id)
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
            
        @self.app.get("/task/{task_id}", status_code=status.HTTP_200_OK)
        def get_task(task_id: Annotated[int, Path(ge=0)], response: Response) -> TaskSchema | None:
            try:
                res = self.db_control.get_task(task_id)
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
            
        @self.app.get("/type_list", status_code=status.HTTP_200_OK)
        def get_type_list(response: Response) -> list[TaskTypeSchema] | None:
            try:
                res = self.db_control.get_type_list()
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
                       
        @self.app.get("/task_list", status_code=status.HTTP_200_OK)
        def get_task_list(response: Response) -> list[TaskSchema] | None:
            try:
                res = self.db_control.get_task_list()
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
        
        
        # UPDATE    
        @self.app.put("/type", status_code=status.HTTP_200_OK)
        def update_type(tasktype: TaskTypeSchema, response: Response) -> TaskTypeSchema | None:
            try:
                res = self.db_control.update_type(tasktype)
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
            except ValidationError as e:
                response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
            except IntegrityError as e:
                response.status_code = status.HTTP_409_CONFLICT
            
        @self.app.put("/task", status_code=status.HTTP_200_OK)
        def update_task(task: TaskSchema, response: Response) -> TaskSchema | None:
            try:
                res = self.db_control.update_task(task)
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
            except ValidationError as e:
                response.status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
            except IntegrityError as e:
                response.status_code = status.HTTP_409_CONFLICT
        
        
        # DELETE    
        @self.app.delete("/type/{type_id}", status_code=status.HTTP_200_OK)
        def delete_type(type_id: Annotated[int, Path(ge=0)], response: Response) -> TaskTypeSchema | None:
            try:
                res = self.db_control.delete_type(type_id)
                return res 
            except NotFoundException as e:
                response.status_code = e.status_code
            
        @self.app.delete("/task/{task_id}", status_code=status.HTTP_200_OK)
        def delete_task(task_id: Annotated[int, Path(ge=0)], response: Response) -> TaskSchema | None:
            try:
                res: TaskSchema = self.db_control.delete_task(task_id)
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
            
        @self.app.delete("/type_list", status_code=status.HTTP_200_OK)
        def clear_all_types(response: Response) -> int | None:
            try:
                res = self.db_control.clear_all_types()
                return res
            except NotFoundException as e:
                response.status_code = e.status_code
         
        @self.app.delete("/task_list", status_code=status.HTTP_200_OK)
        def clear_all_tasks(response: Response) -> int | None:
            try:
                res = self.db_control.clear_all_tasks()
                return res
            except NotFoundException as e:
                response.status_code = e.status_code    