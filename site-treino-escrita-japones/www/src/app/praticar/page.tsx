"use client";

import { PraticarView } from "@/views/praticar/praticar.view";
import { usePraticarViewModel } from "@/view-models/use-praticar-view-model";

export default function PraticarPage() {
	const vm = usePraticarViewModel();
	return <PraticarView vm={vm} />;
}
