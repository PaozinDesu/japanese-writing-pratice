---
paths:
  - "www/**"
---

# Regra: estrutura do frontend (`www/`) — padrão MVVM

Todo arquivo novo criado dentro de `www/` deve seguir esta estrutura em camadas (Model / View / ViewModel). Não criar pastas fora desta lista sem necessidade; se surgir uma categoria nova, perguntar antes de inventar uma pasta.

```
www/              
├── src/
│   ├── app/                # Next.js App Router — somente rotas (page.tsx, layout.tsx, loading.tsx, error.tsx)
│   ├── models/             # Tipos, entidades, DTOs e chamadas à API (fetch)
│   ├── view-models/        # Hooks `use{Name}ViewModel` — estado e lógica de apresentação
│   ├── views/              # Componentes de tela, presentational only (recebem tudo via props)
│   ├── components/         # Componentes de UI reutilizáveis (design system), sem lógica de negócio
│   └── utils/              # Funções utilitárias puras (formatadores, helpers)
├── public/
├── package.json
└── tsconfig.json
```

## Camadas

- **`app/`** — reservado ao roteamento do Next.js. Cada `page.tsx` é o *composition root*: chama o hook de `view-models/` e passa o resultado como props para o componente de `views/`. Não contém JSX de UI nem lógica própria além dessa ligação.
- **`models/`** (Model) — tipos/interfaces, entidades, DTOs (seguem a regra [[create-dto]], `*.dto.ts`) e as funções que chamam a API (`fetch`). É a única camada que sabe da API/dados externos. Não importa React.
- **`view-models/`** (ViewModel) — hooks React (`use{Name}ViewModel`) que orquestram `models/`, guardam estado (`useState`, `useEffect`, etc.) e expõem dados e handlers já prontos para a View. Não retorna JSX e não importa componentes de `views/`.
- **`views/`** (View) — componentes React "burros": recebem tudo via props (dados e callbacks), sem `useState`/`useEffect`/chamada de API própria. Só renderizam.
- **`components/`** — peças de UI reutilizáveis e genéricas (botão, input, modal, card), sem regra de negócio nem acesso a `models/`.
- **`utils/`** — funções puras auxiliares, sem estado e sem dependência de React.

## Fluxo de dependência

`app/page.tsx` → `view-models/` → `models/`
`app/page.tsx` → `views/` (props vindas do ViewModel) → `components/`

- View nunca importa `models/` ou faz fetch diretamente.
- ViewModel nunca importa `views/` nem retorna JSX.
- Model nunca importa React nem hooks.

## Convenções de nomenclatura

- Arquivos em kebab-case, sufixados pela camada: `kanji-list.view.tsx`, `kanji-list.view-model.ts`, `kanji.model.ts`, `kanji.dto.ts`.
- Export da View em PascalCase + `View`: `KanjiListView`.
- Export do hook de ViewModel em camelCase + `ViewModel`: `useKanjiListViewModel`.
- Uma responsabilidade por arquivo (uma View, um ViewModel, um Model).

## Proibido

- `useState`/`useEffect`/chamada de API dentro de `views/`.
- JSX dentro de `view-models/`.
- `fetch`/acesso a API fora de `models/`.
- Arquivo solto em `src/` fora das pastas acima, ou lógica de UI/estado dentro de `app/`.
