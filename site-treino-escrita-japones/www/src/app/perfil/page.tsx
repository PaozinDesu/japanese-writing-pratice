"use client";

import { PerfilView } from "@/views/perfil/perfil.view";
import { usePerfilViewModel } from "@/view-models/use-perfil-view-model";

export default function PerfilPage() {
	const vm = usePerfilViewModel();
	return <PerfilView vm={vm} />;
}
