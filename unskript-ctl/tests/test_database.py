import unittest
import os
import json
import shutil
import sqlite3
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from unskript_ctl_database import ZoDBInterface, SQLInterface
except Exception as e: 
    print(f"ERROR: {e}")

class TestZoDBInterface(unittest.TestCase):
    def setUp(self):
        self.zodb = ZoDBInterface(db_dir='./unskript/db')
    
    def tearDown(self):
        if os.path.exists(os.path.dirname(self.zodb.db_dir)):
            shutil.rmtree(os.path.dirname(self.zodb.db_dir))


    def test_create_database(self):
        # Test database creation
        db = self.zodb.create(db_dir='./unskript/db')
        self.assertIsNotNone(db)
        self.assertTrue(os.path.exists(os.path.join(self.zodb.db_dir, self.zodb.db_name)))

    def test_read_from_nonexistent_collection(self):
        # Test reading from a non-existent collection
        data = self.zodb.read(collection_name='nonexistent_collection')
        self.assertIsNone(data)

    def test_update_collection(self):
        # Test updating a collection
        test_data = {'key1': 'value1', 'key2': 'value2'}
        self.zodb.create(db_dir='./unskript/db')  
        self.zodb.update(collection_name='audit_trail', data=test_data)
        data = self.zodb.read(collection_name='audit_trail')
        self.assertEqual(data, test_data)

    def test_delete_database(self):
        # Test database deletion
        self.zodb.create(db_dir='./unskript/db')  
        self.assertTrue(os.path.exists(os.path.join(self.zodb.db_dir, self.zodb.db_name)))
        self.zodb.delete() 
        self.assertFalse(os.path.exists(os.path.join(self.zodb.db_dir, self.zodb.db_name)))


class TestSQLInterface(unittest.TestCase):
    def setUp(self):
        # Initialize SQLInterface for testing
        self.db_name = 'test_unskript_pss.db'
        self.db_dir = './unskript/db'
        self.table_name = 'AUDIT_TRAIL'
        self.schema_file = 'unskript_db_schema.json'

        # Use SQLInterface for setting up the test environment
        self.sql_interface = SQLInterface(db_name=self.db_name, db_dir=self.db_dir, table_name=self.table_name)
        self.sql_interface.create_table()

    def tearDown(self):
        # Clean up after tests
        self.sql_interface.close_connection()
        os.remove(os.path.join(self.db_dir, self.db_name))

    def test_create_read(self):
        # Test Create and Read operations
        
        # Data for insertion
        execution_data = {
            "execution_id": "123",
            "time_stamp": "2023-12-19T08:00:00Z",
            "connector": "k8s",
            "runbook": "somerunbook.ipynb",
            "summary": "Summary P/E/F",
            "check_name": "ABC",
            "failed_objects": json.dumps(["HELLO \n", "WORLD\n"]),
            "status": "PASS"
        }

        # Perform create operation
        self.sql_interface.create(execution_data)

        # Perform read operation
        retrieved_data = self.sql_interface.read({"execution_id": "123"})
        self.assertIsNotNone(retrieved_data)
        # Add assertions for the retrieved data

    def test_update_delete(self):
        # Test Update and Delete operations
        
        # Data for insertion
        execution_data = {
            "execution_id": "123",
            "time_stamp": "2023-12-19T08:00:00Z",
            "connector": "k8s",
            "runbook": "somerunbook.ipynb",
            "summary": "Summary P/E/F",
            "check_name": "ABC",
            "failed_objects": json.dumps(["HELLO \n", "WORLD\n"]),
            "status": "PASS"
        }

        # Perform create operation
        self.sql_interface.create(execution_data)

        # Perform update operation
        new_data = {
            "execution_id": "123",
            "time_stamp": "2023-12-20T08:00:00Z",
            "connector": "k8s",
            "runbook": "somerunbook.ipynb",
            "summary": "Summary P/E/F",
            "check_name": "ABC",
            "failed_objects": json.dumps(["HELLO \n", "WORLD\n"]),
            "status": "PASS"
        }
        self.sql_interface.update(new_data=new_data, filters={"execution_id": "123"})

        # Perform read operation after update
        updated_data = self.sql_interface.read({"execution_id": "123"})
        updated_data = updated_data[0]
        self.assertEqual(updated_data["time_stamp"], "2023-12-20T08:00:00Z")
        # Add other assertions for the updated data

        # Perform delete operation
        self.sql_interface.delete(filters={"execution_id": "123"})

        # Perform read operation after delete
        deleted_data = self.sql_interface.read({"execution_id": "123"})
        self.assertIsNone(deleted_data)




if __name__ == '__main__':
    unittest.main()

