from src.api.controllers import auth_controller
from src.api.controllers import pedido_controller
from src.api.controllers import fidelidade_controller
from src.api.controllers import usuario_controller
from src.api.controllers import unidade_controller
from src.api.controllers import cardapio_controller
from src.api.controllers import pagamento_controller
from src.api.controllers import cozinha_controller
from src.api.controllers import produto_controller
from src.infrastructure.logging_config import setup_logging
from fastapi import FastAPI, HTTPException
from src.api.exceptions.exception_handler import (
    http_exception_handler,
    generic_exception_handler
)

setup_logging()

app = FastAPI(
    title="API Raízes do Nordeste",
    description="""
Backend de API para gerenciamento de pedidos, produtos, estoque e fidelidade.

## Funcionalidades:
- Cadastro de usuários
- Gestão de produtos e cardápio
- Criação de pedidos
- Processamento de pagamentos
- Programa de fidelidade

## Regras importantes:
- Apenas GERENTE pode cadastrar produtos/unidades
- Cliente só acessa seus próprios pedidos
- Estoque é validado automaticamente
""",
    version="1.0.0",
    contact={
        "name": "Equipe Raízes",
        "email": "suporte@raizes.com"
    }
)


@app.get("/")
def home():
    return {"message": "API Raízes do Nordeste funcionando"}


app.include_router(usuario_controller.router)
app.include_router(unidade_controller.router)
app.include_router(produto_controller.router)
app.include_router(cardapio_controller.router)

app.include_router(pedido_controller.router)
app.include_router(pagamento_controller.router)

app.include_router(fidelidade_controller.router)
app.include_router(cozinha_controller.router)

app.include_router(auth_controller.router) 

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
