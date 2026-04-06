from fastapi import FastAPI
from src.api.controllers import auth_controller
from src.api.controllers import pedido_controller
from src.api.controllers import fidelidade_controller
from src.api.controllers import usuario_controller
from src.api.controllers import unidade_controller
from src.api.controllers import cardapio_controller
from src.api.controllers import pagamento_controller
from src.api.controllers import cozinha_controller
from src.api.controllers import produto_controller

app = FastAPI(
    title="API Raízes do Nordeste",
    description="Backend do sistema de pedidos",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "API Raízes do Nordeste funcionando"}


# ✅ Rotas principais
app.include_router(usuario_controller.router)
app.include_router(unidade_controller.router)
app.include_router(produto_controller.router)
app.include_router(cardapio_controller.router)

# ✅ Fluxo de pedido
app.include_router(pedido_controller.router)
app.include_router(pagamento_controller.router)

# ✅ Fluxos auxiliares
app.include_router(fidelidade_controller.router)
app.include_router(cozinha_controller.router)

app.include_router(auth_controller.router)  
