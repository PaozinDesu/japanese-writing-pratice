# Kaku — base de caracteres japoneses

Base de dados reutilizável de hiragana, katakana e kanji para a plataforma Kaku.

| Arquivo | Conteúdo |
|---|---|
| `kaku-caracteres.json` | Base completa (2.390 caracteres: 115 hiragana, 139 katakana, 2.136 kanji) |
| `hiragana.json` / `katakana.json` / `kanji.json` | A mesma base separada por categoria |
| `schema.json` | JSON Schema de cada registro |
| `kaku-data.js` | Bundle compacto para o site (`window.KAKU_DATA`, ~1,1 MB), expandido no navegador |
| `fonte/kanji.txt` | Fonte editável dos kanji (uma linha por kanji) |
| `fonte/componentes.txt` | Radical, decomposição gráfica e formação histórica de cada kanji |
| `fonte/kanji_extra_*.txt` | Kanji adicionados por nível (dados + radical + componentes numa linha) |
| `fonte/jlpt/` | Listas de nível JLPT usadas como referência (kanjikana.com) |
| `fonte/radicais_kangxi.txt`, `fonte/componentes_dicionario.txt` | Os 214 radicais e o significado dos componentes que não são kanji |
| `fonte/composition.py` | Tabela de radicais, dicionário de componentes e cálculo das relações |
| `fonte/build_data.py` | Gera todos os arquivos acima a partir da fonte e valida os dados |

## Conteúdo

- **Hiragana (115):** 46 básicos, 20 com dakuten + ゔ, 5 com handakuten, 10 pequenos, 33 combinações (yōon).
- **Katakana (139):** 46 básicos, 20 com dakuten + ヴ, 5 com handakuten, 12 pequenos (incluindo ヵ e ヶ), 33 combinações e 22 combinações modernas para palavras estrangeiras.
- **Kanji (2.136, todos os Jōyō):** níveis JLPT conforme a kanjikana.com — N5 80 · N4 170 · N3 370 · N2 380 · N1 1.136.
  - **Ficha completa (685):** todos os N5, N4 e N3, e alguns N2/N1, com 2–3 exemplos e uma frase traduzida.
  - **Ficha essencial (1.451, N2/N1):** significados PT/EN, on/kun com romaji, radical, traços, componentes e 1 exemplo; sem frase (`sentence: null`, `detail: "essencial"`).
  - Origem histórica registrada em 1.410 kanji; os demais mostram só a decomposição gráfica.

Cada caractere aparece **uma única vez** (`id` = `categoria:caractere`). Categoria, JLPT, nível e tipo são só atributos usados pelos filtros.

## Campos principais

| Campo | Kana | Kanji |
|---|---|---|
| `char`, `category`, `group` | ✓ | ✓ |
| `romaji`, `reading` | som / forma em hiragana | leitura principal |
| `meaning.pt`, `meaning.en` | ✓ | ✓ |
| `difficulty` (`iniciante`, `intermediario`, `avancado`) | ✓ | ✓ |
| `jlpt` | `null` | N5–N1 |
| `strokes` | ✓ | ✓ |
| `strokeOrder` | quando disponível | quando disponível |
| `examples[]` (palavra, leitura, romaji, pt, en) | quando aplicável | 2–3 por kanji |
| `readings.on`, `readings.kun`, `readingsRomaji` | — | ✓ |
| `grade`, `usage`, `sentence` (ja/pt/en) | — | ✓ |

### Componentes, radicais e formação (schemaVersion 2)

Cada kanji tem três camadas, propositalmente separadas:

| Campo | O que é | Exemplo (語) |
|---|---|---|
| `radical` | Radical principal (Kangxi): forma como aparece, forma padrão, número e significado | 言 · nº 149 · palavra |
| `decomposition` | **Decomposição gráfica**: só o que se vê | 言 + 五 + 口 |
| `formation` | **Origem / formação histórica**, só quando a classificação tradicional é consolidada; senão `null` | Fono-semântico: 言 (semântico) + 吾 (fonético, ゴ) |

Tipos de componente (`form`):
- `kanji`: caractere independente (clicável quando existe na base, via `ref`).
- `radical`: forma de radical (亻 = 人, 氵 = 水, 艹, 辶…). Quando a forma padrão está na base, também é clicável.
- `grafico`: elemento visual sem significado próprio neste uso. `lookalike: true` marca partes que **parecem** outro caractere mas têm outra origem, como 田 em 思 (era 囟, a cabeça) ou 月 em 青 (era 丹).

Na formação, cada parte tem `role`: `semantico` ou `fonetico` (com a leitura que indicava).

Relações calculadas automaticamente:
- `containsComponents`: todos os componentes, recursivamente. Por exemplo, 語 contém 口 porque 吾 = 五 + 口, e 休 contém 人 por causa de 亻.
- `usedIn`: kanji da base que usam este kanji (ou suas formas de radical) como componente. Por exemplo, 木 → 本 林 森 休 校 村 相 機…
- `related`: kanji que compartilham componentes e/ou radical.

