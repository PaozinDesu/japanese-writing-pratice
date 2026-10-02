"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { CATEGORY_OPTIONS, type CharacterDatabase, loadCharacters } from "@/models/characters.model";
import type { Character, CharacterCategory } from "@/models/characters.type";
import { Intent } from "@/models/intent.model";
import { charHistory } from "@/models/practice-session.model";
import { UD } from "@/models/user-data.model";
import { useSession } from "./use-session";

export interface CategoryProgress {
	category: CharacterCategory;
	label: string;
	description: string;
	total: number;
	masteredCount: number;
	percent: number;
}

const DESCRIPTIONS: Record<CharacterCategory, string> = {
	hiragana: "Silabário fonético",
	katakana: "Palavras estrangeiras",
	kanji: "Os 2.136 de uso comum",
};

function dayOfYear(date: Date): number {
	const start = new Date(date.getFullYear(), 0, 0);
	return Math.floor((date.getTime() - start.getTime()) / 864e5);
}

/** Sem uma "palavra do dia" no protótipo: escolhe de forma estável um kanji N5 por dia do ano. */
function pickCharacterOfDay(db: CharacterDatabase): Character | null {
	const pool = db.characters.filter((c) => c.category === "kanji" && c.jlpt === "N5");
	const source = pool.length ? pool : db.characters;
	return source.length ? source[dayOfYear(new Date()) % source.length] : null;
}

export function useHomeViewModel() {
	const router = useRouter();
	const session = useSession();
	const [db, setDb] = useState<CharacterDatabase | null>(null);

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	const history = charHistory(session.user ? UD.load(session.user) : null);

	const categories: CategoryProgress[] = db
		? (["hiragana", "katakana", "kanji"] as const).map((category) => {
				const inCategory = db.characters.filter((c) => c.category === category);
				const masteredCount = inCategory.filter((c) => (history[c.id]?.ok ?? 0) > 0).length;
				return {
					category,
					label: CATEGORY_OPTIONS.find((o) => o.id === category)!.label,
					description: DESCRIPTIONS[category],
					total: inCategory.length,
					masteredCount,
					percent: inCategory.length ? (masteredCount / inCategory.length) * 100 : 0,
				};
			})
		: [];

	const heroCharacter = db ? pickCharacterOfDay(db) : null;

	function practiceCharacterNow(character: Character) {
		Intent.set({ kind: "chars", chars: [character.id], label: "Caractere " + character.char });
		router.push("/praticar");
	}

	return {
		isLoggedIn: session.isLoggedIn,
		loading: !db,
		categories,
		heroCharacter,
		practiceCharacterNow,
	};
}

export type HomeViewModel = ReturnType<typeof useHomeViewModel>;
