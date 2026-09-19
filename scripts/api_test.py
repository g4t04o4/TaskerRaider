import pytest

from datetime import datetime

from fastapi.testclient import TestClient

from scripts.taskerraider import TaskerRaider



@pytest.fixture(scope="session")
def api():    
    tr = TaskerRaider("sqlite:///file::memory:?cache=shared&uri=true")
    app = tr.app    
    
    with TestClient(app) as test_client:
        res = test_client.delete("/task_list")
        res = test_client.delete("/type_list")
        yield test_client


class TestAPI:
    def test_healthcheck(self, api):
        res = api.get("/healthcheck")
        assert res.status_code == 200
        
    def test_add_type_autoincrement_success(self, api):
        res = api.post("/type", json={
            "name": "learning",
            "desc": "practicing something to become better"
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 1,
            "name": "learning",
            "desc": "practicing something to become better"
        }
        
    def test_add_type_success(self, api):
        res = api.post("/type", json={
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        }
        
    def test_add_type_without_desc_success(self, api):
        res = api.post("/type", json={
            "id": 3,
            "name": "work"
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 3,
            "name": "work",
            "desc": ""
        }
        
    def test_add_type_unique_rows_error(self, api):
        res = api.post("/type", json={
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
        assert res.status_code == 409
    
    def test_add_type_validation_error(self, api):
        res = api.post("/type", json={
            "id": "seven",
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
        assert res.status_code == 422
        
    def test_add_none_type_error(self, api):
        res = api.post("/type", json={
            "id": None,
            "name": None,
            "desc": None
        })
        assert res.status_code == 422
        
    def test_add_type_id_only_error(self, api):
        res = api.post("/type", json={
            "id": 15,
            "name": None,
            "desc": None
        })
        assert res.status_code == 422
        
    def test_add_task_instead_of_type_error(self, api):
        res = api.post("/type", json={
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": str(datetime(2001, 1, 1)),
            "tasktype_id": 3
        })
        assert res.status_code == 422
        
    def test_add_empty_type_error(self, api):
        res = api.post("/type", json={})
        assert res.status_code == 422
          
        
       
    def test_add_task_autoincrement_success(self, api):
        res = api.post("/task", json={
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": str(datetime(2002, 2, 2)),
            "tasktype_id": 3
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_add_task_success(self, api):
        res = api.post("/task", json={
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": str(datetime(2001, 1, 1)),
            "tasktype_id": 3
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": "2001-01-01T00:00:00",
            "tasktype_id": 3
        }
        
    def test_add_task_without_desc_success(self, api):
        res = api.post("/task", json={
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
        assert res.status_code == 201
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 2
        }
        
    def test_add_task_unique_rows_error(self, api):
        res = api.post("/task", json={
            "id": 3,
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
        assert res.status_code == 409
    
    def test_add_task_validation_error(self, api):
        res = api.post("/task", json={
            "id": "three and a half",
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
        assert res.status_code == 422
        
    def test_add_none_task_error(self, api):
        res = api.post("/task", json={
            "id": None,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        assert res.status_code == 422
        
    def test_add_task_id_only_error(self, api):
        res = api.post("/task", json={
            "id": 15,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        assert res.status_code == 422  
        
    def test_add_empty_task_error(self, api):
        res = api.post("/task", json={})
        assert res.status_code == 422
        
    def test_add_type_instead_of_task(self, api):
        res = api.post("/task", json={
            "id": 5,
            "name": "snores",
            "desc": "stuff i realy don't wanna do"
        })
        assert res.status_code == 422
        
        
        
    def test_get_type_success(self, api):
        res = api.get("/type/1")
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "learning",
            "desc": "practicing something to become better"
        }
        
    def test_get_nonexistent_type_error(self, api):
        res = api.get("/type/42")
        assert res.status_code == 404
        
    def test_get_type_validation_error(self, api):
        res = api.get("/type/first")
        assert res.status_code == 422
        
    def test_get_type_by_negative_id_error(self, api):
        res = api.get("/type/-5")
        assert res.status_code == 422
        
    def test_get_type_list_success(self, api):
        res = api.get("/type_list")
        assert res.status_code == 200
        assert res.json() == [
            {"name":"learning",
             "desc":"practicing something to become better",
             "id":1},
            {"name":"chores",
             "desc":"doing stuff to live another day",
             "id":2},
            {"name":"work",
             "desc":"",
             "id":3}
        ]     
        
    def test_get_task_success(self, api):
        res = api.get("/task/1")
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_get_nonexistent_task_error(self, api):
        res = api.get("/task/42")
        assert res.status_code == 404
        
    def test_get_task_validation_error(self, api):
        res = api.get("/task/first")
        assert res.status_code == 422
            
    def test_get_task_by_negative_id_error(self, api):
        res = api.get("/task/-5")
        assert res.status_code == 422
        
    def test_get_task_list_success(self, api):
        res = api.get("/task_list")
        assert res.status_code == 200
        assert res.json() == [
            {"name":"petting a cat",
             "deadline":"2002-02-02T00:00:00",
             "desc":"need to pet that kitty",
             "tasktype_id":3,
             "id":1},
            {"name":"write some code",
             "deadline":"2001-01-01T00:00:00",
             "desc":"python code specifically",
             "tasktype_id":3,
             "id":2},
            {"name":"eat some food",
             "deadline":"2003-03-03T00:00:00",
             "desc":"",
             "tasktype_id":2,
             "id":3}
            ]
        
        
    
    def test_update_type_success(self, api):
        res = api.put("/type", json={
            "id": 1,
            "name": "pleasure",
            "desc": "relaxing behaviour, something that makes you chill"
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "pleasure",
            "desc": "relaxing behaviour, something that makes you chill"
        }
        
    def test_update_type_another_success(self, api):
        res = api.put("/type", json={
            "id": 2,
            "name": "home chores",
            "desc": "stuff that needs to be done at home"
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 2,
            "name": "home chores",
            "desc": "stuff that needs to be done at home"
        }
    
    def test_update_type_without_desc_success(self, api):
        res = api.put("/type", json={
            "id": 1,
            "name": "pleasure"
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "pleasure",
            "desc": ""
        }
        
    def test_update_nonexistent_type_error(self, api):
        res = api.put("/type", json={
            "id": 15,
            "name": "gork",
            "desc": "mork"
        })
        assert res.status_code == 404
        
    def test_update_none_type_error(self, api):
        res = api.put("/type", json={
            "id": None,
            "name": None,
            "desc": None
        })
        assert res.status_code == 422
        
    def test_update_empty_type_error(self, api):
        res = api.put("/type", json={})
        assert res.status_code == 422
        
    def test_update_type_id_only_error(self, api):
        res = api.put("/type", json={"id": 1})
        assert res.status_code == 422
        
    def test_update_type_validation_error(self, api):
        res = api.put("/type", json={
            "id": "three",
            "name": "three",
            "desc": "three"
        })
        assert res.status_code == 422
         
    def test_update_task_success(self, api):
        res = api.put("/task", json={
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_update_task_change_deadline_success(self, api):
        res = api.put("/task", json={
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2004-04-04T00:00:00",
            "tasktype_id": 2
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2004-04-04T00:00:00",
            "tasktype_id": 2
        }
        
    def test_update_task_change_tasktype_success(self, api):
        res = api.put("/task", json={
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 1
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 1
        }
    
    def test_update_task_without_desc_success(self, api):
        res = api.put("/task", json={
            "id": 1,
            "name": "petting a cat",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.status_code == 200
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_update_nonexistent_task_error(self, api):
        res = api.put("/task", json={
            "id": 55,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.status_code == 404
        
    def test_update_none_task_error(self, api):
        res = api.put("/task", json={
            "id": None,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        assert res.status_code == 422
        
    def test_update_empty_task_error(self, api):
        res = api.put("/task", json={})
        assert res.status_code == 422
        
    def test_update_task_id_only_error(self, api):
        res = api.put("/task", json={"id": 1})
        assert res.status_code == 422
        
    def test_update_task_validation_error(self, api):
        res = api.put("/task", json={
            "id": "one",
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.status_code == 422
        
    
    
    def test_delete_type_success(self, api):
        res = api.delete("/type/1")
        assert res.status_code == 200
    
    def test_delete_nonexistent_type_error(self, api):
        res = api.delete("/type/42")
        assert res.status_code == 404
        
    def test_delete_type_validation_error(self, api):
        res = api.delete("/type/three")
        assert res.status_code == 422
        
    def test_clear_all_types_success(self, api):
        res = api.delete("/type_list")
        assert res.status_code == 200       
    
    def test_clear_hollow_types_error(self, api):
        res = api.delete("/type_list")
        assert res.status_code == 404    
       
    def test_get_type_list_from_empty_error(self, api):
        res = api.get("/type_list")
        assert res.status_code == 404   
    
    def test_delete_task_success(self, api):
        res = api.delete("/task/1")
        assert res.status_code == 200
    
    def test_delete_nonexistent_task_error(self, api):
        res = api.delete("/task/42")
        assert res.status_code == 404
        
    def test_delete_task_validation_error(self, api):
        res = api.delete("/task/three")
        assert res.status_code == 422
        
    def test_clear_all_task_success(self, api):
        res = api.delete("/task_list")
        assert res.status_code == 200       
    
    def test_clear_hollow_tasks_error(self, api):
        res = api.delete("/task_list")
        assert res.status_code == 404    
        
    def test_get_task_list_from_empty_error(self, api):
        res = api.get("/task_list")
        assert res.status_code == 404   