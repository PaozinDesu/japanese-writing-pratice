"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useEffect, useState } from "react";
import { type CharacterDatabase, loadCharacters } from "@/models/characters.model";
import { Intent } from "@/models/intent.model";
import { Lists } from "@/models/lists.model";
import { useSession } from "./use-session";

export function useListasViewModel() {
	const router = useRouter();
	const session = useSession();
	const [db, setDb] = useState<CharacterDatabase | null>(null);
	// eslint-disable-next-line @typescript-eslint/no-unused-vars -- só o setter é usado; o valor existe pra forçar o re-render
	const [version, setVersion] = useState(0);
	const [newName, setNewName] = useState("");
	const [error, setError] = useState("");
	const [openId, setOpenId] = useState<string | null>(null);
	const [renamingId, setRenamingId] = useState<string | null>(null);
	const [renameValue, setRenameValue] = useState("");

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	function bump() {
		setVersion((v) => v + 1);
	}

	if (!session.isLoggedIn) {
		return { isLoggedIn: false as const };
	}

	// O componente re-renderiza quando `version` muda, o que refaz esta leitura de `Lists.all()`.
	const lists = Lists.all();

	function createList(event?: FormEvent) {
		event?.preventDefault();
		const result = Lists.create(newName, []);
		if ("error" in result) {
			setError(result.error);
			return;
		}
		setError("");
		setNewName("");
		bump();
	}

	function removeList(id: string) {
		Lists.remove(id);
		if (openId === id) setOpenId(null);
		bump();
	}

	function startRename(id: string, currentName: string) {
		setRenamingId(id);
		setRenameValue(currentName);
	}

	function confirmRename(event?: FormEvent) {
		event?.preventDefault();
		if (!renamingId) return;
		const result = Lists.rename(renamingId, renameValue);
		if (!("error" in result)) {
			setRenamingId(null);
			bump();
		}
	}

	function removeChar(listId: string, charId: string) {
		Lists.removeChar(listId, charId);
		bump();
	}

	function practiceList(listId: string) {
		const list = Lists.get(listId);
		if (!list) return;
		Intent.set({ kind: "list", listId: list.id });
		router.push("/praticar");
	}

	return {
		isLoggedIn: true as const,
		newName,
		setNewName,
		error,
		createList,
		lists: lists.map((l) => ({
			id: l.id,
			name: l.name,
			count: l.chars.length,
			open: openId === l.id,
			toggle: () => setOpenId(openId === l.id ? null : l.id),
			isRenaming: renamingId === l.id,
			startRename: () => startRename(l.id, l.name),
			remove: () => removeList(l.id),
			practice: () => practiceList(l.id),
			characters: l.chars.map((id) => db?.byId.get(id)).filter((c) => !!c),
			removeChar: (charId: string) => removeChar(l.id, charId),
		})),
		renameValue,
		setRenameValue,
		confirmRename,
		cancelRename: () => setRenamingId(null),
	};
}

export type ListasViewModel = ReturnType<typeof useListasViewModel>;