**Critério para a origem:** só registramos a formação quando a classificação tradicional (象形 pictograma, 指事 indicativo, 会意 ideograma composto, 形声 fono-semântico, 国字 kokuji) é amplamente aceita. Quando há divergência conhecida, a nota diz isso. Por exemplo, 明: “sol + lua” é a leitura tradicional, mas as formas antigas mostram 囧; e 東 não é “sol atrás da árvore”. Mnemônicos modernos não entram como origem. Hoje 1.410 dos 2.136 kanji têm formação registrada. Nos kanji de N2/N1 ela quase sempre é fono-semântica (semântico + fonético); os outros mostram só a decomposição gráfica.

## Regras de classificação

- **Nível dos kanji:** N5/N4 → iniciante · N3 → intermediário · N2/N1 → avançado.
- **Nível dos kana:** básicos, dakuten e handakuten → iniciante · pequenos e combinações → intermediário · sons estrangeiros e formas raras (ゔ/ヴ, ヵ/ヶ, ゎ/ヮ, ぢ/づ, ヂ/ヅ) → avançado.
- **Romaji:** Hepburn em estilo digitação, com as vogais longas por extenso (kyou, koohii), seguindo o exemplo pedido. É gerado automaticamente a partir do kana, para não haver divergência.

## Limitações (importante)

1. **JLPT aproximado.** Desde 2010 o JLPT não publica listas oficiais de kanji. Os níveis seguem a classificação usual das listas de estudo e podem variar entre fontes.
2. **“Nível de uso” (`usage`) é derivado do JLPT**, não de contagem de frequência em jornais ou corpora. Para ter frequência real, basta preencher o campo com um ranking (por exemplo, o do KANJIDIC2) no script.
3. **Composição:** a decomposição segue a análise visual usual dos dicionários japoneses e a formação segue a classificação tradicional. As duas foram escritas manualmente, sem um banco etimológico automatizado; vale uma revisão especializada.
4. **Ordem dos traços:** só 30 caracteres têm traçado (`source: "kaku-simplificado"`). São desenhos simplificados feitos à mão para o protótipo. Nos demais o campo é `null`, a contagem de traços é mostrada e a interface indica que a animação ainda não está disponível.
5. Leituras, exemplos e frases foram escritos e revisados manualmente, sem conferência automática com um dicionário. Vale uma revisão por um falante nativo ou professor antes de publicar.

## Como chegar aos 2.136 Jōyō Kanji

A estrutura já comporta a lista completa. O caminho recomendado:

1. **Dados básicos (automático):** importar o [KANJIDIC2](https://www.edrdg.org/wiki/index.php/KANJIDIC_Project) (licença CC BY-SA 4.0) para preencher leituras on/kun, significados em inglês, série escolar, número de traços e ranking de frequência de todos os Jōyō.
2. **Ordem dos traços (automático):** importar os SVGs do [KanjiVG](https://kanjivg.tagaini.net/) (CC BY-SA 3.0). Cada `<path>` vira um item de `strokeOrder.paths` (`viewBox` `0 0 109 109`, `source: "kanjivg"`). O KanjiVG também cobre hiragana e katakana.
3. **Conteúdo em português (manual ou assistido):** significados em PT, exemplos traduzidos e frases. Adicione linhas ao `kanji.txt` no mesmo formato e rode:

```bash
python3 build_data.py
```

O script falha se houver kanji duplicado, exemplo ou frase que não contenha o kanji, ou algum kanji da lista pedida faltando.

**Formato de uma linha do `kanji.txt`:**

```
日|dia; sol|day; sun|ニチ,ジツ|ひ,び,か|N5|1|4|日本:にほん:Japão:Japan¦今日:きょう:hoje:today|今日はいい天気ですね。|Hoje o tempo está bom, né?|The weather is nice today, isn't it?
```

Campos: kanji | significado PT | significado EN | on'yomi | kun'yomi (okurigana depois de `.`) | JLPT | série | traços | exemplos (`palavra:leitura:pt:en`, separados por `¦`) | frase | tradução PT | tradução EN.

Para a lista completa, vale dividir os dados em arquivos por nível (`kanji-n5.json` …) e carregá-los sob demanda, para não baixar ~1,5 MB de uma vez.

## Referência de níveis

As listas de N5 a N1 vêm de https://kanjikana.com/pt/kanji/jlpt/n5 (e páginas N4–N1). Uma página do N1 (16/24) não pôde ser lida por limite de acesso do site. Os 48 kanji dela foram reconstruídos como “todos os Jōyō menos os já listados”; a contagem bate exatamente com o total do site (1.136). Vale conferir essa página quando possível.
