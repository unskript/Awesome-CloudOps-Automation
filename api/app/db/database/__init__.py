import os

db_repository = None

def initialize_db():
    global db_repository
    db_type = os.getenv("DB_TYPE")

    if db_type is None:
        raise Exception("Database type is not defined. Please define a database type in the configuration.")
    
    match db_type:
        case "sqlite":
            from db.database.sqllite import SQLLiterepository
            print("db_repoo is SQL")
            db_url = os.getenv("DATABASE_URL")
            db_repository = SQLLiterepository(db_url)
            db_repository.base.metadata.create_all(bind=db_repository.engine)
            db_repository.connect()
        case _:
            raise Exception("Unknown database type. Please enter valid database type.")
        
initialize_db()