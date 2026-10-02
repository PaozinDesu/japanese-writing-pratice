import { Skeleton } from "@/components/ui/skeleton";
import type { LeituraViewModel } from "@/view-models/use-leitura-view-model";
import { QuizView } from "./quiz-view";
import { ResultView } from "./result-view";
import { SetupView } from "./setup-view";

export interface LeituraViewProps {
	vm: LeituraViewModel;
}

export function LeituraView({ vm }: LeituraViewProps) {
	if (vm.loading) {
		return (
			<div className="mx-auto w-full max-w-3xl px-5 py-10">
				<Skeleton className="h-96 w-full" />
			</div>
		);
	}
	if (vm.view === "quiz") return <QuizView quiz={vm.quiz} />;
	if (vm.view === "result") return <ResultView result={vm.result} />;
	return <SetupView setup={vm.setup} />;
}
