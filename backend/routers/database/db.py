from sqlmodel import Session, create_engine


def get_db_engine(db_uri):
    # return create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    return create_engine(db_uri)
