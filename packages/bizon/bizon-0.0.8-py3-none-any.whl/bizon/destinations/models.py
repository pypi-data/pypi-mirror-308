import json
from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field
from pytz import UTC

from bizon.source.models import SourceRecord


class DestinationRecord(BaseModel):
    bizon_id: str = Field(..., description="Bizon unique identifier of the record")
    bizon_extracted_at: datetime = Field(..., description="Datetime when the record was extracted")
    bizon_loaded_at: datetime = Field(..., description="Datetime when the record was loaded")
    source_record_id: str = Field(..., description="Source record id")
    source_timestamp: datetime = Field(..., description="Timestamp of the source record")
    source_data: dict = Field(..., description="Source record JSON as dict")

    @classmethod
    def from_source_record(cls, source_record: SourceRecord, extracted_at: datetime) -> "DestinationRecord":
        return cls(
            bizon_id=uuid4().hex,
            bizon_extracted_at=extracted_at,
            bizon_loaded_at=datetime.now(tz=UTC),
            source_record_id=source_record.id,
            source_timestamp=source_record.timestamp,
            source_data=source_record.data,
        )

    def to_dict_raw_json_data(self, parquet: bool = False) -> str:
        """Return the record as a dict with raw JSON data"""

        if parquet:
            return {
                "_bizon_id": self.bizon_id,
                "_bizon_extracted_at": int(self.bizon_extracted_at.timestamp() * 1_000_000),
                "_bizon_loaded_at": self.bizon_loaded_at.timestamp(),
                "_source_record_id": self.source_record_id,
                "_source_timestamp": int(self.source_timestamp.timestamp() * 1_000_000),
                "_source_data": json.dumps(self.source_data),
            }

        return {
            "_bizon_id": self.bizon_id,
            "_bizon_extracted_at": self.bizon_extracted_at,
            "_bizon_loaded_at": self.bizon_loaded_at,
            "_source_record_id": self.source_record_id,
            "_source_timestamp": self.source_timestamp,
            "_source_data": json.dumps(self.source_data),
        }
