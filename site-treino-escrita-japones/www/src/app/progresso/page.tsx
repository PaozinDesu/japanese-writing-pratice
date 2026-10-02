"use client";

import { ProgressoView } from "@/views/progresso/progresso.view";
import { useProgressoViewModel } from "@/view-models/use-progresso-view-model";

export default function ProgressoPage() {
	const vm = useProgressoViewModel();
	return <ProgressoView vm={vm} />;
}
