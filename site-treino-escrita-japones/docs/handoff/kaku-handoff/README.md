# Kaku — handoff de design

Pacote de handoff do protótipo **Kaku**, uma plataforma para aprender a escrever e ler japonês (hiragana, katakana e os 2.136 kanji Jōyō). O objetivo é servir de referência para implementar o produto de verdade com o **Claude Code**.

O protótipo veio de um canvas de design com 24 pranchetas:

- 10 telas desktop em 1920×1080;
- 12 telas de celular em 390×844;
- 2 pranchetas do Design System.

Todas as telas funcionam: login, listas, prática de escrita com reconhecimento do traço, prática de leitura, progresso com filtros de período e persistência por usuário.

```
kaku-handoff/
├── README.md            ← este arquivo
├── CLAUDE.md            ← instruções curtas para o Claude Code
├── design-system/       ← tokens, config do Tailwind e componentes (CVA)
├── screenshots/         ← PNG de cada tela e dos estados principais
├── screens-static/      ← HTML estático de cada tela (renderizado, sem JS)
└── source/              ← fonte do protótipo: pranchetas, lógica JS, dados e geradores
```

---

## 1. `design-system/`

É a fonte da verdade visual. Tudo usa a paleta e as escalas padrão do **Tailwind CSS v3.4**. Não há hex arbitrário nem valores como `mt-[13px]`.

| Arquivo | Uso |
|---|---|
| `tailwind.config.js` | Aliases semânticos (`primary`, `secondary`, `accent`, `background`, `surface`, `border`, `text-*`, status), fontes, raios, sombras e breakpoints. Copie ou faça merge no `tailwind.config.js` do app. |
| `components.ts` | Variantes de todos os componentes com **class-variance-authority**: button, input, select, textarea, checkbox, radio, switch, chip, card, modal, dropdown, tooltip, badge, alert, tabs, navbar, bottomNav, table, progress, skeleton etc. Use com `cn()` (clsx + tailwind-merge). |
| `tokens.json` | Os mesmos tokens em JSON, para outras plataformas ou para gerar CSS variables. |
| `LEIAME.md` | Documentação completa: regra 60/30/10, hierarquia de espaçamento, papéis tipográficos, estados e acessibilidade. |
| `python/ds.py`, `python/ui.py` | Implementação usada para gerar o protótipo. `ds.normalize()` encaixa qualquer valor nas escalas do Tailwind. |

Resumo das decisões:

- **Cores (60/30/10).**
  - Fundo `stone-100`.
  - Superfícies brancas com bordas `stone-200/300`.
  - Texto `stone-900/700/600`.
  - Destaque `red-600`: CTAs, links e estados ativos.
  - Status em green, amber, red e blue, sempre com ícone e rótulo.
- **Tipografia.**
  - `Zen Kaku Gothic New`: interface.
  - `Shippori Mincho`: títulos de exibição.
  - `Klee One`: caracteres japoneses de modelo e a caligrafia do reconhecimento.
- **Controles.**
  - Altura 44px (`h-11`) e raio `rounded-lg`.
  - Cards com `rounded-xl`, `border` e `shadow-sm`.
  - Foco com `ring-2 ring-red-600/40`.
- **Breakpoints.** Padrão do Tailwind. A navegação vira barra inferior abaixo de `md`.

Referência visual: `screenshots/design-system/DesignSystem.png` e `Componentes.png`.

## 2. `screenshots/`

PNGs capturados do protótipo em execução, com Playwright e Chromium.

| Pasta | Conteúdo |
|---|---|
| `desktop/visitante/` | As 10 telas desktop sem login (1920×1080) |
| `desktop/logado/` | As telas com usuário logado ("Ana Souza"), histórico de exemplo de 4 meses e a lista "Kanji N5 — Semana 1" |
| `mobile/visitante/`, `mobile/logado/` | As 12 telas de celular (390×844) nos mesmos dois cenários |
| `estados/` | Estados que só aparecem com interação (tabela abaixo) |
| `design-system/` | As duas pranchetas do DS em altura total |

Estados capturados em `estados/`:

- **Escrita:** sessão, feedback do reconhecimento e resumo.
- **Leitura:** pergunta, feedback de erro e resultado com a lista de erros.
- **Conta:** menu do usuário, e validações de login e de cadastro.
- **Celular:** sessões de escrita e leitura, detalhe do kanji e detalhe de lista.

## 3. `screens-static/`

Mesma estrutura de pastas de `screenshots/`, com um `.html` por tela: o DOM já renderizado, com os estilos inline preservados e **sem nenhum script**. O `<canvas>` de desenho vira um placeholder do mesmo tamanho.

