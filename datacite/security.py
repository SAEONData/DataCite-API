from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from starlette.requests import Request
from starlette.status import HTTP_503_SERVICE_UNAVAILABLE
import requests


class Authorizer(HTTPBearer):

    async def __call__(self, request: Request):
        """
        Validate the access token that was supplied in the Authorization header.

        :raises HTTPException: if the token is invalid or the user has insufficient privileges
        """
        config = request.app.extra['config']
        if config.NO_AUTH:
            return {}

        http_auth = await super().__call__(request)
        access_token = http_auth.credentials

        try:
            r = requests.post(config.ACCOUNTS_API_URL + '/authorization/',
                              json={
                                  'token': access_token,
                                  'audience': config.OAUTH2_AUDIENCE,
                                  'scope': config.OAUTH2_SCOPE,
                                  'super_roles': config.ALLOWED_ROLES,
                              },
                              headers={
                                  'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                              },
                              verify=config.SERVER_ENV != 'development',
                              timeout=5.0 if config.SERVER_ENV != 'development' else 300,
                              )
            r.raise_for_status()

        except requests.HTTPError as e:
            try:
                detail = e.response.json()
            except ValueError:
                detail = e.response.reason
            raise HTTPException(status_code=e.response.status_code, detail=detail) from e

        except requests.RequestException as e:
            raise HTTPException(status_code=HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)) from e
