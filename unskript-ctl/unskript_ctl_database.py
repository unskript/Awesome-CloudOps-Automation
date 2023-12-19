#!/usr/bin/env python
#
# Copyright (c) 2023 unSkript.com
# All rights reserved.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE
#
#
import os 
import ZODB
import ZODB.FileStorage

from unskript_factory import DatabaseFactory
from functools import cached_property
from ZODB import DB


class ZoDBInterface(DatabaseFactory):
    def __init__(self):
        super().__init__()
        self.db_name = 'unskript_pss.db'
        self.db_dir = '/unskript/db'
        self.collection_name = 'audit_trail'
        self.db = None

    def create(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('db_name'):
                self.db_name = value
            if key in ('db_dir'):
                self.db_dir = value
            if key in ('collection_name'):
                self.collection_name = value 
        self.logger.debug(f'Checking if DB {self.db_name} exists')
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir, exist_ok=True)

        if not os.path.exists(os.path.join(self.db_dir, self.db_name)):
            pss = ZODB.FileStorage.FileStorage(os.path.join(self.db_dir, self.db_name), pack_keep_old=False)
            db = DB(pss)
            self.logger.debug(f'Creating DB {self.db_name}')
            with db.transaction() as connection:
                root = connection.root()
                root[self.collection_name] = {} 
                connection.transaction_manager.commit()
                connection.close() 
                del root 
                del connection 
        else:
            self.logger.debug(f'DB {self.db_name} Exists!')
            db = DB(os.path.join(self.db_dir, self.db_name))
        self.db = db 
        
        return self.db 

    def read(self, **kwargs):
        data = None
        if not self.db:
            self.logger.error(f"DB {self.db_name} Not initialized or does not exist")
            return  
        for key,value in kwargs.items():
            if key in ('collection_name'):
                self.collection_name = value 

        with self.db.transaction() as connection:
            root = connection.root()
            data = root.get(self.collection_name)
            if data is None:
                # if data does not exist, lets create it
                root[self.collection_name] = {}
            connection.transaction_manager.commit()
            connection.close()
            del root
            del connection 
        
        return data 

    def update(self, **kwargs):
        data = None
        if not self.db:
            self.logger.error(f"DB {self.db_name} Not initialized or does not exist")
            return 
        if 'collection_name' in kwargs:
            self.collection_name = kwargs['collection_name']
        if 'data' in kwargs:
            data = kwargs['data']
        
        with self.db.transaction() as connection:
            root = connection.root()
            root[self.collection_name].update(data)
            connection.transaction_manager.commit()
            connection.close()
            del root
            del connection

        pass 


    def delete(self, **kwargs):
        for key, value in kwargs.items():
            if key in ('db_name'):
                self.db_name = value
            if key in ('db_dir'):
                self.db_dir = value
        if os.path.exists(os.path.join(self.db_dir, self.db_name)) is True:
            try:
                os.remove(os.path.join(self.db_dir, self.db_name))
                self.logger.debug(f'Deleted DB {self.db_name}')
            except Exception as e:
                self.logger.error(f'Deletion of DB {self.db_name} had error. {e}')
                pass 
    




class SQLInterface(DatabaseFactory):
    def __init__(self):
        super().__init__()
        pass 

    def create_db(self, **kwargs):
        pass
    
    def delete_db(self, **kwargs):
        pass
    
    def create(self, **kwargs):
        pass 

    def read(self, **kwargs):
        pass 

    def update(self, **kwargs):
        pass 

    def delete(self, **kwargs):
        pass
