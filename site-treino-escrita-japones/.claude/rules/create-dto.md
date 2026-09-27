---
paths:
  - "**/*.dto.ts"
---

# Regra: criação de DTOs

Toda DTO do projeto deve seguir este padrão.

## Arquivo

- O nome do arquivo sempre termina em `.dto.ts`, em kebab-case: `{action}-{scope}.dto.ts` (ex.: `list-pokemon.dto.ts`).
- Uma DTO por arquivo.

## Nomenclatura

- A classe se chama `{Action}{Scope}DTO`, em PascalCase.
  - `{Action}`: o que a DTO representa (`Create`, `Update`, `Delete`, `Get`, `List`...).
  - `{Scope}`: a entidade ou contexto afetado (`Kanji`, `Stroke`, `Pokemon`...).
  - Exemplos: `CreateKanjiDTO`, `UpdatePracticeDTO`, `ListPokemonDTO`.
- Sufixo sempre `DTO` (maiúsculo), nunca `Dto`.
- A interface de params se chama `I{Action}{Scope}DTOParams` (prefixo `I`), ex.: `IListPokemonDTOParams`.

## Estrutura

1. Uma ou mais interfaces tipando os params da DTO, declaradas acima da classe e exportadas.
   - Se houver objetos aninhados, crie interfaces extras (prefixo `I`) em vez de tipos inline.
2. A classe `{Action}{Scope}DTO`, exportada, **sem construtor**.
3. Um método `static create(params: I{Action}{Scope}DTOParams): {Action}{Scope}DTO` que instancia com `new {Action}{Scope}DTO()`, atribui cada campo a partir de `params` e retorna a instância.
   - Validações e normalizações de entrada ficam dentro do `create`.

## Tipagem das propriedades

Como as propriedades são atribuídas no `create` (e não num construtor), a classe precisa ser tipada assim para compilar em `strict`:

- **Não usar `readonly`**: atribuir a propriedade `readonly` fora do construtor é erro de tipagem.
- **Parâmetro obrigatório**: na interface `campo: Tipo`; na classe `campo!: Tipo` (o `!` evita o erro de propriedade não inicializada, já que o `create` sempre a preenche).
- **Parâmetro condicional (opcional)**: na interface `campo?: Tipo`; na classe `campo?: Tipo`. No `create`, atribuir normalmente (`dto.campo = params.campo`).
- A obrigatoriedade na classe deve sempre espelhar a da interface.

## Exemplo

```ts
// create-kanji.dto.ts

export interface IKanjiStrokeParams {
  order: number;
  path: string;
}

export interface ICreateKanjiDTOParams {
  character: string;
  meaning: string;
  strokes: IKanjiStrokeParams[];
  notes?: string;
}

export class CreateKanjiDTO {
  character!: string;
  meaning!: string;
  strokes!: IKanjiStrokeParams[];
  notes?: string;

  static create(params: ICreateKanjiDTOParams): CreateKanjiDTO {
    const dto = new CreateKanjiDTO();
    dto.character = params.character;
    dto.meaning = params.meaning;
    dto.strokes = params.strokes;
    dto.notes = params.notes;
    return dto;
  }
}
```

## Proibido

- Declarar construtor na DTO; a criação é sempre por `{Action}{Scope}DTO.create(...)`.
- Usar `readonly` nas propriedades.
- Tipar os params inline ou com `any`; use sempre interfaces.
- Criar DTOs em arquivos que não terminem em `.dto.ts`.
