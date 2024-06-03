from sqlmodel import Session

from ..models import Prediction


def create_prediction(session: Session, unique_id: str, email: str):
    prediction = Prediction(uuid4=unique_id, email=email, status="processing")
    db_obj = Prediction.model_validate(prediction)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
