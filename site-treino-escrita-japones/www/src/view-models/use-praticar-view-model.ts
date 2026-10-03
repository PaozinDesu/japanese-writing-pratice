"use client";

import { useEffect, useMemo, useReducer, useRef, useState } from "react";
import { Auth } from "@/models/auth.model";
import {
	CATEGORY_OPTIONS,
	type CharacterDatabase,
	filterCharacters,
	JLPT_OPTIONS,
	loadCharacters,
	poolLabel,
} from "@/models/characters.model";
import type { Character, CharacterCategory, Jlpt } from "@/models/characters.type";
import { Intent, type PracticeIntent } from "@/models/intent.model";
import { Lists } from "@/models/lists.model";
import {
	charHistory,
	charWeight,
	pickChars,
	Sess,
} from "@/models/practice-session.model";
import { evaluateDrawing, InkController, type RecognitionResult } from "@/models/recognition.model";
import { answerOf, meaningOk, readingOk } from "@/models/reading.model";
import { UD, type PracticeList, type WritingSessionItem } from "@/models/user-data.model";
import { useSession } from "./use-session";

export const PRACTICE_SIZES = [10, 20, 30, 50] as const;
export const BOARD_SIZE = 320;

type AnswerResult = "" | "ok" | "no" | "shown";

interface SessionState {
	queue: string[];
	index: number;
	done: WritingSessionItem[];
	sessionId: string | null;
	label: string;
	saved: boolean;
	startedAt: number;
	strokeCount: number;
	result: RecognitionResult | null;
	busy: boolean;
	showCharacter: boolean;
	readingAnswer: string;
	readingResult: AnswerResult;
	meaningAnswer: string;
	meaningResult: AnswerResult;
	override: boolean | null;
	guide: boolean;
	ghost: boolean;
	warn: number;
}

type SessionAction =
	| { type: "begin"; queue: string[]; sessionId: string | null; label: string; saved: boolean; showCharacter: boolean }
	| { type: "fresh"; showCharacter: boolean }
	| { type: "advance"; done: WritingSessionItem[] }
	| { type: "finish"; done: WritingSessionItem[] }
	| { type: "set-stroke-count"; count: number }
	| { type: "set-busy"; busy: boolean }
	| { type: "set-result"; result: RecognitionResult | null }
	| { type: "toggle-show-character" }
	| { type: "set-reading-answer"; value: string }
	| { type: "set-reading-result"; value: AnswerResult }
	| { type: "set-meaning-answer"; value: string }
	| { type: "set-meaning-result"; value: AnswerResult }
	| { type: "set-override"; value: boolean | null }
	| { type: "toggle-guide" }
	| { type: "toggle-ghost" }
	| { type: "warn" };

const initialSession: SessionState = {
	queue: [],
	index: 0,
	done: [],
	sessionId: null,
	label: "",
	saved: false,
	startedAt: 0,
	strokeCount: 0,
	result: null,
	busy: false,
	showCharacter: true,
	readingAnswer: "",
	readingResult: "",
	meaningAnswer: "",
	meaningResult: "",
	override: null,
	guide: true,
	ghost: false,
	warn: 0,
};

