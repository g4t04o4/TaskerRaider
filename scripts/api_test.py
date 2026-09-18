import pytest

from datetime import datetime

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scripts.taskerraider import TaskerRaider

from scripts.dbcontrol import DBControl, Base, Task, TaskType
from scripts.models import TaskSchemaIn, TaskSchema, TaskTypeSchemaIn, TaskTypeSchema

# test_engine = create_engine(
#     "sqlite:///:memory:",
#     connect_args={"check_same_thread": False}
# )
# test_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# @pytest.fixture(scope="function")
# def db_session():
#     Base.metadata.create_all(bind=test_engine)
#     session = test_session() 
#     try:
#         yield session
#     finally:
#         session.close()
#         Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def api():    
    # def override_get_db():
    #     try:
    #         yield db_session
    #     finally:
    #         pass
    
    tr = TaskerRaider("sqlite:///:memory:")
    app = tr.app
    
    tr.db_control.create_tables_from_metadata()
    session = tr.db_control.get_session()
    
    Base.metadata.create_all(tr.db_control._engine)
    
    # api.app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client
    # api.app.dependency_overrides.clear()

# from sqlalchemy.orm import sessionmaker
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
# app.dependency_overrides[get_db] = override_get_db
# client = TestClient(app)

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
        
    def test_add_type_success(self, api):
        res = api.post("/type", json={
            "id": 1,
            "name": "learning",
            "desc": "practicing something to become better"
        })
        assert res.status_code == 201
        
        