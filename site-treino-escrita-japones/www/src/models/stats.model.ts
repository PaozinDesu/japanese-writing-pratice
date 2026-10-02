// Porte das estatísticas de source/js/account.js (PERIODS, buckets, computeStats e formatadores).
// Os formatadores ficam aqui (e não em utils/) porque são específicos do domínio de estatísticas
// do Kaku (datas/porcentagens/durações de sessões de prática), não utilidades genéricas do app.
import type { CharacterCategory } from "./characters.type";
import type { WritingSession, WritingSessionItem } from "./user-data.model";

export type Period = "hoje" | "semana" | "mes" | "tudo";

export const PERIODS: { id: Period; label: string }[] = [
	{ id: "hoje", label: "Hoje" },
	{ id: "semana", label: "Esta semana" },
	{ id: "mes", label: "Este mês" },
	{ id: "tudo", label: "Todo o período" },
];

export function dayStart(t: number): number {
	const d = new Date(t);
	d.setHours(0, 0, 0, 0);
	return d.getTime();
}

export function periodStart(period: Period, now: number): number {
	const d = new Date(dayStart(now));
	if (period === "hoje") return d.getTime();
	if (period === "semana") {
		d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
		return d.getTime();
	}
	if (period === "mes") {
		d.setDate(1);
		return d.getTime();
	}
	return 0;
}

const MONTHS = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"];
const WEEKDAYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"];

export function catOf(id: string): CharacterCategory {
	return id.split(":")[0] as CharacterCategory;
}

export function fmtDur(ms: number): string {
	const minutes = Math.round(ms / 60000);
	if (minutes < 1) return ms > 0 ? "< 1 min" : "0 min";
	const hours = Math.floor(minutes / 60);
	return hours ? hours + "h " + String(minutes % 60).padStart(2, "0") + "min" : minutes + " min";
}

