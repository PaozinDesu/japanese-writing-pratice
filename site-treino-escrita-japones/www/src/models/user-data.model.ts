// Porte de `UD` (source/js/account.js): dados por usuário (listas, sessões de escrita e de leitura).
import { Auth, type User } from "./auth.model";
import { KS } from "./local-store.model";

export interface PracticeList {
	id: string;
	name: string;
	chars: string[];
	created: number;
	updated: number;
}

export interface WritingSessionItem {
	/** id do caractere (ex.: "kanji:山") */
	c: string;
	ok: 0 | 1;
	/** veredito do reconhecimento: "ok" | "almost" | "no" | "" */
	v: string;
	/** similaridade (0–100) */
	s: number;
	t: number;
	ms: number;
	/** resultado da leitura pedida: "ok" | "no" | "shown" | "" */
	rd: string;
	/** resultado do significado pedido: "ok" | "no" | "shown" | "" */
	mn: string;
}

export interface WritingSession {
	id: string;
	start: number;
	end: number;
	ms: number;
	label: string;
	src: unknown;
	planned: number;
	items: WritingSessionItem[];
	demo?: boolean;
}

export interface ReadingSessionItem {
	c: string;
	ok: 0 | 1;
	given: string;
	skipped?: 0 | 1;
	t: number;
	ms: number;
}

export interface ReadingSession {
	id: string;
	start: number;
	end?: number;
	label: string;
	planned: number;
	items: ReadingSessionItem[];
}

export interface UserData {
	lists: PracticeList[];
	sessions: WritingSession[];
	readSessions: ReadingSession[];
}

function emptyUserData(): UserData {
	return { lists: [], sessions: [], readSessions: [] };
}

export const UD = {
	load(user: User): UserData {
		const stored = KS.get<Partial<UserData>>("user." + user.id, {});
		return { ...emptyUserData(), ...stored };
	},

	save(user: User, data: UserData): void {
		KS.set("user." + user.id, data);
	},

	/** Lê, transforma e salva os dados do usuário atual numa única operação; `null` se ninguém está logado. */
	mut<T>(fn: (data: UserData, user: User) => T): T | null {
		const user = Auth.current();
		if (!user) return null;
		const data = UD.load(user);
		const result = fn(data, user);
		UD.save(user, data);
		return result;
	},

	data(): UserData | null {
		const user = Auth.current();
		return user ? UD.load(user) : null;
	},
};
