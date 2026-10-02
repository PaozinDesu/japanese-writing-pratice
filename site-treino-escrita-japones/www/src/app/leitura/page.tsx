"use client";

import { LeituraView } from "@/views/leitura/leitura.view";
import { useLeituraViewModel } from "@/view-models/use-leitura-view-model";

export default function LeituraPage() {
	const vm = useLeituraViewModel();
	return <LeituraView vm={vm} />;
}
