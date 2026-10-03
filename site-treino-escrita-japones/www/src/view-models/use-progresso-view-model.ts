"use client";

import { useEffect, useState } from "react";
import { type CharacterDatabase, loadCharacters } from "@/models/characters.model";
import { streakOf } from "@/models/practice-session.model";
import { computeStats, fmtDate, fmtDur, fmtInt, PERIODS, pct, type Period } from "@/models/stats.model";
import { UD } from "@/models/user-data.model";
import { useSession } from "./use-session";

export function useProgressoViewModel() {
	const session = useSession();
	const [db, setDb] = useState<CharacterDatabase | null>(null);
	const [period, setPeriod] = useState<Period>("semana");

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	if (!session.isLoggedIn || !session.user) {
		return { isLoggedIn: false as const };
	}

	const data = UD.load(session.user);
	const stats = computeStats(data.sessions, period);
	const streak = streakOf(data);

	return {
		isLoggedIn: true as const,
		periods: PERIODS.map((p) => ({ ...p, selected: p.id === period, select: () => setPeriod(p.id) })),
		streak,
		totals: {
			practiced: fmtInt(stats.n),
			accuracy: pct(stats.rate),
			time: fmtDur(stats.ms),
			unique: fmtInt(stats.unique),
		},
		byCategory: (["hiragana", "katakana", "kanji"] as const).map((category) => {
			const c = stats.byCat[category];
			const total = db?.characters.filter((ch) => ch.category === category).length ?? 0;
			return {
				category,
				seen: c.seen,
				ok: c.ok,
				total,
				percent: total ? (c.ok / total) * 100 : 0,
			};
		}),
		series: stats.series.map((s) => ({ label: s.label, full: s.full, acc: s.acc, n: s.n, height: s.n ? Math.max(6, ((s.acc ?? 0) * 100)) : 4 })),
		top: stats.top.map((t) => ({ char: db?.byId.get(t.id)?.char ?? "?", n: t.n, ok: t.ok })),
		hard: stats.hard.map((t) => ({ char: db?.byId.get(t.id)?.char ?? "?", fail: t.fail, ok: t.ok, n: t.n })),
		sessions: stats.sessions.slice(0, 12).map((s) => ({
			id: s.id,
			label: s.label,
			when: fmtDate(s.start, true),
			n: s.n,
			accuracy: pct(s.acc),
			duration: fmtDur(s.ms),
		})),
	};
}

export type ProgressoViewModel = ReturnType<typeof useProgressoViewModel>;
