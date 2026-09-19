import pytest

from datetime import datetime

from scripts.dbcontrol import DBControl, NotFoundException

from scripts.models import TaskSchema, TaskSchemaIn, TaskTypeSchema, TaskTypeSchemaIn

from sqlalchemy.exc import IntegrityError

    
@pytest.fixture(scope="function")
def db():
    db = DBControl("sqlite:///:memory:")
    
    type = TaskTypeSchemaIn(
            name="leisure",
            desc="relaxing behaviour, something that makes you chill"
        )
    db.add_type(type)
    type = TaskTypeSchemaIn(
            name="work",
            desc="work-related tasks"
        )
    db.add_type(type)
    type = TaskTypeSchemaIn(
            name="chores",
            desc="tasks that you have to do for survival"
        )
    db.add_type(type)
    
    
    task = TaskSchemaIn(
            name="meet friends at Arby's",
            deadline=datetime.strptime("01.01.2001 00:00:00","%d.%m.%Y %H:%M:%S"),
            desc="",
            tasktype_id=1
        )
    db.add_task(task)
    task = TaskSchemaIn(
            name="vacuum clean the vacuum cleaner",
            deadline=datetime(2002, 2, 2),
            desc="vacuum cleaner needs to be vacuum cleaned, vacuum clean the living sheet out of the vacuum cleaner",
            tasktype_id=3
        )
    db.add_task(task)
    task = TaskSchemaIn(
            name="add oil to oiltaker",
            deadline=datetime(2003, 3, 3),
            desc="oiltaker wants oil, give it to him, it's your job and no one else's",
            tasktype_id=2
        )
    db.add_task(task)
    
    yield db
    db.clear_all_tasks()
    db.clear_all_types()  

class TestTaskType:
    class TestCreateMethods:    
        def test_add_type_autoincrement_succeeds(self, db):
            type = TaskTypeSchemaIn(
                name="learning",
                desc="practicing something to become better"
            )        
            res = db.add_type(type)    
            assert type.model_dump() == res.model_dump(exclude={"id"})       
        
        def test_add_type_succeeds(self, db):
            type = TaskTypeSchema(
                id=4,
                name="learning",
                desc="practicing something to become better"
            )
            res = db.add_type(type)    
            assert type == res
        
        def test_add_type_unique_rows_fails(self, db):        
            type = TaskTypeSchema(
                id=1,
                name="leisure",
                desc="relaxing behaviour, something that makes you chill"
            )   
            with pytest.raises(IntegrityError):
                db.add_type(type)
    
    class TestReadMethods:        
        def test_get_type_succeeds(self, db):
            type = TaskTypeSchema(
                id=1,
                name="leisure",
                desc="relaxing behaviour, something that makes you chill"
            )
            assert db.get_type(id=1) == type
            
        def test_get_nonexistent_type_fails(self, db):
            with pytest.raises(NotFoundException):
                db.get_type(id=42)            

        def test_get_type_list_succeeds(self, db):
            lst = db.get_type_list()
            assert len(lst)
            for t in lst:            
                assert isinstance(t, TaskTypeSchema)
                
        def test_get_type_list_from_empty_fails(self, db):
            db.clear_all_types()
            with pytest.raises(NotFoundException):
                db.get_type_list()        
     
    class TestUpdateMethods:    
        def test_update_type_succeeds(self, db):
            type = TaskTypeSchema(
                id=1,
                name="pleasure",
                desc="relaxing behaviour, something that makes you chill"
            )
            res = db.update_type(type)     
            assert type == res
            
        def test_update_nonexistent_type_fails(self, db):
            type = TaskTypeSchema(
                id=15,
                name="gork",
                desc="mork"
            )        
            with pytest.raises(NotFoundException): 
                db.update_type(type)
            
    class TestDeleteMethods:
        def test_delete_type_succeeds(self, db):
            id = 1
            deleted_row = db.delete_type(id)
            assert deleted_row.id == id
            
        def test_delete_nonexistent_type_fails(self, db):
            with pytest.raises(NotFoundException):
                db.delete_type(id=42)    
                
        def test_clear_all_types_success(self, db):
            db.clear_all_types()
            
        def test_clear_hollow_types_fails(self, db):
            db.clear_all_types()
            with pytest.raises(NotFoundException):
                db.clear_all_types()
            
class TestTask:
    class TestCreateMethods:
        def test_add_task_autoincrement_succeeds(self, db):
            task = TaskSchemaIn(
                    name="watch That New Hot Movie",
                    deadline=datetime(2004, 4, 4),
                    desc="Yes, that's an actual name of the movie",
                    tasktype_id=1
                )       
            res = db.add_task(task)    
            assert task.model_dump() == res.model_dump(exclude={"id"})   
        
        def test_add_task_succeeds(self, db):
            task = TaskSchema(
                    id=4,
                    name="watch That New Hot Movie",
                    deadline=datetime(2004, 4, 4),
                    desc="Yes, that's an actual name of the movie",
                    tasktype_id=1
                )
            assert db.add_task(task) == task
            
        def test_add_existing_task_fails(self, db):
            task = TaskSchema(
                    id=1,
                    name="meet friends at Arby's",
                    deadline=datetime.strptime("01.01.2001 00:00:00","%d.%m.%Y %H:%M:%S"),
                    desc="",
                    tasktype_id=1
                )
            with pytest.raises(IntegrityError):
                db.add_task(task)
            
    class TestReadMethods:
        def test_get_task_succeeds(self, db):
            task = TaskSchema(
                    id=1,
                    name="meet friends at Arby's",
                    #deadline=datetime.strptime("01.01.2001 00:00:00","%d.%m.%Y %H:%M:%S"),
                    deadline=datetime(2001, 1, 1),
                    desc="",
                    tasktype_id=1
                )
            assert db.get_task(id=1) == task
            
        def test_get_nonexistent_task_fails(self, db):
            with pytest.raises(NotFoundException):
                db.get_task(id=42)
                
        def test_get_task_list_succeeds(self, db):
            lst = db.get_task_list()
            assert len(lst)
            for t in lst:            
                assert isinstance(t, TaskSchema)
                
        def test_get_task_list_from_empty_fails(self, db):
            db.clear_all_tasks()
            with pytest.raises(NotFoundException):
                db.get_task_list() 
    
    class TestUpdateMethods:        
        def test_update_task_succeeds(self, db):
            task = TaskSchema(
                    id=1,
                    name="meet friends at Denny's",
                    deadline=datetime.strptime("01.01.2001 00:00:00","%d.%m.%Y %H:%M:%S"),
                    desc="Not Arby's",
                    tasktype_id=1
                )
            assert db.update_task(task) == task
            
        def test_update_nonexistent_task_fails(self, db):
            task = TaskSchema(
                    id=42,
                    name="gork",
                    deadline=datetime.strptime("01.01.2001 00:00:00","%d.%m.%Y %H:%M:%S"),
                    desc="mork",
                    tasktype_id=16
                )
            with pytest.raises(NotFoundException): 
                db.update_task(task)
    
    class TestDeleteMethods:        
        def test_delete_task_succeeds(self, db):
            id = 1
            deleted_row = db.delete_task(id)
            assert deleted_row.id == id
            
        def test_delete_nonexistent_task_fails(self, db):
            with pytest.raises(NotFoundException):
                db.delete_task(id=42)    
                
        def test_clear_all_tasks_success(self, db):
            db.clear_all_tasks()
            
        def test_clear_hollow_tasks_fails(self, db):
            db.clear_all_tasks()
            with pytest.raises(NotFoundException):
                db.clear_all_tasks()
            