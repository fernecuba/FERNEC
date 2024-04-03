# backend for FERNEC
PoC based on the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)

To install requirements

`$ pip install -r requirements.txt`

To run the server

`uvicorn main:app --reload`

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
