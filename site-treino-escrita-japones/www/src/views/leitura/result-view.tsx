import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Typography } from "@/components/ui/typography";
import type { LeituraViewModel } from "@/view-models/use-leitura-view-model";

function headline(rate: number, total: number): string {
	if (!total) return "Prática encerrada";
	if (rate >= 0.8) return "Excelente leitura!";
	if (rate >= 0.5) return "Bom trabalho!";
	return "Continue praticando";
}

export interface ResultViewProps {
	result: LeituraViewModel["result"];
}

export function ResultView({ result }: ResultViewProps) {
	const rate = result.total ? result.ok / result.total : 0;

	return (
		<div className="mx-auto flex w-full max-w-2xl flex-col gap-6 px-5 py-10 sm:px-6 lg:px-12 xl:px-20">
			<div className="flex flex-col gap-2 text-center">
				<Typography role="h1">{headline(rate, result.total)}</Typography>
				<Typography role="body">{result.label}</Typography>
			</div>

			<Card className="grid grid-cols-3 gap-4 text-center">
				<div>
					<Typography role="h2" as="p">
						{result.total}
					</Typography>
					<Typography role="caption">questões</Typography>
				</div>
				<div>
					<Typography role="h2" as="p" className="text-success">
						{result.ok}
					</Typography>
					<Typography role="caption">acertos</Typography>
				</div>
				<div>
					<Typography role="h2" as="p">
						{result.fail}
					</Typography>
					<Typography role="caption">erros</Typography>
				</div>
			</Card>

			{result.wrong.length > 0 && (
				<Card className="flex flex-col gap-3">
					<Typography role="h4">Para revisar</Typography>
					<div className="flex flex-col gap-2">
						{result.wrong.map((w, i) => (
							<div key={i} className="flex items-center justify-between gap-3 rounded-lg border border-border p-3">
								<span className="font-jp text-2xl">{w.char}</span>
								<div className="flex flex-1 flex-col text-sm">
									<span>
										Você respondeu: <strong>{w.given || "—"}</strong>
									</span>
									<span className="text-text-secondary">
										Correto: {w.correct} <span className="font-jp">({w.kana})</span>
										{w.meaning && ` · ${w.meaning}`}
									</span>
								</div>
							</div>
						))}
					</div>
				</Card>
			)}

			<div className="flex flex-col gap-3 sm:flex-row">
				{result.wrong.length > 0 && (
					<Button variant="danger" onClick={result.onlyWrong} className="flex-1">
						Praticar os {result.wrong.length} errados
					</Button>
				)}
				<Button variant="outline" onClick={result.again} className="flex-1">
					Praticar de novo
				</Button>
				<Button onClick={result.backToSetup} className="flex-1">
					Nova prática
				</Button>
			</div>
		</div>
	);
}
