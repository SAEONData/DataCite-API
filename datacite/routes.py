from fastapi import APIRouter, Depends, Query

from .datacite import DataCiteAPIClient
from .models import DataCiteMetadata, DataCiteMetadataList, DataCiteDOIEvent

router = APIRouter()


@router.get('/', response_model=DataCiteMetadataList)
async def list_records(
        *,
        datacite_api: DataCiteAPIClient = Depends(),
        page_size: int = Query(default=20, ge=1, le=1000),
        page_num: int = Query(default=1, ge=1),
):
    return datacite_api.list_dois(page_size, page_num)


@router.post('/', response_model=DataCiteMetadata)
async def create_or_update_record(
        *,
        datacite_api: DataCiteAPIClient = Depends(),
        metadata: DataCiteMetadata,
):
    return datacite_api.update_doi(metadata.doi, metadata.metadata)


@router.get('/{doi:path}', response_model=DataCiteMetadata)
async def get_record(
        *,
        datacite_api: DataCiteAPIClient = Depends(),
        doi: str,
):
    return datacite_api.get_doi(doi)


@router.delete('/{doi:path}')
async def delete_record(
        *,
        datacite_api: DataCiteAPIClient = Depends(),
        doi: str,
):
    datacite_api.delete_doi(doi)


@router.put('/{doi:path}', response_model=DataCiteMetadata)
async def change_record_state(
        *,
        datacite_api: DataCiteAPIClient = Depends(),
        doi: str,
        event: DataCiteDOIEvent,
):
    return datacite_api.change_doi_state(doi, event)
