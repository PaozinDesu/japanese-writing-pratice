import { Skeleton } from "@/components/ui/skeleton";
import type { PraticarViewModel } from "@/view-models/use-praticar-view-model";
import { SessionView } from "./session-view";
import { SetupView } from "./setup-view";
import { SummaryView } from "./summary-view";

export interface PraticarViewProps {
	vm: PraticarViewModel;
}

export function PraticarView({ vm }: PraticarViewProps) {
	if (vm.loading) {
		return (
			<div className="mx-auto w-full max-w-3xl px-5 py-10">
				<Skeleton className="h-96 w-full" />
			</div>
		);
	}
	if (vm.view === "session") return <SessionView session={vm.session} />;
	if (vm.view === "summary") return <SummaryView summary={vm.summary} />;
	return <SetupView setup={vm.setup} />;
}
