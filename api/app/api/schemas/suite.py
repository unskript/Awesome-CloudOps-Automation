from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel
import json

class CheckConfig(BaseModel):
    id: str
    params: dict
    priority: str
    muted: bool = False
    suite_id: str

    def to_dict(self):
        # Convert the SuiteBase model to a dictionary
        checks_config_dict = self.model_dump()
        # Convert the config field to a string using json.dumps
        checks_config_dict['params'] = json.dumps(checks_config_dict['params'])
        return checks_config_dict


class SuiteConfig(BaseModel):
    schedule: str
    notify: bool
    ai_analysis: bool

class Suite(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    config: SuiteConfig
    checks: List[CheckConfig]

    def to_dict(self):
        # Convert the SuiteBase model to a dictionary
        suite_dict = self.model_dump()
        # Convert the config field to a string using json.dumps
        suite_dict['config'] = json.dumps(suite_dict['config'])
        return suite_dict
    

class CreateSuiteRequest(Suite):
    pass

class CreateSuiteResponse(Suite):
    pass