Abra direto no navegador. As fontes vêm do Google Fonts. Os arquivos servem para:

- inspecionar a estrutura exata (hierarquia, textos, `aria-*`, espaçamentos em px);
- dar ao Claude Code um alvo concreto. Por exemplo: "implemente `screens-static/desktop/logado/Progresso.html` como componente React com as classes do design system".

> Nas telas desktop, o layout é desenhado em 1440×810 e escalado ×1,333 para caber em 1920×1080 (`transform: scale(...)` no wrapper). Na implementação real, use o layout de 1440 de largura útil (`max-w-7xl`) sem esse transform.

## 4. `source/`

Tudo que gera o protótipo.

```
source/
├── project/               ← as 24 pranchetas (.dc.html) + canvas.json + data/kaku-data.js
├── js/                    ← lógica de negócio compartilhada (injetada nas pranchetas)
│   ├── account.js         ← contas, sessão, listas, histórico, estatísticas, períodos
│   ├── rec.js             ← reconhecimento do traço + validação de leitura/significado
│   ├── practice.js        ← prática de escrita (seleção → sessão → resumo)
│   └── reading.js         ← prática de leitura (seleção → quiz → resultado)
├── data/                  ← pipeline da base de caracteres
│   ├── build_data.py, composition.py, *.txt, jlpt/
│   └── out/               ← JSONs gerados, schema.json, LEIAME.md, kaku-data.js
├── common.py, ds.py, ui.py, b_*.py   ← geradores das pranchetas
├── resultado_src.html
└── tools/cap.js, lib.js   ← script Playwright que gerou screenshots/ e screens-static/
```

### 4.1 Mapa das telas

| Prancheta | Celular | O que faz |
|---|---|---|
| `Main` – Início | `MainMobile` | Hero, caractere do dia, "Continue de onde parou" |
| `Caracteres` | `CaracteresMobile`, `DetalheMobile` | Tabela de kana/kanji com filtros e ficha de detalhe; "Adicionar à lista" e "Praticar" |
| `Kanji` – componentes | `KanjiMobile` | Ficha do kanji: leituras, radical, decomposição, origem, exemplos |
| `Praticar` – Escrita | `PraticarMobile`, `ResultadoMobile` | Seleção (sistemas, JLPT, lista, quantidade, "priorizar o que mais errei", modo), sessão com desenho e resumo |
| `Leitura` | `LeituraMobile` | Seleção no mesmo modelo da Escrita, quiz de leitura e resultado |
| `Progresso` | `ProgressoMobile` | KPIs, evolução, caracteres estudados, mais praticados, mais erros, histórico; filtros Hoje / Esta semana / Este mês / Todo o período |
| `Login`, `Cadastro` | `LoginMobile`, `CadastroMobile` | Autenticação com validações |
| `Listas` | `ListasMobile` | CRUD de listas de prática (criar, renomear, excluir, adicionar e remover caracteres, praticar) |
| `Perfil` | `PerfilMobile` | Dados da conta, histórico, dados de exemplo, sair |
| `DesignSystem`, `Componentes` | — | Documentação viva do DS |

### 4.2 Regras de negócio (onde estão)

- **Base de caracteres.**
  - `window.KAKU_DATA` (`project/data/kaku-data.js`) é um bundle compacto que é expandido no navegador.
  - Cada caractere tem `id = categoria:caractere`.
  - Categoria, JLPT, grupo, nível e dificuldade são atributos usados pelos filtros.
  - Schema em `data/out/schema.json` e documentação em `data/out/LEIAME.md`.
  - Para o app real, use `data/out/kaku-caracteres.json` ou os JSONs por categoria.
- **Conta** (`account.js` → `Auth`).
  - Cadastro valida nome, email, idade, senha (mínimo de 6 caracteres) e confirmação, e rejeita email duplicado.
  - A senha é guardada com hash PBKDF2.
  - Sessão ativa em `localStorage`.
  - Páginas protegidas redirecionam para o Login e voltam depois (`returnTo`).
- **Persistência.**
  - Chaves `kaku.v1.users`, `kaku.v1.session` e `kaku.v1.user.<id>`.
  - Por usuário: `{ lists, sessions (escrita), readSessions (leitura) }`.
  - Outras chaves: `intent` (ex.: "praticar este caractere") e `lastEmail`.
- **Seleção da prática.**
  - `pickChars` monta a fila.
  - Com "priorizar o que mais errei", `charWeight` dá mais peso aos caracteres com mais erros e menos acertos recentes.
  - A leitura usa `readingOrder`: ordem aleatória, sem repetição consecutiva e com categorias misturadas.
