import { Check, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Typography } from "@/components/ui/typography";
import type { PraticarViewModel } from "@/view-models/use-praticar-view-model";

export interface SummaryViewProps {
	summary: PraticarViewModel["summary"];
}

function headline(rate: number, total: number): string {
	if (!total) return "Sessão encerrada";
	if (rate >= 0.8) return "Excelente sessão!";
	if (rate >= 0.5) return "Bom trabalho!";
	return "Continue praticando";
}

export function SummaryView({ summary }: SummaryViewProps) {
	const rate = summary.total ? summary.ok / summary.total : 0;

	return (
		<div className="mx-auto flex w-full max-w-2xl flex-col gap-6 px-5 py-10 sm:px-6 lg:px-12 xl:px-20">
			<div className="flex flex-col gap-2 text-center">
				<Typography role="h1">{headline(rate, summary.total)}</Typography>
				<Typography role="body">{summary.label}</Typography>
			</div>

			<Card className="grid grid-cols-3 gap-4 text-center">
				<div>
					<Typography role="h2" as="p">
						{summary.total}
					</Typography>
					<Typography role="caption">caracteres</Typography>
				</div>
				<div>
					<Typography role="h2" as="p" className="text-success">
						{summary.ok}
					</Typography>
					<Typography role="caption">acertos</Typography>
				</div>
				<div>
					<Typography role="h2" as="p">
						{summary.fail}
					</Typography>
					<Typography role="caption">erros</Typography>
				</div>
			</Card>

			<div className="flex flex-wrap gap-2">
				{summary.results.map((r, i) => (
					<span
						key={i}
						className={`font-jp flex items-center gap-1 rounded-lg border px-2 py-1 text-lg ${r.ok ? "border-success-border bg-success-subtle" : "border-error-border bg-error-subtle"}`}
					>
						{r.ok ? <Check className="size-3.5 text-success" aria-hidden="true" /> : <X className="size-3.5 text-error" aria-hidden="true" />}
						{r.char}
					</span>
				))}
			</div>

			<div className="flex flex-col gap-3 sm:flex-row">
				{summary.hasWrong && (
					<Button variant="danger" onClick={summary.retryWrong} className="flex-1">
						Praticar os {summary.wrongCount} errados
					</Button>
				)}
				<Button variant="outline" onClick={summary.practiceAgain} className="flex-1">
					Praticar de novo
				</Button>
				<Button onClick={summary.newSession} className="flex-1">
					Nova sessão
				</Button>
			</div>
		</div>
	);
}
