from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

from db.database.database import BaseRepository 

Base = declarative_base()

class SQLLiterepository(BaseRepository):

    def __init__(self, database_url):
        global Base
        self.database_url = database_url
        self.engine = create_engine(self.database_url, connect_args={"check_same_thread": False})
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.connection = self.sessionLocal
        self.base = Base

    def connect(self):
        return self.connection() 


    def close(self):
        self.connection().close()


    def insert(self, model):
        db = self.connect()
        try:
            inserted_object = db.add(model)
            db.commit()
            db.refresh(model)
            return inserted_object
        finally:
            self.close()


    def insert_many(self, models):
        db = self.connect()
        try:
            inserted_objects = db.add_all(models)
            db.commit()
            if len(models) > 0:
                db.refresh(models[0])
            return inserted_objects
        finally:
            self.close()

    def find_by_id(self, model, id):
        db = self.connect()
        try:
            return db.query(model).filter(model.id == id).first()
        finally:
            self.close()
        
    def find_by_parent_id(self, model, parent_id, parent_attribute):
        db = self.connect()
        try:
            return db.query(model).filter(getattr(model, parent_attribute) == parent_id).all()
        finally:
            self.close()