function sessionReducer(state: SessionState, action: SessionAction): SessionState {
	switch (action.type) {
		case "begin":
			return {
				...initialSession,
				guide: state.guide,
				ghost: state.ghost,
				queue: action.queue,
				sessionId: action.sessionId,
				label: action.label,
				saved: action.saved,
				showCharacter: action.showCharacter,
				startedAt: Date.now(),
			};
		case "fresh":
			return {
				...state,
				strokeCount: 0,
				result: null,
				busy: false,
				showCharacter: action.showCharacter,
				readingAnswer: "",
				readingResult: "",
				meaningAnswer: "",
				meaningResult: "",
				override: null,
				warn: 0,
				startedAt: Date.now(),
			};
		case "advance":
			return { ...state, done: action.done, index: state.index + 1 };
		case "finish":
			return { ...state, done: action.done };
		case "set-stroke-count":
			return { ...state, strokeCount: action.count, warn: 0 };
		case "set-busy":
			return { ...state, busy: action.busy };
		case "set-result":
			return { ...state, result: action.result, busy: false, showCharacter: true };
		case "toggle-show-character":
			return { ...state, showCharacter: !state.showCharacter };
		case "set-reading-answer":
			return { ...state, readingAnswer: action.value, readingResult: "" };
		case "set-reading-result":
			return { ...state, readingResult: action.value };
		case "set-meaning-answer":
			return { ...state, meaningAnswer: action.value, meaningResult: "" };
		case "set-meaning-result":
			return { ...state, meaningResult: action.value };
		case "set-override":
			return { ...state, override: action.value };
		case "toggle-guide":
			return { ...state, guide: !state.guide };
		case "toggle-ghost":
			return { ...state, ghost: !state.ghost };
		case "warn":
			return { ...state, warn: state.warn + 1 };
		default:
			return state;
	}
}

function subtitleOf(c: Character): string {
	return c.category === "kanji" ? c.meaning.pt[0] : c.romaji;
}

function finalOk(state: SessionState): boolean {
	if (!state.result) return false;
	if (state.override != null) return state.override;
	return state.result.verdict === "ok" && state.readingResult !== "no" && state.meaningResult !== "no";
}

