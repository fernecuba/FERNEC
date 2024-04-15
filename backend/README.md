# Backend for FERNEC
PoC based on the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)

## To install requirements

`pip install -r requirements.txt`

## Setting Up

Before running the `predict.py` script, you need to set the `MODEL_PATH` environment variable to the path of your model file.

```export MODEL_PATH="/path/to/your/model/file"```

## To run the server

`python main.py`

You can check it is running at [localhost 8000](http://127.0.0.1:8000)


Also you could try [this request](http://127.0.0.1:8000/items/5?q=somequery)

## Testing

Simply run `pytest`

## Documentation

See the docs
- Swagger at: http://127.0.0.1:8000/docs
- Redoc at: http://127.0.0.1:8000/redoc

See OpenApi specification
http://127.0.0.1:8000/openapi.json
