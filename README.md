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

   ## Testes da API (Postman)

   A API possui uma coleção completa de testes no Postman disponível no repositório:

   ```text
   docs/RaizesDoNordeste_Postman_Collection.json
   ```

   ### Como executar os testes

   1. Inicie a API
  
   ```bash
   # Ativar ambiente
   source venv/bin/activate   # Linux/Mac
   .\venv\Scripts\activate    # Windows

   # Rodar API
   uvicorn src.main:app --reload
   ```
   2. Abra o Postman
   3. Importe a coleção .json
   4. Configure a variável de ambiente

   base_url = http://localhost:8000
   
   5. Execute os testes na ordem abaixo

   ### Setup A (Básico)

   Criação de usuários e unidades
   Ordem:
   1. Criar usuário sistema
   2. Criar usuário gerente
   3. Login gerente
   4. Criar unidade Curitiba Centro
   5. Criar unidade Curitiba Cabral
   6. Criar atendentes
   7. Criar clientes
   8. Login atendentes e clientes

   ### Setup B (Completo)
   Requer Setup A

   Configuração de estoque e cardápio:
   1. Ingredientes
   2. Estoque por unidade
   3. Produtos
   4. Cardápio
   5. CardápioProduto

   ### Testes
   Autenticação e Autorização
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T01	|Login válido	                           |200 + JWT          |
   |T02	|Login inválido	                        |401                |
   |T03	|Sem token	                              |401                |
   |T04	|Sem permissão	                           |403                |
   
   Pedidos
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T05	|Pedido válido	                           |200 OK             |
   |T06	|Pedido sem itens	                        |422                |
   |T07	|Estoque insuficiente                     |409                |
   |T08	|Quantidade inválida                      |422                |
   |T09	|Produto inexistente                      |404                |
   
   Pagamentos
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T10	|Pagamento aprovado (PIX)	               |Pedido → PAGO      |
   |T11	|Pagamento recusado	                     |Mantém pendente    |
   
   Fidelidade
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T12	|Relatório fidelidade por usuário         |200 OK             |
   
   Estoque
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T13	|Relatório de estoque	                  |200 OK             | 
   
   Auditoria (Logs)
   |ID	|Cenário	                                 |Resultado esperado |
   |-----|-----------------------------------------|-------------------|
   |T14	|Listar auditoria	                        |200 OK             |
   |T15	|Criação de pedido gera registro de log	|Registro criado    |
   
    
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
   ---
   ## 📬 Coleção Postman

   A API possui uma coleção completa no Postman com todos os endpoints prontos para teste.

   📁 Arquivo da coleção:

   [Baixar coleção Postman](docs/RaizesDoNordeste_Postman_Collection.json)

   ### Como usar

   1. Abra o Postman
   2. Clique em **Import**
   3. Selecione o arquivo `.json`
   4. Execute os endpoints

   ### Funcionalidades testadas

   - Autenticação JWT
   - Usuários
   - Pedidos
   - Cozinha
   - Estoque
   - Fidelidade
   - Pagamentos
