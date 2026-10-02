// Porte de `Lists` (source/js/account.js): CRUD das listas de prática do usuário.
import { generateId } from "@/utils/id";
import { uniq } from "@/utils/array";
import { type PracticeList, UD } from "./user-data.model";

export type ListMutationResult = { ok: true } | { error: string };
export type ListCreateResult = { ok: true; list: PracticeList } | { error: string };

function nameError(name: string, exceptId?: string): string {
	const trimmed = String(name ?? "").trim();
	if (!trimmed) return "Dê um nome para a lista.";
	if (trimmed.length > 60) return "Use no máximo 60 caracteres.";
	const clashes = Lists.all().some(
		(l) => l.id !== exceptId && l.name.toLowerCase() === trimmed.toLowerCase(),
	);
	if (clashes) return "Você já tem uma lista com esse nome.";
	return "";
}

export const Lists = {
	all(): PracticeList[] {
		return UD.data()?.lists ?? [];
	},

	get(id: string): PracticeList | null {
		return Lists.all().find((l) => l.id === id) ?? null;
	},

	nameError,

	create(name: string, chars: string[] = []): ListCreateResult {
		const error = nameError(name);
		if (error) return { error };
		const result = UD.mut((data) => {
			const list: PracticeList = {
				id: generateId("l"),
				name: name.trim(),
				chars: uniq(chars),
				created: Date.now(),
				updated: Date.now(),
			};
			data.lists.unshift(list);
			return list;
		});
		return result ? { ok: true, list: result } : { error: "Entre na sua conta para criar listas." };
	},

	rename(id: string, name: string): ListMutationResult {
		const error = nameError(name, id);
		if (error) return { error };
		UD.mut((data) => {
			const list = data.lists.find((l) => l.id === id);
			if (list) {
				list.name = name.trim();
				list.updated = Date.now();
			}
		});
		return { ok: true };
	},

	remove(id: string): void {
		UD.mut((data) => {
			data.lists = data.lists.filter((l) => l.id !== id);
		});
	},

	add(id: string, charIds: string[]): void {
		UD.mut((data) => {
			const list = data.lists.find((l) => l.id === id);
			if (list) {
				list.chars = uniq(list.chars.concat(charIds));
				list.updated = Date.now();
			}
		});
	},

	removeChar(id: string, charId: string): void {
		UD.mut((data) => {
			const list = data.lists.find((l) => l.id === id);
			if (list) {
				list.chars = list.chars.filter((c) => c !== charId);
				list.updated = Date.now();
			}
		});
	},

	toggle(id: string, charId: string): void {
		const list = Lists.get(id);
		if (!list) return;
		if (list.chars.includes(charId)) Lists.removeChar(id, charId);
		else Lists.add(id, [charId]);
	},
};