export function usePraticarViewModel() {
	const session = useSession();
	const [db, setDb] = useState<CharacterDatabase | null>(null);
	const [view, setView] = useState<"setup" | "session" | "summary">("setup");

	const [source, setSource] = useState<"filters" | "list">("filters");
	const [categories, setCategories] = useState<CharacterCategory[]>([]);
	const [jlpt, setJlpt] = useState<Jlpt[]>([]);
	const [listId, setListId] = useState<string | null>(null);
	const [size, setSize] = useState<number | "all">(20);
	const [prioritize, setPrioritize] = useState(true);
	const [memory, setMemory] = useState(false);

	const [state, dispatch] = useReducer(sessionReducer, initialSession);
	const ink = useRef<InkController>(null);
	ink.current ??= new InkController(BOARD_SIZE);

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	useEffect(() => {
		const intent = Intent.take();
		if (!intent) return;
		applyIntent(intent);
		// eslint-disable-next-line react-hooks/exhaustive-deps -- só aplica a intenção pendente uma vez, ao montar
	}, []);

	function applyIntent(intent: PracticeIntent) {
		if (intent.kind === "filters") {
			setSource("filters");
			setCategories(intent.categories);
			setJlpt(intent.jlpt);
			return;
		}
		if (intent.kind === "chars") {
			startWith(intent.chars, intent.label);
			return;
		}
		if (intent.kind === "list") {
			const list = Lists.get(intent.listId);
			if (list?.chars.length) {
				setSource("list");
				setListId(list.id);
				const history = charHistory(UD.data());
				startWith(pickChars(list.chars, Math.min(list.chars.length, size === "all" ? list.chars.length : size), history, prioritize), "Lista: " + list.name);
			}
		}
	}

	const lists = session.isLoggedIn ? Lists.all() : [];
	const history = charHistory(session.isLoggedIn ? UD.data() : null);

	const pool = useMemo<Character[]>(() => {
		if (!db) return [];
		if (source === "list") {
			const list = lists.find((l) => l.id === listId);
			return list ? (list.chars.map((id) => db.byId.get(id)).filter(Boolean) as Character[]) : [];
		}
		return filterCharacters(db, { categories, jlpt });
		// eslint-disable-next-line react-hooks/exhaustive-deps -- `lists` é recomputado a cada render; comparar por listId evita loop
	}, [db, source, categories, jlpt, listId]);

	function startWith(ids: string[], label: string) {
		if (!ids.length) return;
		const isLoggedIn = !!Auth.current();
		const sessionId = isLoggedIn ? Sess.start({ label, src: null, n: ids.length }) : null;
		ink.current!.clear();
		dispatch({ type: "begin", queue: ids, sessionId, label, saved: isLoggedIn, showCharacter: !memory });
		setView("session");
	}

	function start() {
		if (!pool.length) return;
		const ids = pool.map((c) => c.id);
		const n = size === "all" ? ids.length : Math.min(size, ids.length);
		const label = source === "list" ? poolLabel({ kind: "list", listName: lists.find((l) => l.id === listId)?.name ?? "" }) : poolLabel({ kind: "filters", categories, jlpt });
		startWith(pickChars(ids, n, session.isLoggedIn ? history : null, prioritize), label);
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

	function reviewHard() {
		startWith(
			hardCharacters.map((h) => h.id),
			"Revisão: mais erros",
		);
	}

	function practiceList(list: PracticeList) {
		startWith(list.chars, poolLabel({ kind: "list", listName: list.name }));
	}

	const current = view === "session" ? (db?.byId.get(state.queue[state.index]) ?? null) : null;
	const upNext = db
		? state.queue
				.slice(state.index + 1, state.index + 7)
				.map((id) => db.byId.get(id))
				.filter((c): c is Character => !!c)
		: [];
	const correctRomaji = current ? answerOf(current).main : "";
	const identified = state.result?.id && db ? (db.byId.get(state.result.id) ?? null) : null;
	const identifiedRomaji = identified ? answerOf(identified).main : "";

	function commit(): WritingSessionItem[] {
		if (!current) return state.done;
		const item: WritingSessionItem = {
			c: current.id,
			ok: finalOk(state) ? 1 : 0,
			v: state.result?.verdict ?? "",
			s: state.result?.sim ?? 0,
			t: Date.now(),
			ms: Math.min(180_000, Date.now() - state.startedAt),
			rd: state.readingResult || (state.readingAnswer ? "shown" : ""),
			mn: state.meaningResult || (state.meaningAnswer ? "shown" : ""),
		};
		if (state.sessionId) Sess.record(state.sessionId, item);
		return [...state.done, item];
	}

	function next() {
		if (!state.result) return;
		const done = commit();
		ink.current!.clear();
		if (state.index + 1 >= state.queue.length) {
			dispatch({ type: "finish", done });
			setView("summary");
		} else {
			dispatch({ type: "advance", done });
			dispatch({ type: "fresh", showCharacter: !memory });
		}
	}

	async function submitDrawing() {
		if (!current || !db || state.result || state.busy) return;
		if (!ink.current!.strokes.length) {
			dispatch({ type: "warn" });
			return;
		}
		dispatch({ type: "set-busy", busy: true });
		try {
			const result = await evaluateDrawing(ink.current!.strokes, db, current, () => ink.current!.toDataUrl());
			dispatch({ type: "set-result", result });
		} catch {
			dispatch({
				type: "set-result",
				result: {
					id: null,
					verdict: "no",
					sim: 0,
					user: ink.current!.strokes.length,
					exp: current.strokes,
					shapeOk: false,
					strokesOk: false,
					img: "",
				},
			});
		}
	}

	function undo() {
		if (state.result || state.busy) return;
		ink.current!.undo();
		dispatch({ type: "set-stroke-count", count: ink.current!.strokes.length });
	}

	function clearDrawing() {
		ink.current!.clear();
		dispatch({ type: "set-stroke-count", count: 0 });
	}

	function checkReading() {
		if (!current || !db || !state.readingAnswer.trim()) return;
		dispatch({ type: "set-reading-result", value: readingOk(db, current, state.readingAnswer) ? "ok" : "no" });
	}

	function checkMeaning() {
		if (!current || !state.meaningAnswer.trim()) return;
		dispatch({ type: "set-meaning-result", value: meaningOk(current, state.meaningAnswer) ? "ok" : "no" });
	}

	function endSession() {
		ink.current!.clear();
		if (!state.done.length) setView("setup");
		else setView("summary");
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

	const doneOk = state.done.filter((i) => i.ok).length;
	const wrongIds = [...new Set(state.done.filter((i) => !i.ok).map((i) => i.c))];
	// Enquanto o resultado do caractere atual ainda não foi confirmado em "Próximo", ele já conta
	// nos contadores de acerto/erro (com o veredito automático ou a marcação manual, o que valer),
	// mas ainda não avança a barra de progresso — essa só avança quando o item é de fato commitado.
	const pendingOk = state.result ? finalOk(state) : null;

	return {
		loading: !db,
		view,

		// setup
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
			lists: lists.map((l: PracticeList) => ({ id: l.id, name: l.name, count: l.chars.length, selected: listId === l.id, select: () => setListId(l.id) })),
			listId,
			poolCount: pool.length,
			poolLabel:
				source === "list"
					? poolLabel({ kind: "list", listName: lists.find((l) => l.id === listId)?.name ?? "" })
					: poolLabel({ kind: "filters", categories, jlpt }),
			sizes: PRACTICE_SIZES,
			size,
			setSize,
			memory,
			setMemory,
			prioritize: prioritize && session.isLoggedIn,
			togglePrioritize: () => session.isLoggedIn && setPrioritize((v) => !v),
			canStart: pool.length > 0,
			start,
			hardCharacters: hardCharacters.map((h) => ({ char: db?.byId.get(h.id)?.char ?? "?", fail: h.fail, accuracy: Math.round((h.ok / h.n) * 100) })),
			reviewHard,
			isLoggedIn: session.isLoggedIn,
			myLists: lists.map((l: PracticeList) => ({ id: l.id, name: l.name, count: l.chars.length, practice: () => practiceList(l) })),
		},

		// session
		session: {
			current,
			upNext,
			correctRomaji,
			position: state.index + 1,
			total: state.queue.length,
			progressPercent: state.queue.length ? (state.done.length / state.queue.length) * 100 : 0,
			okCount: doneOk + (pendingOk === true ? 1 : 0),
			failCount: state.done.length - doneOk + (pendingOk === false ? 1 : 0),
			label: state.label,
			memory,
			showCharacter: state.showCharacter,
			toggleShowCharacter: () => dispatch({ type: "toggle-show-character" }),
			guide: state.guide,
			toggleGuide: () => dispatch({ type: "toggle-guide" }),
			ghost: state.ghost,
			toggleGhost: () => dispatch({ type: "toggle-ghost" }),
			warn: state.warn,
			ink: ink.current!,
			strokeCount: state.strokeCount,
			onStrokeEnd: () => dispatch({ type: "set-stroke-count", count: ink.current!.strokes.length }),
			undo,
			clear: clearDrawing,
			submitDrawing,
			busy: state.busy,
			result: state.result,
			identified,
			identifiedRomaji,
			finalOk: finalOk(state),
			overrideValue: state.override,
			override: (value: boolean) => dispatch({ type: "set-override", value }),
			readingAnswer: state.readingAnswer,
			setReadingAnswer: (value: string) => dispatch({ type: "set-reading-answer", value }),
			readingResult: state.readingResult,
			checkReading,
			meaningAnswer: state.meaningAnswer,
			setMeaningAnswer: (value: string) => dispatch({ type: "set-meaning-answer", value }),
			meaningResult: state.meaningResult,
			checkMeaning,
			next,
			isLast: state.index + 1 >= state.queue.length,
			endSession,
			saved: state.saved,
		},

		// summary
		summary: {
			total: state.done.length,
			ok: doneOk,
			fail: state.done.length - doneOk,
			label: state.label,
			results: state.done.map((item) => {
				const c = db?.byId.get(item.c);
				const subtitle = c ? subtitleOf(c) : "";
				return { char: c?.char ?? "?", ok: !!item.ok, subtitle };
			}),
			hasWrong: wrongIds.length > 0,
			wrongCount: wrongIds.length,
			retryWrong: () => startWith(wrongIds, "Revisão da sessão"),
			practiceAgain: () => startWith([...new Set(state.queue)], state.label),
			newSession: () => setView("setup"),
		},
	};
}

export type PraticarViewModel = ReturnType<typeof usePraticarViewModel>;