export function fmtInt(n: number): string {
	return String(n).replaceAll(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export function pct(x: number | null): string {
	return x == null ? "—" : Math.round(x * 100) + "%";
}

export function fmtDate(t: number, withTime = false): string {
	const d = new Date(t);
	const s =
		d.getDate() +
		" " +
		MONTHS[d.getMonth()] +
		(d.getFullYear() !== new Date().getFullYear() ? " " + d.getFullYear() : "");
	return withTime
		? s + ", " + String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0")
		: s;
}

export interface StatsBucket {
	a: number;
	b: number;
	label: string;
	full: string;
	cur: boolean;
}

function buckets(period: Period, now: number, firstT: number): StatsBucket[] {
	if (period === "hoje") {
		const t0 = dayStart(now);
		return Array.from({ length: 24 }, (_, h) => ({
			a: t0 + h * 3600e3,
			b: t0 + (h + 1) * 3600e3,
			label: h % 6 === 0 ? h + "h" : "",
			full: h + "h–" + (h + 1) + "h",
			cur: new Date(now).getHours() === h,
		}));
	}
	if (period === "semana") {
		const t0 = periodStart("semana", now);
		return Array.from({ length: 7 }, (_, i) => {
			const a = new Date(t0);
			a.setDate(a.getDate() + i);
			return {
				a: a.getTime(),
				b: a.getTime() + 864e5,
				label: WEEKDAYS[i],
				full: WEEKDAYS[i] + ", " + fmtDate(a.getTime()),
				cur: a.getTime() === dayStart(now),
			};
		});
	}
	if (period === "mes") {
		const t0 = new Date(periodStart("mes", now));
		const month = t0.getMonth();
		const out: StatsBucket[] = [];
		for (let i = 1; i <= 31; i++) {
			const a = new Date(t0);
			a.setDate(i);
			if (a.getMonth() !== month) break;
			out.push({
				a: a.getTime(),
				b: a.getTime() + 864e5,
				label: i === 1 || i % 5 === 0 ? String(i) : "",
				full: fmtDate(a.getTime()),
				cur: a.getTime() === dayStart(now),
			});
		}
		return out;
	}
	const end = new Date(periodStart("mes", now));
	let start = new Date(firstT ? dayStart(firstT) : now);
	start.setDate(1);
	const minStart = new Date(end);
	minStart.setMonth(minStart.getMonth() - 5);
	if (start > minStart) start = minStart;
	const out: StatsBucket[] = [];
	for (const a = new Date(start); a <= end; a.setMonth(a.getMonth() + 1)) {
		const b = new Date(a);
		b.setMonth(b.getMonth() + 1);
		out.push({
			a: a.getTime(),
			b: b.getTime(),
			label: MONTHS[a.getMonth()],
			full: MONTHS[a.getMonth()] + " " + a.getFullYear(),
			cur: a.getTime() === end.getTime(),
		});
	}
	return out.slice(-18);
}

export interface CharacterTally {
	id: string;
	n: number;
	ok: number;
	fail: number;
}

export interface CategoryTally {
	seen: number;
	ok: number;
}

export interface StatsSeriesPoint extends StatsBucket {
	n: number;
	ok: number;
	fail: number;
	acc: number | null;
}

export interface SessionSummary {
	id: string;
	start: number;
	label: string;
	n: number;
	ok: number;
	fail: number;
	acc: number;
	ms: number;
	demo: boolean;
}

export interface Stats {
	period: Period;
	n: number;
	ok: number;
	fail: number;
	rate: number | null;
	ms: number;
	sessions: SessionSummary[];
	chars: CharacterTally[];
	unique: number;
	byCat: Record<CharacterCategory, CategoryTally>;
	top: CharacterTally[];
	hard: CharacterTally[];
	series: StatsSeriesPoint[];
}

export function computeStats(sessions: WritingSession[], period: Period, now = Date.now()): Stats {
	const t0 = periodStart(period, now);
	const items: WritingSessionItem[] = [];
	const sessionsInRange: { session: WritingSession; items: WritingSessionItem[] }[] = [];
	let firstT = 0;

	for (const session of sessions) {
		const inRange = session.items.filter((i) => i.t >= t0 && i.t <= now);
		for (const i of session.items) if (!firstT || i.t < firstT) firstT = i.t;
		if (inRange.length) {
			sessionsInRange.push({ session, items: inRange });
			items.push(...inRange);
		}
	}

	const n = items.length;
	const ok = items.filter((i) => i.ok).length;
	const fail = n - ok;
	const ms = items.reduce((a, i) => a + (i.ms || 0), 0);

	const perChar = new Map<string, CharacterTally>();
	for (const i of items) {
		const tally = perChar.get(i.c) ?? { id: i.c, n: 0, ok: 0, fail: 0 };
		tally.n++;
		if (i.ok) tally.ok++;
		else tally.fail++;
		perChar.set(i.c, tally);
	}
	const chars = [...perChar.values()];

	const byCat: Record<CharacterCategory, CategoryTally> = {
		hiragana: { seen: 0, ok: 0 },
		katakana: { seen: 0, ok: 0 },
		kanji: { seen: 0, ok: 0 },
	};
	for (const tally of chars) {
		const cat = byCat[catOf(tally.id)];
		cat.seen++;
		if (tally.ok) cat.ok++;
	}

	const top = [...chars].sort((a, b) => b.n - a.n || b.ok - a.ok).slice(0, 8);
	const hard = chars
		.filter((p) => p.fail > 0)
		.sort((a, b) => b.fail - a.fail || a.ok / a.n - b.ok / b.n)
		.slice(0, 8);

	const series: StatsSeriesPoint[] = buckets(period, now, firstT).map((bucket) => {
		const inBucket = items.filter((i) => i.t >= bucket.a && i.t < bucket.b);
		const okInBucket = inBucket.filter((i) => i.ok).length;
		return {
			...bucket,
			n: inBucket.length,
			ok: okInBucket,
			fail: inBucket.length - okInBucket,
			acc: inBucket.length ? okInBucket / inBucket.length : null,
		};
	});

	const sessionSummaries: SessionSummary[] = sessionsInRange
		.sort((a, b) => b.session.start - a.session.start)
		.map(({ session, items: inRange }) => {
			const okInRange = inRange.filter((i) => i.ok).length;
			return {
				id: session.id,
				start: session.start,
				label: session.label,
				n: inRange.length,
				ok: okInRange,
				fail: inRange.length - okInRange,
				acc: okInRange / inRange.length,
				ms: inRange.reduce((a, i) => a + (i.ms || 0), 0),
				demo: !!session.demo,
			};
		});

	return {
		period,
		n,
		ok,
		fail,
		rate: n ? ok / n : null,
		ms,
		sessions: sessionSummaries,
		chars,
		unique: chars.length,
		byCat,
		top,
		hard,
		series,
	};
}
