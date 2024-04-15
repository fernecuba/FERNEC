import uvicorn
from fastapi import FastAPI
from fernec.predict import router as predict_router
from manage.get_state import router as state_router

def get_application() -> FastAPI:
    application = FastAPI(title='FERNEC API')

    #Add routers
    application.include_router(predict_router)
    application.include_router(state_router)
    return application


app = get_application()

if __name__ == "__main__":
    print('Starting FERNEC backend') # TO DO: Set a logger
    uvicorn.run(app)
