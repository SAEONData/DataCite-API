import pkg_resources

from fastapi import FastAPI, Depends
import uvicorn
from dotenv import load_dotenv

from datacite import config, routes, security

load_dotenv()

app = FastAPI(
    title="DataCite API",
    version=pkg_resources.require('DataCite-API')[0].version,
    config=config.Config(),
)

app.include_router(
    routes.router,
    dependencies=[Depends(security.Authorizer())],
)

if __name__ == '__main__':
    uvicorn.run(app, host=app.extra['config'].SERVER_HOST, port=app.extra['config'].SERVER_PORT)
