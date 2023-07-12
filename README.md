# Epson Connect

This library provides a wrapper for the Epson Connect API.

NB: This library is very much still in beta.

## Install

```
pip install epson-connect
```

## Usage

```python
import epson_connect

ec = epson_connect.Client(
    printer_email='...',
    client_id='...',
    client_secret='...',
)

# Or with these enviornment variables defined...
# export EPSON_CONNECT_API_PRINTER_EMAIL=<an email address for the device>
# export EPSON_CONNECT_API_CLIENT_ID=<client id>
# export EPSON_CONNECT_API_CLIENT_SECRET=<client secret>
# ec = epson_connect.Client()

# Print a PDF.
job_id = ec.printer.print('./path/to/file.pdf')

# List scan destinations.
ec.scanner.list()
```

### Tests

```
tox
```

### Deployment

```
poetry build
poetry publish
```
