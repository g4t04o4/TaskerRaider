from typing import Optional
from datetime import datetime

from sqlalchemy import String, Date, ForeignKey
from sqlalchemy import create_engine, select, delete

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship, Session

from scripts.models import TaskSchema, TaskSchemaIn, TaskTypeSchema, TaskTypeSchemaIn
  
class NotFoundException(Exception):
    pass
    
class Base(DeclarativeBase):
    pass

class Task(Base):
    __tablename__ = "task"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    deadline: Mapped[datetime] = mapped_column(Date)
    desc: Mapped[Optional[str]]
    
    tasktype_id: Mapped[int] = mapped_column(ForeignKey('tasktype.id'))
    tasktype: Mapped["TaskType"] = relationship(back_populates="tasks")
    
    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r}, deadline={self.deadline!r}, desc={self.desc!r}, tasktype_id={self.tasktype_id!r})"
    
class TaskType(Base):
    __tablename__ = "tasktype"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[Optional[str]]
    
    tasks: Mapped[list["Task"]] = relationship(back_populates="tasktype", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"TaskType(id={self.id!r}, name={self.name!r}, desc={self.desc!r})"

class DBControl:
    def __init__(self, filepath: str) -> None:
        self._db_filepath = filepath
        self._engine = create_engine(self._db_filepath, echo=False, connect_args={"check_same_thread": False}) 
        
        Base.metadata.create_all(self._engine)
          

    # CREATE                        
    def add_type(self, tasktype: TaskTypeSchemaIn | TaskTypeSchema) -> TaskTypeSchema:
        with Session(self._engine) as session:
            t = TaskType(**tasktype.model_dump())
            session.add(t)
            session.commit()
            return TaskTypeSchema.model_validate(session.get(TaskType, t.id))
    
    def add_task(self, task: TaskSchemaIn | TaskTypeSchema) -> TaskSchema:
        with Session(self._engine) as session:
            t = Task(**task.model_dump())
            session.add(t)
            session.commit()
            return TaskSchema.model_validate(session.get(Task, t.id))
    
    
    # READ             
    def get_type(self, id) -> TaskTypeSchema:
        with Session(self._engine) as session:
            t = session.get(TaskType, id)
            if t is None:
                raise NotFoundException
            val= TaskTypeSchema.model_validate(t)
            return val
    
    def get_task(self, id) -> TaskSchema:
        with Session(self._engine) as session:
            t = session.get(Task, id)
            if t is None:
                raise NotFoundException
            val= TaskSchema.model_validate(t)
            return val
        
    def get_type_list(self) -> list[TaskTypeSchema]:
        with Session(self._engine) as session:
            lst = []            
            for t in session.scalars(select(TaskType)).all():
                lst.append(TaskTypeSchema.model_validate(t))
            if not lst:
                raise NotFoundException
            return lst
        
    def get_task_list(self) -> list[TaskSchema]:
        with Session(self._engine) as session:
            lst = []            
            for t in session.scalars(select(Task)).all():
                lst.append(TaskSchema.model_validate(t))
            if not lst:
                raise NotFoundException
            return lst
    
    
    # UPDATE
    def update_type(self, tasktype: TaskTypeSchema) -> TaskTypeSchema:
        with Session(self._engine) as session:
            t = TaskType(**tasktype.model_dump())
            old_t = session.get(TaskType, t.id)
            if old_t is None:
                raise NotFoundException
            old_t.name = t.name
            old_t.desc = t.desc
            return TaskTypeSchema.model_validate(old_t)
        
    def update_task(self, task: TaskSchema) -> TaskSchema:
        with Session(self._engine) as session:
            t = Task(**task.model_dump())
            old_t = session.get(Task, t.id)
            if old_t is None:
                raise NotFoundException
            old_t.name = t.name
            old_t.deadline = t.deadline
            old_t.desc = t.desc
            old_t.tasktype_id = t.tasktype_id
            return TaskSchema.model_validate(old_t)
    
    
    # DELETE    
    def delete_type(self, id) -> TaskTypeSchema:
        with Session(self._engine) as session:            
            row = session.get(TaskType, id)            
            if row is None:
                raise NotFoundException
            deleted_row = TaskTypeSchema.model_validate(row)         
            session.delete(row)
            session.commit()
            return deleted_row               

    def delete_task(self, id) -> TaskSchema:
        with Session(self._engine) as session:            
            row = session.get(Task, id)            
            if row is None:
                raise NotFoundException
            deleted_row = TaskSchema.model_validate(row)             
            session.delete(row)
            session.commit()
            return deleted_row 
    
    def clear_all_types(self) -> int:
        with Session(self._engine) as session:            
            res = session.execute(delete(TaskType))
            if res.rowcount == 0: # type:ignore
                raise NotFoundException
            session.commit()
            return res.rowcount # type:ignore
   
    def clear_all_tasks(self) -> int:
        with Session(self._engine) as session:
            res = session.execute(delete(Task))
            if res.rowcount == 0: # type:ignore
                raise NotFoundException
            session.commit()
            return res.rowcount # type:ignore
        
    
    
    
    
    
   