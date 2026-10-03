"use client";

import { CharacterDetailView } from "@/views/caracteres/character-detail.view";
import { useCharacterDetailViewModel } from "@/view-models/use-character-detail-view-model";

export default function CharacterDetailPage() {
	const vm = useCharacterDetailViewModel();
	return <CharacterDetailView vm={vm} />;
}
