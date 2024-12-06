from datetime import datetime
from pprint import pprint

from pydantic import Field, UUID1, field_serializer

from PyOData1C.http import Connection, auth
from PyOData1C.models import OdataModel
from PyOData1C.odata import OData


class StageModel(OdataModel):
    uid_1c: UUID1 = Field(alias='Ref_Key',
                          exclude=True)
    number: str = Field(alias='Number')
    stage_date: datetime = Field(alias='Date')


    @field_serializer('stage_date')
    def serialize_stage_date(self, stage_date: datetime, _info):
        return stage_date.isoformat('T', 'seconds')


class StageOdata(OData):
    database = 'erp_dev'
    entity_model = StageModel
    entity_name = 'Document_ЭтапПроизводства2_2'


data = {'Number': 's2', 'Date': '2024-11-01T00:00:00'}


with Connection('erp.polipak.local',
                'http',
                auth.HTTPBasicAuth('КравцунАВ'.encode(), '2882ak')) as conn:

    stage = StageOdata.manager(conn).create(data)
    pprint(stage)

