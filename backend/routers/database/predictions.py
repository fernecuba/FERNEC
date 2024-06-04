from supabase import Client

# TODO: define dtos and return Prediction model
# from ..models import Prediction


def create_prediction(client: Client, unique_id: str, email: str):
    data = (client.table("predictions").
            insert({"uuid4": unique_id, "email": email, "status": "processing"}).
            execute())
    assert len(data.data) == 1
    return data.data[0]


def get_prediction(client: Client, unique_id: str):
    data = client.table("predictions").select("*").eq("uuid4", unique_id).execute()
    if len(data.data) == 0:
        return None
    return data.data[0]


def update_prediction(client: Client, unique_id: str, prediction: dict):
    data = client.table("predictions").update(prediction).eq("uuid4", unique_id).execute()
    assert len(data.data) == 1
    return data.data[0]
