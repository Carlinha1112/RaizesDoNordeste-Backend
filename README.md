   # Raízes do Nordeste — Backend API

   API REST para gerenciamento de pedidos, cardápio, estoque e fidelidade da rede de lanchonetes **Raízes do Nordeste**.

   Desenvolvido com **FastAPI**, **SQLAlchemy** e **SQLite**.
   Projeto Multidisciplinar — Trilha Back-End — **UNINTER 2026**.

   Autor: Carla Adriana Duarte Muller

   ---

   ## Tecnologias

   * Python 3.11+
   * FastAPI 0.135+
   * SQLAlchemy 2.0
   * SQLite
   * Passlib (hash de senha — `pbkdf2_sha256`)
   * python-jose (JWT)
   * Pydantic v2
   * Uvicorn

   ---

   ## Requisitos

   * Python 3.11 ou superior instalado
   * pip atualizado

   ```bash
   pip install --upgrade pip
   ```

   ---

   ## Como configurar

   ### 1. Clone o repositório

   ```bash
   git clone https://github.com/Carlinha1112/RaizesDoNordeste-Backend.git
   cd RaizesDoNordeste-Backend
   ```

   ### 2. Crie e ative o ambiente virtual

   ```bash
   python -m venv venv
   ```

   **Windows**

   ```bash
   venv\Scripts\activate
   ```

   **Linux / Mac**

   ```bash
   source venv/bin/activate
   ```

   ### 3. Instale as dependências

   ```bash
   pip install -r requirements.txt
   ```

   ### 4. Configure as variáveis de ambiente

   Crie um arquivo `.env` na raiz do projeto:

   ```env
   SECRET_KEY=sua_chave_secreta_forte_aqui
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   DATABASE_URL=sqlite:///./database.db
   ```

   > Nunca compartilhe seu arquivo `.env`.

   ---

   ## Como criar o banco de dados

   O projeto usa SQLite com criação automática das tabelas via SQLAlchemy.

   ```bash
   python -m src.infrastructure.database.create_tables
   ```

   Será criado o arquivo:

   ```text
   database.db
   ```

   ---

   ## Como iniciar a API

   ```bash
   uvicorn src.main:app --reload
   ```

   API disponível em:

   ```text
   http://localhost:8000
   ```

   ---

   ## Documentação da API

   ### Swagger UI

   ```text
   http://localhost:8000/docs
   ```

   ### ReDoc

   ```text
   http://localhost:8000/redoc
   ```

   ---

   ## Estrutura do Projeto

   ```text
   src/
   ├── api/
   │   ├── controllers/      # Rotas e endpoints
   │   ├── dependencies/     # JWT e roles
   │   ├── exceptions/       # Handler global de erros
   │   └── schemas/          # Request / Response (Pydantic)
   │
   ├── application/
   │   └── services/         # Regras de negócio
   │
   ├── domain/
   │   └── entities/         # Entidades SQLAlchemy
   │
   ├── infrastructure/
   │   ├── database/         # Sessão e conexão
   │   ├── repositories/     # Persistência
   │   └── logging_config.py
   │
   ├── core/
   │   └── security.py       # JWT e autenticação
   │
   └── main.py               # Inicialização FastAPI
   ```

   ---

   ## Endpoints Principais

   | Método | Rota                             | Descrição                             | Acesso                        |
   | ------ | ------------------------------   | ------------------------------------- | ----------------------------- |
   | POST   | `/auth/login`                    | Login e token JWT                     | Público                       |
   | POST   | `/usuarios/`                     | Cadastrar usuário                     | Público                       |
   | GET    | `/usuarios/{id}`                 | Buscar usuário                        | GERENTE                       |
   | GET    | `/unidades/`                     | Listar unidades                       | JWT                           |
   | POST   | `/unidades/`                     | Criar unidade                         | GERENTE                       |
   | GET    | `/produtos/`                     | Listar produtos                       | JWT                           |
   | POST   | `/produtos/`                     | Criar produto                         | GERENTE                       |
   | GET    | `/cardapios/`                    | Listar cardápios                      | JWT                           |
   | POST   | `/pedidos/`                      | Criar pedido                          | CLIENTE / ATENDENTE           |
   | GET    | `/pedidos/`                      | Listar pedidos (Gerente filtra canal) | JWT                           |
   | GET    | `/pedidos/{id}`                  | Buscar pedido                         | JWT                           |
   | DELETE | `/pedidos/{id}`                  | Cancelar pedido                       | CLIENTE / ATENDENTE / GERENTE |
   | POST   | `/pagamentos/{pedido_id}`        | Processar pagamento                   | CLIENTE /ATENDENTE            |
   | GET    | `/fidelidade/me`                 | Consultar meus pontos                 | JWT                           |
   | GET    | `/fidelidade/{usuario_id}`       | Consultar pontos de qualquer usuário  | GERENTE                       |
   | GET    | `/cozinha/aguardando`            | Lista pedidos aguardando preparo      | ATENDENTE / GERENTE           |
   | GET    | `/cozinha/em-preparo`            | Lista pedidos em preparo              | ATENDENTE / GERENTE           |
   | GET    | `/cozinha/prontos`               | Lista pedidos prontos                 | ATENDENTE / GERENTE           |
   | PATCH  | `/cozinha/{pedido_id}/iniciar`   | Inicia preparo do pedido              | ATENDENTE / GERENTE           |
   | PATCH  | `/cozinha/{pedido_id}/pronto`    | Marca pedido como pronto              | ATENDENTE / GERENTE           |
   | PATCH  | `/cozinha/{pedido_id}/finalizar` | Finaliza o pedido / entrega concluída | ATENDENTE / GERENTE           |
   
   ### Filtro por canal de pedido

   Disponível para perfil **GERENTE**:

   ```http
   GET /pedidos/?canal=APP
   GET /pedidos/?canal=TOTEM
   GET /pedidos/?canal=BALCAO
   GET /pedidos/?canal=PICKUP
   ```

   ## Autenticação

   A API utiliza **JWT Bearer Token**.

   ### Login

   ```http
   POST /auth/login
   Content-Type: application/x-www-form-urlencoded
   ```

   ```text
   username=email@exemplo.com
   password=SuaSenha123
   ```

   ### Uso do token

   ```http
   Authorization: Bearer SEU_TOKEN
   ```

   No Swagger (`/docs`), clique em **Authorize** e cole o token.

   ---

   ## Perfis de Usuário

   | Perfil    | Permissões                                           |
   | --------- | ---------------------------------------------------- |
   | CLIENTE   | Criar pedido, consultar próprios pedidos, fidelidade |
   | ATENDENTE | Acompanhar cozinha e atualizar preparo               |
   | GERENTE   | Acesso completo                                      |

   ---

   ## Canal do Pedido

   Todo pedido deve informar `canal_pedido`.

   | Valor  | Canal                 |
   | ------ | --------------------- |
   | APP    | Aplicativo móvel      |
   | TOTEM  | Totem autoatendimento |
   | BALCAO | Atendimento balcão    |
   | PICKUP | Retirada rápida       |

   ### Exemplo

   ```json
   {
   "id_unidade": 1,
   "canal_pedido": "TOTEM",
   "itens": [
      {
         "produto_id": 1,
         "quantidade": 2
      }
   ],
   "pontos_utilizados": 0
   }
   ```

   ---

   ## Fluxo Crítico

   ```text
   1. POST /pedidos/
      → Pedido criado (AGUARDANDO_PAGAMENTO)

   2. POST /pagamentos/{pedido_id}
      → Pagamento processado

   3. Se aprovado:
      → status = PAGO
      → baixa no estoque
      → crédito fidelidade

   4. PATCH /cozinha/{id}/iniciar
      → status = EM_PREPARO

   5. PATCH /cozinha/{id}/pronto
      → status = PRONTO

   6. PATCH /cozinha/{id}/finalizar
      → status = FINALIZADO
   ```

   ---

   ## Testes (Postman / Insomnia)

   Arquivo disponível no repositório:

   ```text
   postman_collection.json
   ```

   ### Ordem sugerida

   1. Login
   2. Criar usuário cliente
   3. Criar unidade
   4. Criar produto
   5. Criar pedido
   6. Processar pagamento
   7. Consultar status
   8. Testar erros (401, 403, 404, 409, 422)

   ---

   ## Logs

   Gerados em:

   * Console
   * `app.log`

   ### Eventos registrados

   * Pagamentos
   * Acessos negados
   * Erros internos
   * Exceptions

   ---

   ## Segurança e LGPD

   * Senhas armazenadas com hash seguro
   * Nunca retorna `senha_hash`
   * Dados pessoais usados apenas para operação
   * Fidelidade exige consentimento
   * JWT com expiração configurável

   ---

   ## Repositório

   GitHub:

   ```text
   https://github.com/Carlinha1112/RaizesDoNordeste-Backend
   ```
