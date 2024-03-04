from api.schemas.suite import CreateSuiteRequest, CreateSuiteResponse, SuiteConfig, CheckConfig
from db.database import db_repository
import json
from db.models.suite import convert_suite_to_db_schema, convert_check_config_to_db_schema, convert_check_config_to_api_object


def create_suite(suite: CreateSuiteRequest) -> CreateSuiteResponse:
    # Create Suite
    db_suite = convert_suite_to_db_schema(suite)
    db_repository.insert(db_suite)

    # Create CheckConfigurations
    check_configs = []
    for check_config in suite.checks:
        db_check = convert_check_config_to_db_schema(check_config, db_suite.id)
        check_configs.append(db_check)

    db_repository.insert_many(check_configs)

    new_check_configs = [convert_check_config_to_api_object(check_config) for check_config in check_configs]

    new_suite_configs = json.loads(db_suite.config)
    return CreateSuiteResponse(id=db_suite.id,
                               name=db_suite.name, 
                               description=db_suite.description, 
                               config=SuiteConfig(**new_suite_configs),
                               checks=new_check_configs)


# def get_suite_by_id(suite_id: Suite.id) -> CreateSuiteResponse:
#     db_suite = db_repository.find_by_id(Suite, suite_id)
#     suite = {column.key: getattr(db_suite, column.key) for column in db_suite.__table__.columns}
#     suite['config'] = json.loads(suite['config'])
#     suite_checks = db_repository.find_by_parent_id(CheckConfiguration, suite_id, "suite_id")
#     suite['checks'] = []
#     for check in suite_checks:
#         check.params = json.loads(check.params)
#         suite['checks'].append(CheckConfiguration()))
#     suitee = CreateSuiteResponse(**suite)

#     return suitee