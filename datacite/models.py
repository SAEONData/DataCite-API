from typing import List
from enum import Enum

from pydantic import BaseModel, Field

# adapted from https://www.crossref.org/blog/dois-and-matching-regular-expressions
DOI_REGEX = r'^10\.\d{4,}(\.\d+)*/[-._;()/:a-zA-Z0-9]+$'


class DataCiteMetadata(BaseModel):
    doi: str = Field(..., regex=DOI_REGEX)
    metadata: dict


class DataCiteMetadataList(BaseModel):
    records: List[DataCiteMetadata]
    total_records: int
    total_pages: int
    this_page: int


class DataCiteDOIEvent(Enum):
    register = 'register'  # change state from draft to registered
    publish = 'publish'  # change state from draft or registered to findable
    hide = 'hide'  # change state from findable to registered
