
from fastapi import FastAPI
from auth.admin_auth import create_unlimited_access_token
from routers import url_scan_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Dragons Of Eden API",
    summary="Official API for the Dragons Of Eden platform",
    description="This API is exclusively developed for the Dragons Of Eden platform, enabling secure and efficient interaction with its services. Unauthorized access or use of this API is strictly prohibited and may result in legal action. By using this API, you agree to comply with all applicable terms, conditions, and policies. For more information, please visit our official website at [Dragons Of Eden](https://dragonsofeden.com/).",
    version="0.1.0",
    terms_of_service="https://www.dragonsofeden.com/terms-of-service",
    contact={
        "name": "Dragons Of Eden Discord Support Server",
        "url": "https://discord.com/invite/M5WVpvfW3G",
    },
    license_info={}
)

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def root():
    return {"Hello":"World"}

# Get this method when you want to add a new autorization token
#@app.post("/token")
def generate_unlimited_token(username: str):
    token = create_unlimited_access_token(data={"sub": username})
    return {"access_token": token}

app.include_router(url_scan_router.router)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

