"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { type CharacterDatabase, loadCharacters } from "@/models/characters.model";
import type { Character } from "@/models/characters.type";
import { useCharacterActions } from "./use-character-actions";

export function useCharacterDetailViewModel() {
	const params = useParams<{ id: string }>();
	const [db, setDb] = useState<CharacterDatabase | null>(null);

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	const id = decodeURIComponent(params.id ?? "");
	const character: Character | null = db?.byId.get(id) ?? null;
	const actions = useCharacterActions(character, `/caracteres/${encodeURIComponent(id)}`);

	return {
		loading: !db,
		character,
		...actions,
	};
}

export type CharacterDetailViewModel = ReturnType<typeof useCharacterDetailViewModel>;
