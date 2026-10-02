"use client";

import { CaracteresView } from "@/views/caracteres/caracteres.view";
import { useCaracteresViewModel } from "@/view-models/use-caracteres-view-model";

export default function CaracteresPage() {
	const vm = useCaracteresViewModel();
	return <CaracteresView vm={vm} />;
}
