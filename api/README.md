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
