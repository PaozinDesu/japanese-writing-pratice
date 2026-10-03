// Porte de Sess/ReadSess/charHistory/charWeight/pickChars/streakOf (source/js/account.js).
import { shuffle } from "@/utils/array";
import { generateId } from "@/utils/id";
import { dayStart } from "./stats.model";
import { UD, type ReadingSessionItem, type UserData, type WritingSessionItem } from "./user-data.model";

export const Sess = {
	start(meta: { label: string; src: unknown; n: number }): string | null {
		return UD.mut((data) => {
			data.sessions = data.sessions.filter((s) => s.items.length);
			const session = {
				id: generateId("s"),
				start: Date.now(),
				end: Date.now(),
				ms: 0,
				label: meta.label,
				src: meta.src ?? null,
				planned: meta.n,
				items: [],
			};
			data.sessions.push(session);
			return session.id;
		});
	},

	record(sessionId: string, item: WritingSessionItem): void {
		UD.mut((data) => {
			const session = data.sessions.find((s) => s.id === sessionId);
			if (!session) return;
			session.items.push(item);
			session.end = item.t;
			session.ms += item.ms;
		});
	},
};

export const ReadSess = {
	start(label: string, n: number): string | null {
		return UD.mut((data) => {
			data.readSessions = data.readSessions.filter((s) => s.items.length);
			const session = { id: generateId("r"), start: Date.now(), label, planned: n, items: [] };
			data.readSessions.push(session);
			return session.id;
		});
	},

	record(sessionId: string, item: ReadingSessionItem): void {
		UD.mut((data) => {
			const session = data.readSessions.find((s) => s.id === sessionId);
			if (session) {
				session.items.push(item);
				session.end = item.t;
			}
		});
	},
};

export interface CharHistoryEntry {
	n: number;
	ok: number;
	fail: number;
	last: number;
	lastOk: boolean;
}

export type CharHistory = Record<string, CharHistoryEntry>;

function historyFrom(sessions: { items: { c: string; ok: 0 | 1; t: number }[] }[]): CharHistory {
	const history: CharHistory = {};
	for (const session of sessions) {
		for (const item of session.items) {
			const entry = history[item.c] ?? (history[item.c] = { n: 0, ok: 0, fail: 0, last: 0, lastOk: true });
			entry.n++;
			if (item.ok) entry.ok++;
			else entry.fail++;
			if (item.t >= entry.last) {
				entry.last = item.t;
				entry.lastOk = !!item.ok;
			}
		}
	}
	return history;
}

export function charHistory(data: UserData | null): CharHistory {
	return historyFrom(data?.sessions ?? []);
}

export function readHistory(data: UserData | null): CharHistory {
	return historyFrom(data?.readSessions ?? []);
}

/** Sorteio ponderado: caracteres com mais erros (e errados na última vez) aparecem com mais frequência. */
export function charWeight(entry: CharHistoryEntry | undefined): number {
	if (!entry) return 1;
	const errorRate = (entry.fail + 0.5) / (entry.n + 1);
	return 0.35 + 3 * errorRate + (entry.lastOk ? 0 : 1.2);
}

export function pickChars(
	ids: string[],
	n: number,
	history: CharHistory | null,
	prioritize: boolean,
): string[] {
	if (!prioritize || !history) return shuffle(ids).slice(0, n);
	const keyed = ids.map((id) => ({ id, k: Math.random() ** (1 / charWeight(history[id])) }));
	keyed.sort((a, b) => b.k - a.k);
	return shuffle(keyed.slice(0, n).map((x) => x.id));
}

export function streakOf(data: UserData | null, now = Date.now()): number {
	const days = new Set<number>();
	for (const session of data?.sessions ?? []) {
		for (const item of session.items) days.add(dayStart(item.t));
	}
	let t = dayStart(now);
	if (!days.has(t)) {
		const yesterday = new Date(t);
		yesterday.setDate(yesterday.getDate() - 1);
		t = yesterday.getTime();
	}
	let streak = 0;
	while (days.has(t)) {
		streak++;
		const previous = new Date(t);
		previous.setDate(previous.getDate() - 1);
		t = previous.getTime();
	}
	return streak;
}
