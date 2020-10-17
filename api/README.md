# easy-way-api

## Docker

### Building the Image

```sh
docker build -t easy-way-api:test -f Dockerfile .
```

### Running the Image

```sh
docker run -p 8080:8080 easy-way-api:test
```

## Swagger UI

You can navigate to `localhost:8080/api/v1/ui` to use the user interface.
