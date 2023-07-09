# Epson Connect

This library provides a wrapper for the Epson Connect API.

NB: This library is very must still in alpha.

## Install

```
pip install epson-connect
```

## Usage

```python
import epson_connect

ec = espon_connect.Client(
    printer_email='...',
    client_id='...',
    client_secret='...',
)

# Or with these enviornment variables defined...
# export ESPON_CONNECT_API_PRINTER_EMAIL=<an email address for the device>
# export ESPON_CONNECT_API_CLIENT_ID=<client id>
# export ESPON_CONNECT_API_CLIENT_SECRET=<client secret>
# ec = espon_connect.Client()

job_id = ec.printer.print('./path/to/file.pdf')
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