- **Reconhecimento da escrita** (`rec.js` → `Rec`).
  - Compara os traços do usuário com máscaras do glifo em Klee One.
  - Normaliza a caixa (`fit`) e calcula uma pontuação por distância chamfer contra o alvo e uma lista de candidatos.
  - Limiares: `OK = 0.6` para acerto e `ID_MIN = 0.33` para identificar outro caractere.
  - O usuário pode corrigir manualmente (Contar como Acerto / Erro).
- **Validação da leitura** (`rec.js` → `readingOk`).
  - Aceita romaji ou kana.
  - Ignora maiúsculas e espaços.
  - Para kanji, aceita qualquer leitura on ou kun cadastrada; `canonRo` normaliza vogais longas e partículas.
- **Estatísticas** (`computeStats`).
  - Períodos (`PERIODS`): hoje, semana a partir de segunda, mês e tudo.
  - Com o período, calcula acertos, erros, taxa, tempo, sessões, sequência de dias (`streakOf`), mais erros e mais praticados.

### 4.3 Como abrir o protótipo localmente

As pranchetas carregam `./support.js`, o runtime do formato de canvas (React e o motor de template `x-dc`). Esse runtime é **do ambiente de design e não faz parte deste pacote**. Para ver as telas funcionando, use o artefato publicado no claude.ai ou os `screens-static/`.

Se você tiver o runtime, sirva a pasta e abra as páginas:

```bash
cd source/project && cp /caminho/do/support.js . && python3 -m http.server 8765
# http://127.0.0.1:8765/Main.dc.html
```

### 4.4 Regerar as pranchetas e os dados

```bash
cd source
for b in b_pages b_chars b_kanji b_mobile b_practice b_auth b_lists b_progress b_resultado b_ds b_reading b_mobile2; do python3 $b.py; done
cd data && python3 build_data.py && cp out/kaku-data.js ../project/data/   # só se mudar a base
```

Os geradores escrevem em `project/`. A lógica em `js/*.js` é embutida nas pranchetas na hora de gerar, então edite `js/` e rode os geradores de novo. Rodar os geradores sobre este pacote reproduz exatamente os arquivos de `project/`; isso foi verificado.

---

## 5. Usando com o Claude Code

1. Coloque esta pasta dentro do repositório do app, por exemplo em `docs/design-handoff/`. O `CLAUDE.md` daqui pode ser mesclado ao do projeto.
2. Peça por etapas. Exemplos:
   - "Configure Tailwind + CVA com `design-system/tailwind.config.js` e `design-system/components.ts`. Crie os componentes base em `src/components/ui`."
   - "Implemente a tela Progresso seguindo `screenshots/desktop/logado/Progresso.png` e a estrutura de `screens-static/desktop/logado/Progresso.html`. A regra de cálculo está em `source/js/account.js` (`computeStats`, `PERIODS`)."
   - "Porte `source/js/rec.js` para TypeScript como módulo puro, com testes para `readingOk` e `canonRo`."
   - "Importe `source/data/out/kaku-caracteres.json` para o banco usando `schema.json`."
3. Como fonte de verdade:
   - **Visual:** `design-system/` + `screenshots/`.
   - **Estrutura e textos:** `screens-static/`.
   - **Comportamento:** `source/js/`.
   - **Dados:** `source/data/out/`.

Stack sugerida: React ou Next.js, Tailwind 3.4, class-variance-authority, tailwind-merge, ícones de linha (lucide-react substitui bem os SVGs inline do protótipo) e Google Fonts (Zen Kaku Gothic New, Shippori Mincho, Klee One). Os textos da interface estão em pt-BR.

## 6. Limitações conhecidas

- **A autenticação é só um protótipo.** Contas e dados ficam em `localStorage` no navegador. No produto real, troque por backend e sessão de verdade; hash e validação precisam ir para o servidor.
- **O reconhecimento é aproximado.** Ele compara a forma, não a ordem nem a direção dos traços, e foi calibrado com poucos exemplos. Por isso a correção manual existe.
- **A base de caracteres foi montada manualmente.** Significados, exemplos e origem histórica precisam de revisão por alguém fluente antes de produção. 1.451 kanji N2/N1 têm só a ficha essencial.
- **A escala das telas desktop é artificial.** O ×1,333 serve só para caber nas pranchetas de 1920×1080 (veja a seção 3).
- **Os traços do modelo são simplificados.** Há caminhos de traço vetoriais para apenas cerca de 30 caracteres (`load_paths` em `common.py`). Os demais usam o glifo da fonte Klee One.
