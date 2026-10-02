"use client";

import { CadastroView } from "@/views/cadastro/cadastro.view";
import { useCadastroViewModel } from "@/view-models/use-cadastro-view-model";

export default function CadastroPage() {
	const vm = useCadastroViewModel();
	return <CadastroView vm={vm} />;
}
