from api.schemas.suite import CreateSuiteRequest, CreateSuiteResponse, SuiteConfig, CheckConfig
from db.database import db_repository
import json
import uuid

def create_suite(suite: CreateSuiteRequest) -> CreateSuiteResponse:
    # Create Suite
    suite_config = suite.config.model_dump_json()
    suite_model = db_repository.models.get["suite"]
    suite_model.id = str(uuid.uuid4())
    suite_model.name = suite.name
    suite_model.description = suite.description
    suite_model.config = suite_config
    db_repository.insert(suite_model)

    # Create CheckConfigurations
    check_configs = []
    for check_config in suite.checks:
        check_config_params = json.dumps(check_config.params)
        checks_config_model = db_repository.models.get["checksConfiguration"]
        checks_config_model.id = str(uuid.uuid4())
        checks_config_model.params = check_config_params
        checks_config_model.muted = check_config.muted
        checks_config_model.suite_id = suite_model.id
        check_configs.append(checks_config_model)

    db_repository.insert_many(check_configs)
    new_check_configs = []
    for check_config in check_configs:
        check_config.params = json.loads(check_config.params)
        new_check_configs.append(CheckConfig(**check_config.__dict__))

    new_suite_configs = json.loads(suite_model.config)
    return CreateSuiteResponse(id=suite_model.id,
                               name=suite_model.name, 
                               description=suite_model.description, 
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