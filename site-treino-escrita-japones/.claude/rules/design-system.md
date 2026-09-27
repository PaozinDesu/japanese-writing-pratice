---
paths:
  - "www/**"
---

# Regra: design system do frontend (`www/`)

Siga estas regras em todos os componentes, páginas e estilos criados ou modificados em `www/`. Se alguma regra não puder ser cumprida, explique o motivo antes de prosseguir.

## 1. Cores — regra 60/30/10

- **60% — cor dominante (base):** fundos principais, grandes áreas e superfícies. Token: `bg-background` (`--background`).
- **30% — cor secundária:** cards, seções, sidebars, headers e elementos de apoio. Token: `bg-muted` / `text-muted-foreground` (`--muted`, `--muted-foreground`).
- **10% — cor de destaque (accent):** apenas CTAs, links, estados ativos, badges e elementos que precisam chamar atenção. Token: `bg-primary` / `text-primary` (`--primary`, `--primary-foreground`).
- Os tokens são definidos como variáveis CSS em [`src/app/globals.css`](../../www/src/app/globals.css) (`:root`, bloco `@theme inline` e o `@media (prefers-color-scheme: dark)`) — este projeto usa Tailwind v4 via CSS, não há `tailwind.config`. Use sempre as classes derivadas desses tokens (`bg-background`, `bg-muted`, `bg-primary`, `text-primary`, etc.), nunca hex solto (`bg-[#2563eb]`) nem `style={{ color: "..." }}`.
- Precisa de uma cor nova? Adicione o token em `globals.css` (claro e escuro) antes de usar — não invente classe/hex ad-hoc no componente.
- Não use a cor de destaque (`primary`) em áreas grandes (fundo de página, fundo de card inteiro) nem em elementos puramente decorativos.

## 2. Espaçamentos, raio e tipografia

- Use exclusivamente a escala padrão do Tailwind (`p-*`, `m-*`, `gap-*`, `space-*`, `w-*`, `h-*`, `rounded-*`, `text-*`, `border-*`), múltiplos de 4px (`p-2` = 8px, `p-4` = 16px, `gap-6` = 24px).
- **Proibido** valor arbitrário entre colchetes (`p-[13px]`, `mt-[5px]`, `gap-[7px]`, `rounded-[10px]`, `text-[15px]`) e estilo inline com pixel quebrado.
- Ritmo consistente: espaçamento interno de componente entre `2` e `6`; espaçamento entre seções entre `8` e `16`.

## 3. Ícones

- Use **somente** `lucide-react` (`import { IconName } from "lucide-react"`).
- Proibido SVG inline, emoji como ícone, ou outra biblioteca de ícones (Heroicons, FontAwesome, Material Icons, etc.).
- Tamanho sempre via classe Tailwind: `size-4`, `size-5` ou `size-6`. Não passar `size={16}` nem estilo inline para dimensionar.
- `strokeWidth` consistente em todo o projeto (usar o padrão do componente `Icon` do Lucide, não sobrescrever por ícone sem motivo).
- Ícone sem texto ao lado precisa de `aria-label` (ou `<span className="sr-only">`) descrevendo a ação.

## Checklist antes de finalizar

- [ ] Distribuição de cores respeita 60/30/10 e usa os tokens de `globals.css`, sem hex solto.
- [ ] Nenhum valor arbitrário (`[...]`) de espaçamento, tamanho, raio ou fonte.
- [ ] Todo ícone vem de `lucide-react`, dimensionado com `size-*` e acessível quando não tem texto de apoio.
