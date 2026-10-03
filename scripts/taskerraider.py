from typing import Annotated, Optional
from datetime import datetime

from scripts.dbcontrol import DBControl, NotFoundException

from fastapi import FastAPI, Path, Request, status, Form, Depends
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError, HTTPException

from starlette.exceptions import HTTPException as StarletteHTTPException

from scripts.models import TaskSchemaIn, TaskSchema, TaskTypeSchemaIn, TaskTypeSchema

from sqlalchemy.exc import IntegrityError


class TaskerRaider:
    def __init__(self, db_filepath = "sqlite:///database.db") -> None:
        if not db_filepath.startswith("sqlite:///"):
            db_filepath = "sqlite:///" + db_filepath
        
        # База данных для хранения задач
        self.db_filepath = db_filepath
        self.db_control = DBControl(self.db_filepath)
        
        # Основное приложение FastAPI
        self.app = FastAPI(title="Tasker Raider")
        
        # Фронт
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        self.templates = Jinja2Templates(directory="templates")
        
        # Руты
        self._register_routes()
        
                    
    def _register_routes(self):
        @self.app.get("/", include_in_schema=False)
        @self.app.get("/home", include_in_schema=False)
        async def redirect_home():
            return RedirectResponse(url=self.app.url_path_for("gettasks"), 
                                    status_code=status.HTTP_307_TEMPORARY_REDIRECT)
        
        # READ    
        @self.app.get("/gettypes", include_in_schema=False)
        async def gettypes(request: Request):
            return self.templates.TemplateResponse(request, 
                                                   "typelist.html", 
                                                   {
                                                       "types": self.db_control.get_type_list()
                                                    })
            
        
        @self.app.get("/gettasks", include_in_schema=False)
        async def gettasks(request: Request):
            return self.templates.TemplateResponse(request, 
                                                   "tasklist.html", 
                                                   {
                                                       "tasks": self.db_control.get_task_list()
                                                    })
        
        
        # CREATE        
        @self.app.get("/addtypeform", include_in_schema=False)
        async def addtypeform(request: Request):
            return self.templates.TemplateResponse(request, "addtypeform.html")
        
        @self.app.get("/addtaskform", include_in_schema=False)
        async def addtaskform(request: Request):
            return self.templates.TemplateResponse(request, "addtaskform.html")
        
        @self.app.post("/typesubmit", include_in_schema=False)
        async def submittype(request: Request,                            
                             form_data: Annotated[TaskTypeSchema | TaskTypeSchemaIn, Form()]):          
            self.db_control.add_type(form_data)
            return RedirectResponse(url=self.app.url_path_for("gettypes"),                                     
                                    status_code=status.HTTP_303_SEE_OTHER)
            
                
        @self.app.post("/tasksubmit", include_in_schema=False)
        async def submittask(request: Request, 
                            form_data: Annotated[TaskSchema | TaskSchemaIn, Form()]):          
            self.db_control.add_task(form_data)
            return RedirectResponse(url=self.app.url_path_for("gettasks"), 
                                    status_code=status.HTTP_303_SEE_OTHER)
        
        
        # UPDATE     
        @self.app.put("/updatetypeform", include_in_schema=False)
        async def updatetypeform(request: Request):
            pass   
             
        @self.app.put("/updatetaskform", include_in_schema=False)
        async def updatetaskform(request: Request):
            pass  
        
             
        # DELETE   
        @self.app.get("/deletetypesconfirm", include_in_schema=False)
        async def deletetypesconfirm(request: Request):
            return self.templates.TemplateResponse(request, "confirmationform.html",
                                                   {
                                                       "action_desc": "delete all types",
                                                       "method": "deletetypes"
                                                   })
        
        @self.app.get("/deletetasksconfirm", include_in_schema=False)
        async def deletetasksconfirm(request: Request):
            return self.templates.TemplateResponse(request, "confirmationform.html",
                                                   {
                                                       "action_desc": "delete all tasks",
                                                       "method": "deletetasks"
                                                   })
                  
        @self.app.post("/deletetypes", include_in_schema=False)
        async def deletetypes(request: Request):
            self.db_control.clear_all_types()
            return RedirectResponse(url=self.app.url_path_for("gettypes"),                                     
                                    status_code=status.HTTP_303_SEE_OTHER)  
                
        @self.app.post("/deletetasks", include_in_schema=False)
        async def deletetasks(request: Request):
            self.db_control.clear_all_tasks()  
            return RedirectResponse(url=self.app.url_path_for("gettasks"),                                     
                                    status_code=status.HTTP_303_SEE_OTHER)     
        
        
        # API level
        @self.app.get("/api/healthcheck", status_code=status.HTTP_200_OK)
        def healthcheck() -> str:
            return "operational"
        
        
        # CREATE     
        @self.app.post("/api/type", status_code=status.HTTP_201_CREATED)    
        def add_type(tasktype: TaskTypeSchemaIn | TaskTypeSchema) -> TaskTypeSchema | None:            
            return self.db_control.add_type(tasktype)
            
        @self.app.post("/api/task", status_code=status.HTTP_201_CREATED)    
        def add_task(task: TaskSchemaIn | TaskSchema) -> TaskSchema | None:
            return self.db_control.add_task(task)
        
        
        # READ   
        @self.app.get("/api/type/{type_id}", status_code=status.HTTP_200_OK)
        def get_type(type_id: Annotated[int, Path(ge=0)]) -> TaskTypeSchema | None:
            return self.db_control.get_type(type_id)
            
        @self.app.get("/api/task/{task_id}", status_code=status.HTTP_200_OK)
        def get_task(task_id: Annotated[int, Path(ge=0)]) -> TaskSchema | None:
            return self.db_control.get_task(task_id)
            
        @self.app.get("/api/types", status_code=status.HTTP_200_OK)
        def get_type_list() -> list[TaskTypeSchema] | None:
            return self.db_control.get_type_list()
                       
        @self.app.get("/api/tasks", status_code=status.HTTP_200_OK)
        def get_task_list() -> list[TaskSchema] | None:
            return self.db_control.get_task_list()
        
        
        # UPDATE    
        @self.app.put("/api/type", status_code=status.HTTP_200_OK)
        def update_type(tasktype: TaskTypeSchema) -> TaskTypeSchema | None:
            return self.db_control.update_type(tasktype)
            
        @self.app.put("/api/task", status_code=status.HTTP_200_OK)
        def update_task(task: TaskSchema) -> TaskSchema | None:
            return self.db_control.update_task(task)
        
        
        # DELETE    
        @self.app.delete("/api/type/{type_id}", status_code=status.HTTP_200_OK)
        def delete_type(type_id: Annotated[int, Path(ge=0)]) -> TaskTypeSchema | None:
            return self.db_control.delete_type(type_id)
            
        @self.app.delete("/api/task/{task_id}", status_code=status.HTTP_200_OK)
        def delete_task(task_id: Annotated[int, Path(ge=0)]) -> TaskSchema | None:
            return self.db_control.delete_task(task_id)
            
        @self.app.delete("/api/types", status_code=status.HTTP_200_OK)
        def clear_all_types() -> int | None:
            return self.db_control.clear_all_types()
         
        @self.app.delete("/api/tasks", status_code=status.HTTP_200_OK)
        def clear_all_tasks() -> int | None:            
            return self.db_control.clear_all_tasks() 
        
        
        # Exception handlers
        @self.app.exception_handler(IntegrityError)
        async def integrity_exception_handler(request: Request, exc: IntegrityError):
            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"detail": "Value already exists."}
                )
            else:
                return self.templates.TemplateResponse(
                    request,
                    "error.html",
                    {
                        "error_code": status.HTTP_409_CONFLICT,
                        "error_details": "Value already exists."
                    },
                    status_code=status.HTTP_409_CONFLICT
                )
            
        @self.app.exception_handler(NotFoundException)
        async def general_http_exception_handler(request: Request, exc: NotFoundException):
            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={"detail": "Found no such items."}
                )
            else:
                return self.templates.TemplateResponse(
                    request,
                    "error.html",
                    {
                        "error_code": status.HTTP_404_NOT_FOUND,
                        "error_details": "Found no such items."
                    },
                    status_code=status.HTTP_404_NOT_FOUND
                )
                
        @self.app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            if request.url.path.startswith("/api"):
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    content={"detail": exc.errors()}
                )
            else:
                return self.templates.TemplateResponse(
                    request,
                    "error.html",
                    {
                        "error_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
                        "error_details": "Invalid request. Check input values."
                    },
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
               )