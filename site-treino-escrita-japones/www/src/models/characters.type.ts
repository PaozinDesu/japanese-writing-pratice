// Tipos espelhando docs/handoff/kaku-handoff/source/data/out/schema.json (schemaVersion 2).

export type CharacterCategory = "hiragana" | "katakana" | "kanji";

export type CharacterGroup =
	| "basico"
	| "dakuten"
	| "handakuten"
	| "pequeno"
	| "combinacao"
	| "estrangeiro"
	| "joyo";

export type Jlpt = "N5" | "N4" | "N3" | "N2" | "N1";

export type Difficulty = "iniciante" | "intermediario" | "avancado";

export interface CharacterExample {
	word: string;
	reading: string;
	romaji: string;
	pt: string;
	en: string;
}

export interface StrokeOrder {
	source: string;
	viewBox: string;
	paths: string[];
	note?: string;
}

export interface KanjiOnReading {
	kana: string;
	romaji: string;
}

export interface KanjiKunReading {
	kana: string;
	display: string;
	okurigana?: string | null;
	romaji: string;
}

export interface KanjiReadings {
	on: KanjiOnReading[];
	kun: KanjiKunReading[];
}

export interface KanjiUsage {
	level?: number;
	label?: string;
}

export interface KanjiSentence {
	ja: string;
	pt: string;
	en: string;
}

export interface KanjiRadical {
	char: string;
	standard: string;
	number: number;
	meaning: Record<string, string>;
	name?: string | null;
	ref?: string | null;
}

export type ComponentForm = "kanji" | "radical" | "grafico";

export interface CharacterComponent {
	c: string;
	form: ComponentForm;
	meaning: string;
	ref: string | null;
	lookalike?: boolean;
	standard?: string;
}

export type FormationType =
	| "pictograma"
	| "indicativo"
	| "ideograma-composto"
	| "fono-semantico"
	| "kokuji";

export interface FormationPart {
	c: string;
	role: "semantico" | "fonetico";
	reading?: string;
	meaning?: string;
	form?: string;
	ref?: string | null;
}

export interface KanjiFormation {
	type: FormationType;
	label: string;
	description: string;
	note?: string | null;
	parts?: FormationPart[];
}

export type CharacterDetail = "completo" | "essencial";

/** Um caractere kana (hiragana/katakana): os campos exclusivos de kanji não existem. */
export interface KanaCharacter {
	id: string;
	char: string;
	category: "hiragana" | "katakana";
	group: CharacterGroup;
	romaji: string;
	reading: string;
	meaning: { pt: string[]; en: string[] };
	jlpt: null;
	difficulty: Difficulty;
	strokes: number;
	strokeOrder: StrokeOrder | null;
	examples: CharacterExample[];
	components?: string[];
	note?: string;
}

/** Um kanji: todos os campos abaixo são obrigatórios pelo schema quando category === "kanji". */
export interface KanjiCharacter {
	id: string;
	char: string;
	category: "kanji";
	group: CharacterGroup;
	romaji: string;
	reading: string;
	meaning: { pt: string[]; en: string[] };
	jlpt: Jlpt | null;
	difficulty: Difficulty;
	strokes: number;
	strokeOrder: StrokeOrder | null;
	examples: CharacterExample[];
	note?: string;
	readings: KanjiReadings;
	readingsRomaji: string[];
	grade: number;
	gradeLabel?: string;
	usage: KanjiUsage;
	sentence: KanjiSentence | null;
	radical: KanjiRadical;
	decomposition: CharacterComponent[];
	formation: KanjiFormation | null;
	containsComponents: string[];
	usedIn: string[];
	related: string[];
	detail: CharacterDetail;
}

export type Character = KanaCharacter | KanjiCharacter;

export function isKanji(character: Character): character is KanjiCharacter {
	return character.category === "kanji";
}

export interface CharacterDatabaseFile {
	meta: {
		schemaVersion: 2;
		generatedAt?: string;
		romanization?: string;
		groups?: Record<string, string>;
		difficulty?: Record<string, string>;
		jlpt?: Jlpt[];
		counts: Record<string, number>;
		caveats?: string[];
	};
	characters: Character[];
}
