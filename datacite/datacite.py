from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
import requests

from .models import DataCiteMetadata, DataCiteMetadataList, DataCiteDOIEvent


class DataCiteAPIClient:

    def __init__(self, request: Request):
        config = request.app.extra['config']
        self.api_url = 'https://api.test.datacite.org' if config.DATACITE_TESTING else 'https://api.datacite.org'
        self.prefix = config.DOI_PREFIX
        self.username = config.DATACITE_USERNAME
        self.password = config.DATACITE_PASSWORD
        self.timeout = (5, 60)

    def list_dois(self, page_size: int, page_num: int) -> DataCiteMetadataList:
        """
        Get a list of metadata records from DataCite, which have a DOI matching our configured prefix.

        Note: Using DataCite's ``page[number]`` query parameter we can fetch a maximum of 10,000 records in total.
        If this limit becomes problematic, we will have to switch to using the ``page[cursor]`` query parameter.
        DataCite's pagination methods are described here: https://support.datacite.org/docs/pagination

        :param page_size: the number of records to be returned per page
        :param page_num: the page number
        :return: DataCiteMetadataList
        """
        result = self._request('GET', '/dois/', params={
            'query': 'id:{prefix}/*'.format(prefix=self.prefix),
            'page[size]': page_size,
            'page[number]': page_num,
        })

        return DataCiteMetadataList(
            records=[DataCiteMetadata(
                doi=item['id'],
                metadata=item['attributes'],
            ) for item in result['data']],
            total_records=result['meta']['total'],
            total_pages=result['meta']['totalPages'],
            this_page=result['meta']['page'],
        )

    def add_doi(self, doi: str, metadata: dict) -> DataCiteMetadata:
        """
        Add a metadata record to DataCite in ``draft`` state. This will fail if
        the DOI already exists on DataCite.

        :param doi: the new DOI string
        :param metadata: the metadata dictionary
        :return: DataCiteMetadata
        """
        metadata['doi'] = doi
        metadata.pop('event', None)  # ensure that the input doesn't trigger a state change
        payload = {
            'data': {
                'attributes': metadata,
            }
        }
        result = self._request('POST', '/dois/', json=payload)

        return DataCiteMetadata(
            doi=result['data']['id'],
            metadata=result['data']['attributes'],
        )

    def get_doi(self, doi: str) -> DataCiteMetadata:
        """
        Fetch a metadata record from DataCite.

        :param doi: the DOI string
        :return: DataCiteMetadata
        """
        result = self._request('GET', '/dois/{doi}'.format(doi=doi))

        return DataCiteMetadata(
            doi=result['data']['id'],
            metadata=result['data']['attributes'],
        )

    def update_doi(self, doi: str, metadata: dict) -> DataCiteMetadata:
        """
        Update a metadata record on DataCite. This will add the record (in ``draft`` state)
        if the DOI does not exist on DataCite.

        :param doi: the DOI string
        :param metadata: the metadata dictionary
        :return: DataCiteMetadata
        """
        metadata.pop('event', None)  # ensure that the input doesn't trigger a state change
        payload = {
            'data': {
                'id': doi,
                'attributes': metadata,
            }
        }
        result = self._request('PUT', '/dois/{doi}'.format(doi=doi), json=payload)

        return DataCiteMetadata(
            doi=result['data']['id'],
            metadata=result['data']['attributes'],
        )

    def delete_doi(self, doi: str) -> None:
        """
        Delete a metadata record from DataCite.

        :param doi: the DOI string
        :return: None
        """
        self._request('DELETE', '/dois/{doi}'.format(doi=doi))

    def change_doi_state(self, doi: str, event: DataCiteDOIEvent) -> DataCiteMetadata:
        """
        Change the state of a metadata record on DataCite.

        :param doi: the DOI string
        :param event: the state change event to trigger
        :return: DataCiteMetadata
        """
        payload = {
            'data': {
                'id': doi,
                'attributes': {'event': event.name},
            }
        }
        result = self._request('PUT', '/dois/{doi}'.format(doi=doi), json=payload)

        return DataCiteMetadata(
            doi=result['data']['id'],
            metadata=result['data']['attributes'],
        )

    def _request(self, method, path, **kwargs):
        headers = {}
        if method in ('GET', 'POST', 'PUT'):
            headers['Accept'] = 'application/vnd.api+json'
        if method in ('POST', 'PUT'):
            headers['Content-Type'] = 'application/vnd.api+json'
        try:
            r = requests.request(method, self.api_url + path, **kwargs,
                                 auth=(self.username, self.password),
                                 timeout=self.timeout,
                                 headers=headers)
            r.raise_for_status()
            if r.content:
                return r.json()

        except requests.HTTPError as e:
            try:
                error_detail = e.response.json()
            except ValueError:
                error_detail = e.response.reason
            raise HTTPException(status_code=e.response.status_code, detail=error_detail)

        except requests.RequestException as e:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
