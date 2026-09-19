import pytest

from datetime import datetime

from fastapi.testclient import TestClient

from scripts.taskerraider import TaskerRaider



@pytest.fixture(scope="session")
def api():    
    tr = TaskerRaider("sqlite:///file::memory:?cache=shared&uri=true")
    app = tr.app    
    
    with TestClient(app) as test_client:
        yield test_client

def _assert(func, expected_response_code, *args, **kwargs):
    res = func(*args, **kwargs)
    assert res.status_code == expected_response_code
    return res

class TestAPI:   
    # Fixture setup 
    @pytest.fixture(autouse=True)
    def _setup_fixture(self, api):
        self.api: TestClient = api
        
        
    # assert methods
    def post(self, expected_response_code: int, *args, **kwargs):
        return _assert(self.api.post, expected_response_code, *args, **kwargs)
        
    def get(self, expected_response_code: int, *args, **kwargs):
        return _assert(self.api.get, expected_response_code, *args, **kwargs)
        
    def put(self, expected_response_code: int, *args, **kwargs):
        return _assert(self.api.put, expected_response_code, *args, **kwargs)
            
    def delete(self, expected_response_code: int, *args, **kwargs):
        return _assert(self.api.delete, expected_response_code, *args, **kwargs)        
        
        
    # Tests
    def test_healthcheck(self):
        res = self.get(200, "/healthcheck")
        
    def test_add_type_autoincrement_success(self):
        res = self.post(201, "/type", json={
            "name": "learning",
            "desc": "practicing something to become better"
        })
        assert res.json() == {
            "id": 1,
            "name": "learning",
            "desc": "practicing something to become better"
        }
        
    def test_add_type_success(self):
        res = self.post(201, "/type", json={
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
        assert res.json() == {
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        }
        
    def test_add_type_without_desc_success(self):
        res = self.post(201, "/type", json={
            "id": 3,
            "name": "work"
        })
        assert res.json() == {
            "id": 3,
            "name": "work",
            "desc": ""
        }
        
    def test_add_type_unique_rows_error(self):
        res = self.post(409, "/type", json={
            "id": 2,
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
    
    def test_add_type_validation_error(self):
        res = self.post(422, "/type", json={
            "id": "seven",
            "name": "chores",
            "desc": "doing stuff to live another day"
        })
        
    def test_add_none_type_error(self):
        res = self.post(422, "/type", json={
            "id": None,
            "name": None,
            "desc": None
        })
        
    def test_add_type_id_only_error(self):
        res = self.post(422, "/type", json={
            "id": 15,
            "name": None,
            "desc": None
        })
        
    def test_add_task_instead_of_type_error(self):
        res = self.post(422, "/type", json={
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": str(datetime(2001, 1, 1)),
            "tasktype_id": 3
        })
        
    def test_add_empty_type_error(self):
        res = self.post(422, "/type", json={})
          
        
       
    def test_add_task_autoincrement_success(self):
        res = self.post(201, "/task", json={
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": str(datetime(2002, 2, 2)),
            "tasktype_id": 3
        })
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_add_task_success(self):
        res = self.post(201, "/task", json={
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": str(datetime(2001, 1, 1)),
            "tasktype_id": 3
        })
        assert res.json() == {
            "id": 2,
            "name": "write some code",
            "desc": "python code specifically",
            "deadline": "2001-01-01T00:00:00",
            "tasktype_id": 3
        }
        
    def test_add_task_without_desc_success(self):
        res = self.post(201, "/task", json={
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 2
        }
        
    def test_add_task_unique_rows_error(self):
        res = self.post(409, "/task", json={
            "id": 3,
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
    
    def test_add_task_validation_error(self):
        res = self.post(422, "/task", json={
            "id": "three and a half",
            "name": "eat some food",
            "deadline": str(datetime(2003, 3, 3)),
            "tasktype_id": 2
        })
        
    def test_add_none_task_error(self):
        res = self.post(422, "/task", json={
            "id": None,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        
    def test_add_task_id_only_error(self):
        res = self.post(422, "/task", json={
            "id": 15,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        
    def test_add_empty_task_error(self):
        res = self.post(422, "/task", json={})
        
    def test_add_type_instead_of_task(self):
        res = self.post(422, "/task", json={
            "id": 5,
            "name": "snores",
            "desc": "stuff i realy don't wanna do"
        })
        
        
        
    def test_get_type_success(self):
        res = self.get(200, "/type/1")
        assert res.json() == {
            "id": 1,
            "name": "learning",
            "desc": "practicing something to become better"
        }
        
    def test_get_nonexistent_type_error(self):
        res = self.get(404, "/type/42")
        
    def test_get_type_validation_error(self):
        res = self.get(422, "/type/first")
        
    def test_get_type_by_negative_id_error(self):
        res = self.get(422, "/type/-5")
        
    def test_get_type_list_success(self):
        res = self.get(200, "/types")
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
        
    def test_get_task_success(self):
        res = self.get(200, "/task/1")
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_get_nonexistent_task_error(self):
        res = self.get(404, "/task/42")
        
    def test_get_task_validation_error(self):
        res = self.get(422, "/task/first")
            
    def test_get_task_by_negative_id_error(self):
        res = self.get(422, "/task/-5")
        
    def test_get_task_list_success(self):
        res = self.get(200, "/tasks")
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
        
        
    
    def test_update_type_success(self):
        res = self.put(200, "/type", json={
            "id": 1,
            "name": "pleasure",
            "desc": "relaxing behaviour, something that makes you chill"
        })
        assert res.json() == {
            "id": 1,
            "name": "pleasure",
            "desc": "relaxing behaviour, something that makes you chill"
        }
        
    def test_update_type_another_success(self):
        res = self.put(200, "/type", json={
            "id": 2,
            "name": "home chores",
            "desc": "stuff that needs to be done at home"
        })
        assert res.json() == {
            "id": 2,
            "name": "home chores",
            "desc": "stuff that needs to be done at home"
        }
    
    def test_update_type_without_desc_success(self):
        res = self.put(200, "/type", json={
            "id": 1,
            "name": "pleasure"
        })
        assert res.json() == {
            "id": 1,
            "name": "pleasure",
            "desc": ""
        }
        
    def test_update_nonexistent_type_error(self):
        res = self.put(404, "/type", json={
            "id": 15,
            "name": "gork",
            "desc": "mork"
        })
        
    def test_update_none_type_error(self):
        res = self.put(422, "/type", json={
            "id": None,
            "name": None,
            "desc": None
        })
        
    def test_update_empty_type_error(self):
        res = self.put(422, "/type", json={})
        
    def test_update_type_id_only_error(self):
        res = self.put(422, "/type", json={"id": 1})
        
    def test_update_type_validation_error(self):
        res = self.put(422, "/type", json={
            "id": "three",
            "name": "three",
            "desc": "three"
        })
         
    def test_update_task_success(self):
        res = self.put(200, "/task", json={
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_update_task_change_deadline_success(self):
        res = self.put(200, "/task", json={
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2004-04-04T00:00:00",
            "tasktype_id": 2
        })
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2004-04-04T00:00:00",
            "tasktype_id": 2
        }
        
    def test_update_task_change_tasktype_success(self):
        res = self.put(200, "/task", json={
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 1
        })
        assert res.json() == {
            "id": 3,
            "name": "eat some food",
            "desc": "food needs to be eaten",
            "deadline": "2003-03-03T00:00:00",
            "tasktype_id": 1
        }
    
    def test_update_task_without_desc_success(self):
        res = self.put(200, "/task", json={
            "id": 1,
            "name": "petting a cat",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        assert res.json() == {
            "id": 1,
            "name": "petting a cat",
            "desc": "",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        }
        
    def test_update_nonexistent_task_error(self):
        res = self.put(404, "/task", json={
            "id": 55,
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        
    def test_update_none_task_error(self):
        res = self.put(422, "/task", json={
            "id": None,
            "name": None,
            "desc": None,
            "deadline": None,
            "tasktype_id": None
        })
        
    def test_update_empty_task_error(self):
        res = self.put(422, "/task", json={})
        
    def test_update_task_id_only_error(self):
        res = self.put(422, "/task", json={"id": 1})
        
    def test_update_task_validation_error(self):
        res = self.put(422, "/task", json={
            "id": "one",
            "name": "petting a cat",
            "desc": "need to pet that kitty",
            "deadline": "2002-02-02T00:00:00",
            "tasktype_id": 3
        })
        
    
    
    def test_delete_type_success(self):
        res = self.delete(200, "/type/1")
    
    def test_delete_nonexistent_type_error(self):
        res = self.delete(404, "/type/42")
        
    def test_delete_type_validation_error(self):
        res = self.delete(422, "/type/three")
        
    def test_clear_all_types_success(self):
        res = self.delete(200, "/types")
    
    def test_clear_hollow_types_error(self):
        res = self.delete(404, "/types")
       
    def test_get_type_list_from_empty_error(self):
        res = self.get(404, "/types")
    
    def test_delete_task_success(self):
        res = self.delete(200, "/task/1")
    
    def test_delete_nonexistent_task_error(self):
        res = self.delete(404, "/task/42")
        
    def test_delete_task_validation_error(self):
        res = self.delete(422, "/task/three")
        
    def test_clear_all_task_success(self):
        res = self.delete(200, "/tasks")
    
    def test_clear_hollow_tasks_error(self):
        res = self.delete(404, "/tasks")
        
    def test_get_task_list_from_empty_error(self):
        res = self.get(404, "/tasks")