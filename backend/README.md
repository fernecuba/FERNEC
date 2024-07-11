# Backend for FERNEC
PoC based on the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/)

## Run with Docker

### Requirements

- Create a folder named `models`
- Place the CNN and RNN models in the `models` folder
- Specify the path to the models in the config.yml file 

### Run

- ```make build```
- ```make start```

## Run without Docker

### To install requirements

`pip install -r requirements.txt`

### Setting Up

Before running the `predict.py` script, you need to set the `MODEL_CNN_PATH` and `MODEL_RNN_PATH` environment variables to the path of your model file.

```export MODEL_CNN_PATH="/path/to/your/cnn_model/file"```
```export MODEL_RNN_PATH="/path/to/your/rnn_model/file"```

### To run the server

`python main.py`

You can check it is running at [localhost 8000](http://127.0.0.1:8000)


Also you could try [this request](http://127.0.0.1:8000/items/5?q=somequery)

## Testing

Step onto `/backend` with `cd backend`

Run `python3 -m pytest`

To check coverage you can use `coverage run -m pytest` and then `coverage html -i`. File coverage will be saved onto `backend/htmlcov`


## Documentation

See the docs
- Swagger at: http://127.0.0.1:8000/docs
- Redoc at: http://127.0.0.1:8000/redoc

See OpenApi specification
http://127.0.0.1:8000/openapi.json
