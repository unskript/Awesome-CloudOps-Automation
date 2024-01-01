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
import re
import ZODB
import sqlite3
import json
import ZODB.FileStorage

from unskript_factory import DatabaseFactory, UnskriptFactory
from ZODB import DB


class ZoDBInterface(DatabaseFactory):
    def __init__(self, **kwargs):
        super().__init__()
        self.db_name = 'unskript_pss.db'
        self.db_dir = '/unskript/db'
        self.collection_name = 'audit_trail'
        for key, value in kwargs.items():
            if key in ('db_name'):
                self.db_name = value
            if key in ('db_dir'):
                self.db_dir = value
            if key in ('collection_name'):
                self.collection_name = value 
        
        self.db = self.create()

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
            return False
        if 'collection_name' in kwargs:
            self.collection_name = kwargs['collection_name']
        if 'data' in kwargs:
            data = kwargs['data']
        
        with self.db.transaction() as connection:
            root = connection.root()
            old_data = root[self.collection_name]
            old_data.update(data)
            root[self.collection_name] = old_data
            connection.transaction_manager.commit()
            connection.close()
            del root
            del connection

        return True 


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
                return False
        return True 

class SQLInterface(DatabaseFactory):
    def __init__(self, **kwargs):
        self.db_name = 'unskript_pss.db'
        self.db_dir = '/unskript/db'
        self.table_name = 'AUDIT_TRAIL'
        self.db = None
        for key, value in kwargs.items():
            if key in ('db_name'):
                self.db_name = value
            if key in ('db_dir'):
                self.db_dir = value
            if key in ('table_name'):
                self.table_name = value 

        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir, exist_ok=True)
        self.conn = sqlite3.connect(os.path.join(self.db_dir, self.db_name))
        self.cursor = self.conn.cursor()
        self.schema = self._read_schema(os.path.join(os.path.dirname(__file__), 'unskript_db_schema.json'))
        self.create_table()

    def _read_schema(self, schema_file):
        with open(schema_file, 'r') as file:
            return json.load(file)

    def create_table(self):
        # Create a table based on the schema read from the file
        columns = ', '.join(f"{col} {self.schema['properties'][col]['type']}" for col in self.schema['properties'])
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                {columns}
            )
        ''')
        self.conn.commit()

    def create(self, execution_data):
        # Create a new execution record
        columns = ', '.join(self.schema['properties'].keys())
        placeholders = ', '.join(['?'] * len(self.schema['properties']))
        values = [execution_data[key] for key in self.schema['properties']]
        self.cursor.execute(f'''
            INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})
        ''', values)
        self.conn.commit()

    def read(self, filters=None):
        # Read data with optional filters
        if filters is None:
            # If no filters provided, fetch all data
            self.cursor.execute(f'''
                SELECT * FROM {self.table_name}
            ''')
        else:
            # Construct the WHERE clause based on the filters
            filter_conditions = ' AND '.join(f"{key} = ?" for key in filters)
            filter_values = tuple(filters.values())
            self.cursor.execute(f'''
                SELECT * FROM {self.table_name} WHERE {filter_conditions}
            ''', filter_values)

        data = self.cursor.fetchall()
        if data:
            result = []
            for row in data:
                result.append(dict(zip(self.schema['properties'], row)))
            return result
        return None

    def update(self, new_data=None, filters=None):
        # Update rows based on optional filters and new data
        if new_data is None or filters is None:
            # If no new_data or filters provided, do not perform update
            return False

        # Construct SET clause for new data
        set_values = ', '.join(f"{key} = ?" for key in new_data)
        set_params = tuple(new_data.values())

        # Construct the WHERE clause based on the filters
        filter_conditions = ' AND '.join(f"{key} = ?" for key in filters)
        filter_values = tuple(filters.values())

        self.cursor.execute(f'''
            UPDATE {self.table_name} SET {set_values} WHERE {filter_conditions}
        ''', (*set_params, *filter_values))

        self.conn.commit()
        return True

    def delete(self, filters=None):
        # Delete rows based on optional filters
        if filters is None:
            # If no filters provided, do not perform deletion
            return False

        # Construct the WHERE clause based on the filters
        filter_conditions = ' AND '.join(f"{key} = ?" for key in filters)
        filter_values = tuple(filters.values())

        self.cursor.execute(f'''
            DELETE FROM {self.table_name} WHERE {filter_conditions}
        ''', filter_values)

        self.conn.commit()
        return True 

    def close_connection(self):
        # Close the database connection
        self.conn.close()

# SnippetsDB Interface
class CodeSnippets(ZoDBInterface):
    def __init__(self, **kwargs):
        self.db_dir = '/var/unskript'
        self.db_name = 'snippets.db'
        self.collection_name = 'unskript_cs'
        
        if 'db_dir' in kwargs:
            self.db_dir = kwargs.get('db_dir')
        if 'db_name' in kwargs:
            self.db_name = kwargs.get('db_name')
        if 'collection_name' in kwargs:
            self.collection_name = kwargs.get('collection_name')
        
        super().__init__(db_dir=self.db_dir,
                         db_name=self.db_name,
                         collection_name=self.collection_name)
        
        self.snippets = self.read() or []
    
    def get_checks_by_uuid(self, check_uuid_list: list):
        return [snippet for snippet in self.snippets
                if snippet.get('metadata') and
                snippet.get('metadata').get('uuid') in check_uuid_list]


    def get_checks_by_connector(self, connector_names: list, full_snippet: bool = False):
        filtered_snippets = []
        for snippet in self.snippets:
            metadata = snippet.get('metadata')
            if metadata and metadata.get('action_is_check'):
                connector = metadata.get('action_type')
                connector = connector.split('_')[-1].lower()
                if any(name.lower() == 'all' or re.match(name.lower(), connector) for name in connector_names):
                    if not full_snippet:
                        filtered_snippets.append(snippet)
                    else:
                        filtered_snippets.append([
                            connector.capitalize(),
                            snippet.get('name'),
                            metadata.get('action_entry_function')
                        ])
        return filtered_snippets
    
    def get_all_check_names(self):
        return [snippet.get('metadata').get('action_entry_function') for snippet in self.snippets
                if snippet.get('metadata') and snippet.get('metadata').get('action_is_check')]

    def get_check_by_name(self, check_name: str):
        return [snippet for snippet in self.snippets
                if snippet.get('metadata') and
                snippet.get('metadata').get('action_is_check') and
                snippet.get('metadata').get('action_entry_function') == check_name]
    
    def get_action_name_from_id(self, action_uuid: str):
        matches = [snippet for snippet in self.snippets if snippet.get('metadata') and snippet.get('metadata').get('uuid') == action_uuid]
        return matches[0] if matches else None

    def get_connector_name_from_id(self, action_uuid: str):
        matches = [
            snippet.get('metadata').get('action_type').replace('LEGO_TYPE_', '').lower()
            for snippet in self.snippets
            if snippet.get('metadata') and snippet.get('metadata').get('uuid') == action_uuid
        ]
        return matches[0] if matches else None

# PSS Interface
class PSS(ZoDBInterface):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# DBInterface 
class DBInterface(UnskriptFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # PSS Interface 
        self.pss = PSS(db_name='unskript_pss.db',
                       db_dir = '/unskript/db',
                       collection_name = 'audit_trail')
        
        # CodeSnippet Interface
        self.cs = CodeSnippets(db_name = 'snippets.db',
                               db_dir = '/var/unskript',
                               collection_name = 'unskript_cs')
        if not self.pss or not self.cs:
            self.logger.error("Unable to Initialize CS and PSS Database!, Check log file")
            return 
        
        self.logger.info("Initialized DBInterface")