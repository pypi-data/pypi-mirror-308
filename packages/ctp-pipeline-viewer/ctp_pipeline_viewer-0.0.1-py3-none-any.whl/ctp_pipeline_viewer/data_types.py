import dataclasses
import datetime
import re
from enum import auto, StrEnum

import dateutil.parser
from pydantic import BaseModel, Field, AliasChoices, field_validator
from pydantic.dataclasses import dataclass


class View(StrEnum):
    IMPORT_QUEUE = auto()
    EXPORT_QUEUE = auto()
    QUARANTINES = auto()
    ARCHIVE = auto()
    PRE_ARCHIVE = auto()


CTP_VIEWS = {View.IMPORT_QUEUE, View.EXPORT_QUEUE, View.QUARANTINES}
XNAT_VIEWS = {View.ARCHIVE, View.PRE_ARCHIVE}


@dataclass
class ProjectConfig:
    ctp_url: str
    ctp_pipeline: str
    ctp_interval: int = 5
    xnat_url: str | None = None
    xnat_project: str | None = None
    xnat_interval: int = 5
    history = 13
    views: list[View] = Field(default_factory=list)


class Configs(BaseModel):
    interval: int = 5
    history: int = 13
    configs: list[ProjectConfig] = Field(default_factory=list)


class CtpSummary(BaseModel):
    pipeline: str = Field('', validation_alias=AliasChoices('Pipeline'))
    import_queues: int = Field(0, validation_alias=AliasChoices('ImportQueues'))
    export_queues: int = Field(0, validation_alias=AliasChoices('ExportQueues'))
    quarantines: int = Field(0, validation_alias=AliasChoices('Quarantines'))
    time_stamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now())  # pylint:disable=unnecessary-lambda

    @field_validator('import_queues', 'export_queues', 'quarantines', mode='before')
    @classmethod
    def remove_separators(cls, v: str) -> int:
        if isinstance(v, int):
            return v
        return int(v.replace(',', ''))


def _validate_date(v: str) -> datetime.datetime | None:
    v = v.replace('\xa0\xa0\xa0', ' ')
    try:
        val = dateutil.parser.parse(v)
        return val
    except dateutil.parser.ParserError:
        return None


class CtpBaseModel(BaseModel):
    name: str | None = None
    last_file_received: str | None = Field(None, validation_alias=AliasChoices('Last file received:'))
    last_file_received_at: datetime.datetime | None = Field(None, validation_alias=AliasChoices('Last file received at:'))
    last_file_supplied: str | None = Field(None, validation_alias=AliasChoices('Last file received:'))
    last_file_supplied_at: datetime.datetime | None = Field(None, validation_alias=AliasChoices('Last file supplied at:'))

    @field_validator('last_file_received_at', 'last_file_supplied_at', mode='before')
    @classmethod
    def validate_date(cls, v: str) -> datetime.datetime | None:
        return _validate_date(v)

    @field_validator('last_file_received', 'last_file_supplied', mode='before')
    @classmethod
    def validate_path(cls, v: str) -> str | None:
        if v == 'No activity':
            return None
        return v


class DirectoryImportService(CtpBaseModel):
    files_received: int = Field(-1, validation_alias=AliasChoices('Files received:'))
    queue_size: int = Field(-1, validation_alias=AliasChoices('Queue size:'))


class DicomFilter(CtpBaseModel):
    ...


class IDMap(CtpBaseModel):
    ...


class DicomAnonymizer(CtpBaseModel):
    ...


class DicomExportService(CtpBaseModel):
    export_enabled: bool = Field(False, validation_alias=AliasChoices('Export enabled:'))
    export_queue_size: int = Field(-1, validation_alias=AliasChoices('Export queue size:'))
    last_export_elapsed_time: str | None = Field(None, validation_alias=AliasChoices('Last export elapsed time:'))
    last_file_dequeued: str | None = Field(None, validation_alias=AliasChoices('Last file dequeued:'))
    last_file_dequeued_at: datetime.datetime | None = Field(None, validation_alias=AliasChoices('Last file dequeued at:'))

    @field_validator('last_file_received_at', 'last_file_supplied_at', 'last_file_dequeued_at', mode='before')
    @classmethod
    def validate_date(cls, v: str) -> datetime.datetime | None:
        return _validate_date(v)


class PerformanceLogger(CtpBaseModel):
    files_processed: int = Field(-1, validation_alias=AliasChoices('Files processed:'))


@dataclasses.dataclass
class RegexIn:
    string: str
    match: re.Match | None = None

    def __eq__(self, other: str | re.Pattern) -> bool:  # type: ignore
        if isinstance(other, str):
            other = re.compile(other)
        self.match = other.fullmatch(self.string)
        return self.match is not None


@dataclass
class CtpStatus:
    name: str
    elements: list[CtpBaseModel] = Field(default_factory=list)


@dataclass
class XnatExperimentInfo:
    archive: set[str] = Field(default_factory=set)
    pre_archive: set[str] = Field(default_factory=set)
    time_stamp: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now())  # pylint:disable=unnecessary-lambda


def has_ctp_views(config: ProjectConfig) -> bool:
    return len(set(config.views) & CTP_VIEWS) > 0


def has_xnat_views(config: ProjectConfig) -> bool:
    return len(set(config.views) & XNAT_VIEWS) > 0
