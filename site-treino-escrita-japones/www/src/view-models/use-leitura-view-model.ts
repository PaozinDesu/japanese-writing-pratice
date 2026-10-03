"use client";

import { useEffect, useMemo, useState } from "react";
import {
	CATEGORY_OPTIONS,
	type CharacterDatabase,
	filterCharacters,
	JLPT_OPTIONS,
	loadCharacters,
	poolLabel,
} from "@/models/characters.model";
import type { Character, CharacterCategory, Jlpt } from "@/models/characters.type";
import { Lists } from "@/models/lists.model";
import { charWeight, pickChars, readHistory, ReadSess } from "@/models/practice-session.model";
import { answerOf, readingOk, readingOrder } from "@/models/reading.model";
import { pct } from "@/models/stats.model";
import { UD, type PracticeList, type ReadingSessionItem } from "@/models/user-data.model";
import { uniq } from "@/utils/array";
import { useSession } from "./use-session";

export const READING_SIZES = [10, 20, 30, 50] as const;

interface QuizItem {
	id: string;
	ok: boolean;
	given: string;
	skipped: boolean;
}

export function useLeituraViewModel() {
	const session = useSession();
	const [db, setDb] = useState<CharacterDatabase | null>(null);
	const [view, setView] = useState<"setup" | "quiz" | "result">("setup");

	const [source, setSource] = useState<"filters" | "list">("filters");
	const [categories, setCategories] = useState<CharacterCategory[]>([]);
	const [jlpt, setJlpt] = useState<Jlpt[]>([]);
	const [listId, setListId] = useState<string | null>(null);
	const [size, setSize] = useState<number | "all">(20);
	const [prioritize, setPrioritize] = useState(true);

	const [queue, setQueue] = useState<string[]>([]);
	const [index, setIndex] = useState(0);
	const [answer, setAnswer] = useState("");
	const [result, setResult] = useState<{ ok: boolean; given: string } | null>(null);
	const [done, setDone] = useState<QuizItem[]>([]);
	const [sessionId, setSessionId] = useState<string | null>(null);
	const [startedAt, setStartedAt] = useState(0);
	const [label, setLabel] = useState("");

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	const lists = session.isLoggedIn ? Lists.all() : [];
	const history = readHistory(session.isLoggedIn ? UD.data() : null);

	const pool = useMemo<Character[]>(() => {
		if (!db) return [];
		if (source === "list") {
			const list = lists.find((l) => l.id === listId);
			return list ? (list.chars.map((id) => db.byId.get(id)).filter(Boolean) as Character[]) : [];
		}
		return filterCharacters(db, { categories, jlpt });
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [db, source, categories, jlpt, listId]);

	function begin(ids: string[], quizLabel: string) {
		if (!ids.length) return;
		const prevLast = queue.at(-1) ?? null;
		const ordered = readingOrder(ids, ids.length, prevLast);
		const sid = session.isLoggedIn ? ReadSess.start(quizLabel, ordered.length) : null;
		setQueue(ordered);
		setIndex(0);
		setAnswer("");
		setResult(null);
		setDone([]);
		setLabel(quizLabel);
		setSessionId(sid);
		setStartedAt(Date.now());
		setView("quiz");
	}

	function start() {
		if (!pool.length) return;
		const ids = pool.map((c) => c.id);
		const n = size === "all" ? ids.length : Math.min(size, ids.length);
		const quizLabel =
			"Leitura · " +
			(source === "list"
				? poolLabel({ kind: "list", listName: lists.find((l) => l.id === listId)?.name ?? "" })
				: poolLabel({ kind: "filters", categories, jlpt }));
		begin(pickChars(ids, n, session.isLoggedIn ? history : null, prioritize), quizLabel);
	}

	const hardCharacters = useMemo(() => {
		if (!db) return [];
		return Object.entries(history)
			.map(([id, entry]) => ({ id, ...entry }))
			.filter((h) => h.fail > 0 && db.byId.has(h.id))
			.sort((a, b) => charWeight(b) - charWeight(a))
			.slice(0, 10);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [db, session.user]);

	function practiceList(list: PracticeList) {
		begin(list.chars, "Leitura · " + poolLabel({ kind: "list", listName: list.name }));
	}

	// Nível JLPT só faz sentido para kanji — fica habilitado sempre que a seleção de sistema de
	// escrita inclui kanji: "Todos" (nenhuma categoria marcada, que vale para os três tipos) ou
	// "Kanji". Com Hiragana/Katakana sozinhos não há kanji na seleção, então os chips desabilitam.
	function hasKanjiInSelection(cats: CharacterCategory[]): boolean {
		return !cats.length || cats.includes("kanji");
	}
	const jlptEnabled = hasKanjiInSelection(categories);

	function toggleCategory(id: CharacterCategory) {
		setCategories((prev) => {
			const next = prev.includes(id) ? prev.filter((c) => c !== id) : [...prev, id];
			if (!hasKanjiInSelection(next)) setJlpt([]);
			return next;
		});
	}

	function record(item: Omit<ReadingSessionItem, "t" | "ms">) {
		if (sessionId) {
			ReadSess.record(sessionId, { ...item, t: Date.now(), ms: Math.min(180_000, Date.now() - startedAt) });
		}
		setStartedAt(Date.now());
	}

	function advance(nextDone: QuizItem[]) {
		if (index + 1 >= queue.length) {
			setDone(nextDone);
			setView("result");
			return;
		}
		setDone(nextDone);
		setIndex(index + 1);
		setResult(null);
		setAnswer("");
	}

	const current = view === "quiz" ? (db?.byId.get(queue[index]) ?? null) : null;

	function submit() {
		if (!current || !db) return;
		if (result) {
			advance(done);
			return;
		}
		const trimmed = answer.trim();
		if (!trimmed) return;
		const ok = readingOk(db, current, trimmed);
		setResult({ ok, given: trimmed });
		setDone((prev) => [...prev, { id: current.id, ok, given: trimmed, skipped: false }]);
		record({ c: current.id, ok: ok ? 1 : 0, given: trimmed });
	}

	function skip() {
		if (!current || result) return;
		const nextDone = [...done, { id: current.id, ok: false, given: "", skipped: true }];
		record({ c: current.id, ok: 0, given: "", skipped: 1 });
		advance(nextDone);
	}

	function next() {
		advance(done);
	}

	function endQuiz() {
		if (!done.length) setView("setup");
		else setView("result");
	}

	const answered = done.length;
	const okCount = done.filter((d) => d.ok).length;
	// Puladas contam para o avanço da barra (via `answered`/`done.length`), mas não entram em
	// acertos nem em erros — nem na porcentagem de acerto, que considera só tentativas julgadas.
	const failCount = done.filter((d) => !d.ok && !d.skipped).length;
	const judgedCount = okCount + failCount;
	const accuracy = pct(judgedCount > 0 ? okCount / judgedCount : null);

	return {
		loading: !db,
		view,
		setup: {
			source,
			setSource,
			categories: CATEGORY_OPTIONS.map((option) => ({
				...option,
				count: db ? db.characters.filter((c) => c.category === option.id).length : 0,
				selected: categories.includes(option.id),
				toggle: () => toggleCategory(option.id),
			})),
			jlpt: JLPT_OPTIONS.map((level) => ({
				level,
				count: db ? db.characters.filter((c) => c.jlpt === level).length : 0,
				selected: jlpt.includes(level),
				toggle: () => setJlpt((prev) => (prev.includes(level) ? prev.filter((j) => j !== level) : [...prev, level])),
			})),
			jlptEnabled,
			noneSelected: !categories.length,
			clearFilters: () => setCategories([]),
			lists: lists.map((l) => ({ id: l.id, name: l.name, count: l.chars.length, selected: listId === l.id, select: () => setListId(l.id) })),
			poolCount: pool.length,
			poolLabel:
				source === "list"
					? poolLabel({ kind: "list", listName: lists.find((l) => l.id === listId)?.name ?? "" })
					: poolLabel({ kind: "filters", categories, jlpt }),
			sizes: READING_SIZES,
			size,
			setSize,
			prioritize: prioritize && session.isLoggedIn,
			togglePrioritize: () => session.isLoggedIn && setPrioritize((v) => !v),
			canStart: pool.length > 0,
			start,
			hardCharacters: hardCharacters.map((h) => ({ char: db?.byId.get(h.id)?.char ?? "?", fail: h.fail, accuracy: Math.round((h.ok / h.n) * 100) })),
			reviewHard: () => begin(hardCharacters.map((h) => h.id), "Leitura · Revisão: mais erros"),
			isLoggedIn: session.isLoggedIn,
			myLists: lists.map((l: PracticeList) => ({ id: l.id, name: l.name, count: l.chars.length, practice: () => practiceList(l) })),
		},
		quiz: {
			current,
			position: index + 1,
			total: queue.length,
			progressPercent: queue.length ? (answered / queue.length) * 100 : 0,
			okCount,
			failCount,
			accuracy,
			answer,
			setAnswer,
			result,
			submit,
			skip,
			next,
			endQuiz,
			isLast: index + 1 >= queue.length,
			answerOf: current ? answerOf(current) : null,
		},
		result: {
			total: done.length,
			ok: okCount,
			fail: done.length - okCount,
			label,
			right: done.filter((d) => d.ok).map((d) => {
				const c = db?.byId.get(d.id);
				return { char: c?.char ?? "?", answer: c ? answerOf(c).all[0] : "" };
			}),
			wrong: done
				.filter((d) => !d.ok)
				.map((d) => {
					const c = db?.byId.get(d.id);
					const a = c ? answerOf(c) : null;
					return {
						char: c?.char ?? "?",
						given: d.skipped ? "Pulado" : d.given,
						correct: a?.main ?? "",
						kana: a?.kana ?? "",
						meaning: c && c.category === "kanji" ? c.meaning.pt.join("; ") : "",
					};
				}),
			again: () => begin(queue, label),
			onlyWrong: () => begin(uniq(done.filter((d) => !d.ok).map((d) => d.id)), "Revisão dos erros"),
			backToSetup: () => setView("setup"),
		},
	};
}

export type LeituraViewModel = ReturnType<typeof useLeituraViewModel>;
