// Porte de `Intent` (source/js/account.js): passa uma intenção de uma tela pra outra
// (ex.: "praticar este caractere" partindo do detalhe de um caractere até /praticar).
import type { CharacterCategory, Jlpt } from "./characters.type";
import { KS } from "./local-store.model";

const TTL_MS = 15 * 60_000;

export type PracticeIntent =
	| { kind: "chars"; chars: string[]; label: string }
	| { kind: "list"; listId: string }
	| { kind: "filters"; categories: CharacterCategory[]; jlpt: Jlpt[] };

interface StoredIntent {
	at: number;
	value: PracticeIntent;
}

export const Intent = {
	set(value: PracticeIntent): void {
		KS.set("intent", { at: Date.now(), value } satisfies StoredIntent);
	},

	/** Consome a intenção pendente (uma única vez) se ainda estiver dentro da validade. */
	take(): PracticeIntent | null {
		const stored = KS.get<StoredIntent | null>("intent", null);
		if (!stored) return null;
		KS.del("intent");
		return Date.now() - stored.at < TTL_MS ? stored.value : null;
	},
};
