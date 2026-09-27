---
paths:
  - "server/**"
---

# Regra: estrutura do backend (`server/`)

Todo arquivo novo criado dentro de `server/` deve ser colocado na pasta correta desta estrutura. Não criar pastas fora desta lista sem necessidade; se surgir uma categoria nova, perguntar antes de inventar uma pasta.

```
server/
├── src/
│   ├── config/          # Configurações gerais (banco de dados, variáveis de ambiente)
│   ├── controllers/     # Controladores (recebem as requisições e enviam as respostas)
│   ├── models/          # Modelos de dados / Schemas (Mongoose, Prisma, TypeORM)
│   ├── repositories/    # Comunicação direta com o banco de dados (queries)
│   ├── routes/          # Definição das rotas da API
│   ├── services/        # Regras de negócio da aplicação
│   ├── middlewares/     # Interceptadores (autenticação, tratamento de erros)
│   ├── utils/           # Funções utilitárias e ajudantes (formatadores, enums)
│   └── server.ts        # Arquivo principal que inicia o servidor
├── .env                 # Variáveis de ambiente
├── package.json         # Dependências do projeto
└── tsconfig.json        # Configuração do TypeScript
```

## Onde colocar cada arquivo

- **`config/`** — inicialização de banco de dados, leitura/validação de env vars, configuração de libs de terceiros.
- **`controllers/`** — recebem `Request`/`Response`, chamam `services/` e formatam a resposta. Não contêm regra de negócio nem query direta ao banco.
- **`models/`** — schemas/entidades do ORM (Mongoose, Prisma, TypeORM).
- **`repositories/`** — única camada que fala com o banco de dados (queries, `find`, `save`, etc.). Services chamam repositories, nunca o contrário.
- **`routes/`** — só define `router.get/post/...` e liga rota a controller; sem lógica.
- **`services/`** — regra de negócio da aplicação; orquestra repositories, valida regras, lança erros de domínio.
- **`middlewares/`** — autenticação, autorização, tratamento de erros, logging, validação de request.
- **`utils/`** — funções puras auxiliares, formatadores, enums e constantes sem estado.
- **DTOs** seguem a regra [[create-dto]] (`*.dto.ts`); ficam junto do módulo que as usa (ex.: dentro de `controllers/` ou em uma subpasta `dtos/` do domínio), não soltas na raiz de `src/`.
- **`server.ts`** — único arquivo que instancia e sobe o servidor (`app.listen`). Não conter rotas, controllers ou regra de negócio.

## Convenções de nomenclatura

- Arquivos em kebab-case, sufixados pela camada: `user.controller.ts`, `user.service.ts`, `user.repository.ts`, `user.routes.ts`, `user.model.ts`, `auth.middleware.ts`.
- Uma responsabilidade por arquivo (um controller, um service, etc.).

## Proibido

- Controller acessando o banco de dados diretamente — sempre via `services/` → `repositories/`.
- Regra de negócio dentro de `routes/` ou `controllers/`.
- Criar arquivo solto em `src/` fora das pastas acima.
- Mais de um arquivo de bootstrap do servidor (apenas `server.ts`).
