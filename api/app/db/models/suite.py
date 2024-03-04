from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database.sqllite import Base
from sqlalchemy import DateTime
from sqlalchemy.sql import func
import uuid
import json

from api.schemas.suite import Suite as ApiSuite
from api.schemas.suite import CheckConfig


class CheckConfiguration(Base):
    __tablename__ = "check_configurations"

    id = Column(String, primary_key=True)
    suite_id = Column(String, ForeignKey('suites.id'))
    params = Column(String)
    priority = Column(String)
    muted = Column(Boolean)

class Suite(Base):
    __tablename__ = "suites"

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    config = Column(String)
    checks = relationship("CheckConfiguration", back_populates="suite")

CheckConfiguration.suite = relationship("Suite", back_populates="checks")



def convert_suite_to_db_schema(suite:ApiSuite):
    suite_config = suite.config.model_dump_json()
    id = str(uuid.uuid4())
    return Suite(id=id,name=suite.name, description=suite.description, config=suite_config)

def convert_suite_to_api_object(suite:Suite):
    pass


def convert_check_config_to_db_schema(check_config, suite_id):
    check_config_params = json.dumps(check_config.params)
    return CheckConfiguration(id=str(uuid.uuid4()),
                              params=check_config_params,
                              priority=check_config.priority, 
                              muted=check_config.muted, 
                              suite_id=suite_id)

def convert_check_config_to_api_object(check_config:CheckConfiguration):
    check_config.params = json.loads(check_config.params)
    return CheckConfig(**check_config.__dict__)