# Kaku Design System · Tailwind CSS

Um único conjunto de decisões visuais para todas as telas do Kaku. Tudo usa a paleta e as escalas **padrão do Tailwind CSS v3.4**: não há hex arbitrário nem valores como `mt-[13px]`.

| Arquivo | Para quê |
|---|---|
| `tailwind.config.js` | Aliases semânticos (`primary`, `surface`, `text-primary`…) apontando para a paleta padrão do Tailwind |
| `components.ts` | Variantes de todos os componentes com **class-variance-authority (CVA)** |
| `tokens.json` | Os mesmos tokens em JSON (cores, espaçamento, tipografia, raios, sombras, breakpoints) |
| `python/ds.py` · `python/ui.py` | A mesma fonte usada para gerar o protótipo (canvas) |

## 1. Cores — regra 60/30/10

| Papel | Uso | Tailwind |
|---|---|---|
| **60% dominante** | fundo das páginas, áreas grandes | `background` = stone-100 · `background-subtle` = stone-50 |
| **30% secundária** | cards, menus, header, navegação, bordas, texto, ações secundárias | `surface` = white · `border` = stone-200/300 · `secondary` = stone-900 |
| **10% destaque** | CTAs, links, estados ativos, indicadores | `primary`/`accent` = red-600 |

| Token | Padrão | hover | active | subtle | muted/focus | disabled |
|---|---|---|---|---|---|---|
| primary | red-600 | red-700 | red-800 | red-50 | red-100 | red-300 |
| secondary | stone-900 | stone-800 | stone-700 | stone-100 | — | stone-300 |
| accent | red-600 | — | — | red-50 | red-100 | borda red-200 |
| text | primary stone-900 · secondary stone-700 · muted stone-600 · placeholder stone-500 · disabled stone-400 |
| status | success green-700/100 · warning amber-800/100 · error red-700/100 · info blue-800/100 (cada um com `subtle` 50, `border` 200 e `solid` 600) |

Texto secundário e legendas ficam em stone-700/stone-600 para manter o contraste AA também sobre stone-100. Status sempre vem com ícone e rótulo, nunca só cor.

## 2. Espaçamento

Escala do Tailwind com uma hierarquia fixa:

- elementos relacionados (ícone + texto, rótulo → campo): `gap-2`
- itens de um grupo (chips, botões lado a lado): `gap-2`/`gap-3`
- componentes dentro de um card: `gap-4`
- padding de card: `p-6` (compacto `p-4`/`p-5`)
- entre cards/colunas: `gap-6`
- entre seções: `gap-8` → `gap-12`
- página: `max-w-7xl mx-auto px-5 sm:px-6 lg:px-12 xl:px-20 pt-10 pb-12`
- formulários: `gap-4` entre campos
- título → texto: `gap-2`; texto → conteúdo: `gap-4`/`gap-6`

## 3. Tipografia

| Papel | Classes |
|---|---|
| Display | `font-serif text-6xl leading-none font-bold` |
| H1 | `font-serif text-5xl leading-none font-bold` |
| H2 | `font-serif text-3xl leading-9 font-bold` |
| H3 | `text-xl leading-7 font-bold` |
| H4 | `text-lg leading-7 font-bold` |
| Body | `text-base leading-6 text-text-secondary` |
| Body Small | `text-sm leading-5 text-text-secondary` |
| Label | `text-sm leading-5 font-bold` |
| Caption | `text-xs leading-4 text-text-muted` |
| Overline | `text-xs font-bold uppercase tracking-widest text-text-muted` |

Fontes: `font-serif` Shippori Mincho · `font-sans` Zen Kaku Gothic New · `font-jp` Klee One (só para os caracteres japoneses em destaque, que podem usar a escala completa `text-2xl`…`text-8xl`).

## 4. Componentes e estados

`components.ts` define: `button` (primary, secondary, outline, ghost, danger, link × sm/md/lg/icon, com loading), `input`/`select`/`textarea` (estado de erro), `checkbox`, `radio`, `switchTrack`, `card` (padding, interativo, selecionado), `modal`, `overlay`, `dropdown`, `menuItem`, `tooltip`, `badge` (tons + sistemas de escrita), `alert`, `skeleton`, `emptyState`, `tabs`/`tab`, `chip`, `navbar`/`navLink`, `bottomNav`, `sidebar`, `breadcrumb`, `table`/`th`/`td`, `paginationItem` e `progress`.

Estados comuns a todos:
- **hover**: um tom acima (primary 600→700; outline → stone-50)
- **focus**: `outline-2 outline-offset-2 outline-primary`; campos com `ring-4 ring-primary-muted`
- **active**: dois tons acima e `scale-95`
- **disabled**: `opacity-50 cursor-not-allowed`
- **loading**: spinner `animate-spin` + rótulo no gerúndio ("Salvando…")
- **erro**: borda `primary`, fundo `error-subtle` e mensagem com ícone

```tsx
import { button, input, card } from './design-system/components';
<button className={button({ variant: 'primary', size: 'lg' })}>Começar</button>
<input className={input({ state: hasError ? 'error' : 'default' })} aria-invalid={hasError} />
<div className={card({ interactive: true })}>…</div>
```

## 5. Bordas, raios e sombras

- `rounded-md`: badges, chips pequenos, tooltips, checkboxes
- `rounded-lg`: botões, inputs, selects, tiles, itens de menu
- `rounded-xl`: cards, painéis, modais
- `rounded-full`: pílulas de filtro, abas segmentadas, avatares, barras de progresso
- Bordas `border` (1px) stone-200, campos stone-300, seleção `border-2 border-primary`. Divisores stone-200.
- Sombras: `shadow-sm` segmento ativo · `shadow-md` hover/tooltip · `shadow-lg` dropdown · `shadow-xl` modal.

## 6. Layout e breakpoints

Breakpoints padrão: `sm` 640 · `md` 768 · `lg` 1024 · `xl` 1280 · `2xl` 1536. A navegação superior aparece a partir de `md`; abaixo disso, a barra inferior. Grids: cards `sm:grid-cols-2 lg:grid-cols-3`; caracteres `grid-cols-2 sm:grid-cols-4 lg:grid-cols-5`; prática `lg:grid-cols-12` (3 / 5 / 4 colunas).

## Protótipo (canvas)

O canvas não carrega o Tailwind (os quadros só aceitam estilos inline). Por isso, `ds.normalize()` converte cada tela para os valores exatos das classes Tailwind: cores da paleta, espaçamentos, tamanhos de fonte, alturas de controles, raios e sombras. Os estados (hover, foco, desabilitado, tooltip, spinner) ficam centralizados no `<helmet>` de `common.py`. Os quadros mostram os breakpoints `xl` (1440px) e celular (390px).
