# DataCite API

***Note: DataCite integration is now provided by the Open-Data-Platform project***

A facade to the DOI functions of the [DataCite REST API](https://support.datacite.org/docs/api),
facilitating registration and management of DOI records with DataCite.

## Installation

### System dependencies

* Python 3.6

## Configuration

The service is configured using environment variables. For a local / non-containerised deployment,
these may be loaded from a `.env` file located in the project root directory. See `.env.example`
for an example configuration.

### Environment variables

#### Server config
- **`SERVER_ENV`**: deployment environment; `development` | `testing` | `staging` | `production`
- **`SERVER_HOST`**: IP address / hostname to listen on
- **`SERVER_PORT`**: port number to listen on

#### Security config
- **`ACCOUNTS_API_URL`**: URL of the ODP Accounts API, for access token validation
- **`OAUTH2_SCOPE`**: OAuth2 scope applicable to this service
- **`ALLOWED_ROLES`**: JSON-encoded list of roles that may access this service
- **`NO_AUTH`**: optional, default `False`; set to `True` to disable access token validation

#### DataCite integration
- **`DOI_PREFIX`**: our DOI prefix
- **`DATACITE_USERNAME`**: our DataCite username
- **`DATACITE_PASSWORD`**: our DataCite password
- **`DATACITE_TESTING`**: set to `True` to use the DataCite test API (optional, default `False` - use the live API)
