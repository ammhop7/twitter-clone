from fastapi import FastAPI

app = FastAPI(title='Twitter Clone')

@app.get('/')
async def root():
    return {'message': 'ok'}