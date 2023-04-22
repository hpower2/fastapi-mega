from src.main import app
import uvicorn


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8111, reload=True, workers=20)