from fastapi import FastAPI

app = FastAPI(
    title="API Raízes do Nordeste",
    description="Backend do sistema de pedidos",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "API Raízes do Nordeste funcionando"}