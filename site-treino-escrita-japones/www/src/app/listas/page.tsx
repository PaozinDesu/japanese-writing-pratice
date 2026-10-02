"use client";

import { ListasView } from "@/views/listas/listas.view";
import { useListasViewModel } from "@/view-models/use-listas-view-model";

export default function ListasPage() {
	const vm = useListasViewModel();
	return <ListasView vm={vm} />;
}
