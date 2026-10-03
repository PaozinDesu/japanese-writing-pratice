import type {
	Character,
	CharacterCategory,
	CharacterDatabaseFile,
	CharacterGroup,
	Jlpt,
} from "./characters.type";

/** Rótulo do grupo do caractere ("TIPO" no painel/página de detalhe) — vale pra kana e kanji. */
export const GROUP_LABEL: Record<CharacterGroup, string> = {
	basico: "Básico",
	dakuten: "Dakuten",
	handakuten: "Handakuten",
	pequeno: "Pequeno",
	combinacao: "Combinação",
	estrangeiro: "Uso estrangeiro",
	joyo: "Jōyō",
};

export interface CharacterDatabase {
	meta: CharacterDatabaseFile["meta"];
	characters: Character[];
	byId: Map<string, Character>;
}

let cache: Promise<CharacterDatabase> | null = null;

/** Busca uma vez e mantém em memória pelo tempo de vida da página — equivalente ao `kdb()`/`D._idx` do protótipo. */
export function loadCharacters(): Promise<CharacterDatabase> {
	cache ??= fetch("/data/kaku-caracteres.json")
		.then((res) => res.json() as Promise<CharacterDatabaseFile>)
		.then((data) => ({
			meta: data.meta,
			characters: data.characters,
			byId: new Map(data.characters.map((c) => [c.id, c])),
		}));
	return cache;
}

/** Um glifo representativo de cada categoria, pra ilustrar cards/legendas sem carregar um caractere real. */
export const SAMPLE_GLYPH: Record<CharacterCategory, string> = {
	hiragana: "あ",
	katakana: "ア",
	kanji: "字",
};

export const CATEGORY_OPTIONS: { id: CharacterCategory; label: string }[] = [
	{ id: "hiragana", label: "Hiragana" },
	{ id: "katakana", label: "Katakana" },
	{ id: "kanji", label: "Kanji" },
];

export const JLPT_OPTIONS: Jlpt[] = ["N5", "N4", "N3", "N2", "N1"];

export interface CharacterFilters {
	categories: CharacterCategory[];
	jlpt: Jlpt[];
}

/** Filtra por sistema de escrita (sem seleção = todos) e, só para kanji, por nível JLPT — hiragana e katakana nunca são afetados pelo nível. */
export function filterCharacters(db: CharacterDatabase, filters: CharacterFilters): Character[] {
	const { categories, jlpt } = filters;
	return db.characters.filter((c) => {
		if (categories.length && !categories.includes(c.category)) return false;
		if (c.category === "kanji" && jlpt.length) return jlpt.includes(c.jlpt as Jlpt);
		return true;
	});
}

export type PoolLabelSource =
	| { kind: "filters"; categories: CharacterCategory[]; jlpt: Jlpt[] }
	| { kind: "list"; listName: string };

/** Porte de `poolLabel` (practice.js). */
export function poolLabel(source: PoolLabelSource): string {
	if (source.kind === "list") return "Lista: " + source.listName;
	const catLabels = source.categories.map(
		(id) => CATEGORY_OPTIONS.find((o) => o.id === id)!.label,
	);
	const jlptSorted = [...source.jlpt].sort().reverse();
	if (!catLabels.length && !jlptSorted.length) return "Todos os caracteres";
	if (!catLabels.length) return "Todos · Kanji " + jlptSorted.join(" + ");
	return (
		catLabels.join(" + ") +
		(jlptSorted.length && source.categories.includes("kanji") ? " · " + jlptSorted.join(" + ") : "")
	);
}

export function readingText(e: Character): string {
	if (e.category !== "kanji") return e.char + " · " + e.romaji;
	const on = e.readings.on.map((o) => o.kana).join("、");
	const kun = e.readings.kun.map((k) => k.display).join("、");
	return [on, kun].filter(Boolean).join(" ／ ");
}

export function readingRomaji(e: Character): string {
	return e.category === "kanji" ? (e.readingsRomaji ?? []).join(", ") : e.romaji;
}
