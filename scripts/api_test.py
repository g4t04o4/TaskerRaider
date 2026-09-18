import pytest

from datetime import datetime

from fastapi.testclient import TestClient

from scripts.taskerraider import TaskerRaider



@pytest.fixture(scope="class")
def api():    
    tr = TaskerRaider("sqlite:///test.db")
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