"use client";

import { useEffect, useMemo, useState } from "react";
import {
	CATEGORY_OPTIONS,
	type CharacterDatabase,
	filterCharacters,
	JLPT_OPTIONS,
	loadCharacters,
} from "@/models/characters.model";
import type { Character, CharacterCategory, Difficulty, Jlpt } from "@/models/characters.type";
import { useCharacterActions } from "./use-character-actions";

const PAGE_SIZE = 60;

export const DIFFICULTY_OPTIONS: { id: Difficulty; label: string }[] = [
	{ id: "iniciante", label: "Iniciante" },
	{ id: "intermediario", label: "Intermediário" },
	{ id: "avancado", label: "Avançado" },
];

export type CategoryFilter = CharacterCategory | "all";

function toggle<T>(list: T[], value: T): T[] {
	return list.includes(value) ? list.filter((v) => v !== value) : [...list, value];
}

function matchesQuery(c: Character, query: string): boolean {
	const q = query.trim().toLowerCase();
	if (!q) return true;
	if (c.char.toLowerCase().includes(q)) return true;
	if (c.romaji.toLowerCase().includes(q)) return true;
	if (c.reading.toLowerCase().includes(q)) return true;
	if (c.meaning.pt.some((m) => m.toLowerCase().includes(q))) return true;
	if (c.meaning.en.some((m) => m.toLowerCase().includes(q))) return true;
	return false;
}

export function useCaracteresViewModel() {
	const [db, setDb] = useState<CharacterDatabase | null>(null);
	const [query, setQuery] = useState("");
	const [category, setCategory] = useState<CategoryFilter>("all");
	const [jlpt, setJlpt] = useState<Jlpt[]>([]);
	const [difficulty, setDifficulty] = useState<Difficulty[]>([]);
	const [page, setPage] = useState(1);
	const [selectedId, setSelectedId] = useState<string | null>(null);

	useEffect(() => {
		loadCharacters().then(setDb);
	}, []);

	const filtered = useMemo(() => {
		if (!db) return [];
		const categories: CharacterCategory[] = category === "all" ? [] : [category];
		return filterCharacters(db, { categories, jlpt })
			.filter((c) => !difficulty.length || difficulty.includes(c.difficulty))
			.filter((c) => matchesQuery(c, query));
	}, [db, category, jlpt, difficulty, query]);

	const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
	const currentPage = Math.min(page, totalPages);
	const pageItems = filtered.slice((currentPage - 1) * PAGE_SIZE, currentPage * PAGE_SIZE);

	// Sem seleção do usuário ainda, cai no primeiro resultado — o painel nunca fica vazio,
	// sem precisar de um efeito só pra copiar isso pro estado.
	const selectedCharacter: Character | null = selectedId == null ? (pageItems[0] ?? null) : (db?.byId.get(selectedId) ?? null);
	const panel = useCharacterActions(selectedCharacter, "/caracteres");

	function setQueryAndResetPage(value: string) {
		setQuery(value);
		setPage(1);
	}

	function selectCategory(value: CategoryFilter) {
		setCategory(value);
		setPage(1);
	}

	function toggleJlpt(level: Jlpt) {
		setJlpt((prev) => toggle(prev, level));
		setPage(1);
	}

	function toggleDifficulty(level: Difficulty) {
		setDifficulty((prev) => toggle(prev, level));
		setPage(1);
	}

	const categoryTabs = [
		{ id: "all" as const, label: "Todos", count: db?.characters.length ?? 0 },
		...CATEGORY_OPTIONS.map((option) => ({
			id: option.id,
			label: option.label,
			count: db ? db.characters.filter((c) => c.category === option.id).length : 0,
		})),
	].map((tab) => ({ ...tab, selected: category === tab.id, select: () => selectCategory(tab.id) }));

	const jlptChips = JLPT_OPTIONS.map((level) => ({
		level,
		selected: jlpt.includes(level),
		toggle: () => toggleJlpt(level),
	}));

	const difficultyChips = DIFFICULTY_OPTIONS.map((option) => ({
		...option,
		selected: difficulty.includes(option.id),
		toggle: () => toggleDifficulty(option.id),
	}));

	return {
		loading: !db,
		query,
		setQuery: setQueryAndResetPage,
		categoryTabs,
		jlptChips,
		difficultyChips,
		results: pageItems,
		totalResults: filtered.length,
		grandTotal: db?.characters.length ?? 0,
		page: currentPage,
		totalPages,
		setPage,
		selectedCharacter,
		select: (id: string) => setSelectedId(id),
		panel,
	};
}

export type CaracteresViewModel = ReturnType<typeof useCaracteresViewModel>;
