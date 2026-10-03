"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";
import { Auth } from "@/models/auth.model";
import type { Character } from "@/models/characters.type";
import { Intent } from "@/models/intent.model";
import { Lists } from "@/models/lists.model";
import { useSession } from "./use-session";

/**
 * Ações de um caractere (adicionar/remover de listas, praticar, ir pro login) — porte de
 * `listPickerVals` (source/js/account.js), desacoplado de rota: usado tanto pela página
 * `/caracteres/[id]` quanto pelo painel inline da lista de Caracteres.
 */
export function useCharacterActions(character: Character | null, returnTo: string) {
	const router = useRouter();
	const session = useSession();
	const [newListName, setNewListName] = useState("");
	const [feedback, setFeedback] = useState("");
	const [feedbackError, setFeedbackError] = useState("");
	// eslint-disable-next-line @typescript-eslint/no-unused-vars -- só o setter é usado; o valor existe pra forçar o re-render após mutar Lists
	const [version, setVersion] = useState(0);

	function bump() {
		setVersion((v) => v + 1);
	}

	const lists = session.user ? Lists.all() : [];
	const inCount = character ? lists.filter((l) => l.chars.includes(character.id)).length : 0;

	function toggleList(listId: string) {
		if (!character) return;
		Lists.toggle(listId, character.id);
		bump();
	}

	function createList(event?: FormEvent) {
		event?.preventDefault();
		if (!character) return;
		const result = Lists.create(newListName, [character.id]);
		if ("error" in result) {
			setFeedbackError(result.error);
			return;
		}
		setFeedbackError("");
		setNewListName("");
		setFeedback(`Lista "${result.list.name}" criada com este caractere.`);
		bump();
	}

	function practiceThis() {
		if (!character) return;
		Intent.set({ kind: "chars", chars: [character.id], label: "Caractere " + character.char });
		router.push("/praticar");
	}

	function goToLogin() {
		Auth.setReturnTo(returnTo);
		router.push("/login");
	}

	function goToCharacter(characterId: string) {
		router.push(`/caracteres/${encodeURIComponent(characterId)}`);
	}

	return {
		isLoggedIn: session.isLoggedIn,
		lists: lists.map((l) => ({
			id: l.id,
			name: l.name,
			count: l.chars.length,
			has: character ? l.chars.includes(character.id) : false,
			toggle: () => toggleList(l.id),
		})),
		inCount,
		newListName,
		setNewListName,
		createList,
		feedback,
		feedbackError,
		practiceThis,
		goToLogin,
		goToCharacter,
	};
}

export type CharacterActions = ReturnType<typeof useCharacterActions>;
