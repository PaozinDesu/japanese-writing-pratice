// Porte da validação de leitura/significado (source/js/rec.js, seção final) e da montagem
// do quiz de leitura (source/js/reading.js). Puro — sem canvas, sem React.
import { shuffle, uniq } from "@/utils/array";
import type { CharacterDatabase } from "./characters.model";
import type { Character, KanjiKunReading, KanjiOnReading } from "./characters.type";

function isKunReading(r: KanjiOnReading | KanjiKunReading): r is KanjiKunReading {
	return "display" in r;
}

function norm(s: string): string {
	return String(s ?? "")
		.toLowerCase()
		.normalize("NFD")
		.replaceAll(/[̀-ͯ]/g, "");
}

function kanaTable(db: CharacterDatabase): Record<string, string> {
	const table: Record<string, string> = {};
	for (const c of db.characters) {
		if (c.category !== "kanji" && c.romaji) table[c.char] = c.romaji;
	}
	return table;
}

function kanaToRomaji(db: CharacterDatabase, s: string): string {
	const table = kanaTable(db);
	const chars = [...s];
	let out = "";
	let doubled = false;
	for (let i = 0; i < chars.length; i++) {
		const c = chars[i];
		const two = c + (chars[i + 1] ?? "");
		if (c === "っ" || c === "ッ") {
			doubled = true;
			continue;
		}
		if (c === "ー") {
			out += out.slice(-1);
			continue;
		}
		let r: string;
		if (chars[i + 1] && table[two]) {
			r = table[two];
			i++;
		} else {
			r = table[c] ?? c;
		}
		if (doubled && r) {
			out += r[0];
			doubled = false;
		}
		out += r;
	}
	return out;
}

export function canonRo(s: string): string {
	let out = String(s ?? "")
		.toLowerCase()
		.replaceAll("ā", "aa")
		.replaceAll("ī", "ii")
		.replaceAll("ū", "uu")
		.replaceAll("ē", "ee")
		.replaceAll("ō", "ou")
		.replaceAll("ô", "ou")
		.replaceAll(/[^a-z]/g, "");
	out = out
		.replaceAll("jy", "j")
		.replaceAll("shi", "si")
		.replaceAll("sh", "sy")
		.replaceAll("chi", "ti")
		.replaceAll("ch", "ty")
		.replaceAll("tsu", "tu")
		.replaceAll("fu", "hu")
		.replaceAll("ji", "zi")
		.replaceAll("j", "zy")
		.replaceAll("di", "zi")
		.replaceAll("du", "zu")
		.replaceAll("oo", "ou")
		.replaceAll("nn", "n")
		.replaceAll("wo", "o");
	return out;
}

function readingKeys(db: CharacterDatabase, e: Character): Set<string> {
	const keys = new Set<string>();
	const addRomaji = (r: string) => {
		keys.add(canonRo(r));
		keys.add(canonRo(r.replaceAll(/\(.*?\)/g, "")));
	};
	if (e.category === "kanji") {
		for (const r of e.readingsRomaji ?? []) addRomaji(r);
		for (const r of [...e.readings.on, ...e.readings.kun]) {
			keys.add(canonRo(kanaToRomaji(db, r.kana)));
			if (isKunReading(r) && r.display) {
				keys.add(canonRo(kanaToRomaji(db, r.display.replaceAll(/\(.*?\)/g, ""))));
			}
		}
	} else {
		addRomaji(e.romaji);
		if (e.reading) keys.add(canonRo(kanaToRomaji(db, e.reading)));
	}
	keys.delete("");
	return keys;
}

export function readingOk(db: CharacterDatabase, e: Character, answer: string): boolean {
	const a = String(answer ?? "").trim();
	if (!a) return false;
	const romaji = /[぀-ヿ]/.test(a) ? kanaToRomaji(db, a) : a;
	return readingKeys(db, e).has(canonRo(romaji));
}

function meaningTokens(e: Character): string[] {
	const tokens: string[] = [];
	for (const m of [...e.meaning.pt, ...e.meaning.en]) {
		for (const raw of norm(m).replaceAll(/\(.*?\)/g, " ").split(/[,;/]| ou | or /)) {
			const t = raw
				.replaceAll(/[^a-z0-9 ]/g, " ")
				.replaceAll(/\s+/g, " ")
				.trim()
				.replace(/^(o|a|os|as|um|uma|the|to|an) /, "");
			if (t) tokens.push(t);
		}
	}
	return tokens;
}

export function meaningOk(e: Character, answer: string): boolean {
	const a = norm(answer)
		.replaceAll(/[^a-z0-9 ]/g, " ")
		.replaceAll(/\s+/g, " ")
		.trim()
		.replace(/^(o|a|os|as|um|uma|the|to|an) /, "");
	if (a.length < 2) return false;
	return meaningTokens(e).some(
		(t) =>
			t === a ||
			(a.length >= 3 && (" " + t + " ").includes(" " + a + " ")) ||
			(t.length >= 4 && (" " + a + " ").includes(" " + t + " ")),
	);
}

export interface ReadingAnswer {
	main: string;
	all: string[];
	kana: string;
}

/** Resposta principal exibida (romaji) + todas as aceitas. */
export function answerOf(e: Character): ReadingAnswer {
	if (e.category !== "kanji") return { main: e.romaji, all: [e.romaji], kana: e.reading };
	const romaji = uniq((e.readingsRomaji ?? []).map((r) => r.replaceAll(/[()]/g, "")));
	const kana = [...e.readings.on.map((o) => o.kana), ...e.readings.kun.map((k) => k.display)].join("、");
	return { main: romaji.join(", "), all: romaji, kana };
}

/** Ordem aleatória, sem repetir o mesmo caractere em sequência (nem entre o fim de uma sessão e o início da próxima). */
export function readingOrder(ids: string[], n: number, avoidFirst: string | null): string[] {
	const q = shuffle(ids).slice(0, n);
	if (q.length > 1 && q[0] === avoidFirst) {
		const j = 1 + Math.trunc(Math.random() * (q.length - 1));
		[q[0], q[j]] = [q[j], q[0]];
	}
	for (let i = 1; i < q.length; i++) {
		if (q[i] === q[i - 1]) {
			const j = q.findIndex((x, k) => k > i && x !== q[i - 1]);
			if (j > 0) [q[i], q[j]] = [q[j], q[i]];
		}
	}
	return q;
}
