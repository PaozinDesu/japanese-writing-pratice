"use client";

import { Volume2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { FittedGlyph } from "@/components/ui/fitted-glyph";
import { ProgressBar } from "@/components/ui/progress-bar";
import { Typography } from "@/components/ui/typography";
import { input as inputField } from "@/components/ui/variants";
import type { CharacterCategory } from "@/models/characters.type";
import type { LeituraViewModel } from "@/view-models/use-leitura-view-model";
import { speakJapanese } from "@/utils/speech";
import { cn } from "@/utils/cn";

const CATEGORY_LABEL: Record<CharacterCategory, string> = { hiragana: "Hiragana", katakana: "Katakana", kanji: "Kanji" };

export interface QuizViewProps {
	quiz: LeituraViewModel["quiz"];
}

export function QuizView({ quiz }: QuizViewProps) {
	const { current } = quiz;
	if (!current) return null;

	return (
		<div className="mx-auto flex w-full max-w-2xl flex-col gap-6 px-5 py-10 sm:px-6 lg:px-12 xl:px-20">
			<Card className="flex flex-col gap-4">
				<div className="flex items-center justify-between gap-3">
					<div className="flex flex-col gap-0.5">
						<Typography role="body" className="font-bold text-text-primary">
							Questão {quiz.position} de {quiz.total}
						</Typography>
						<Typography role="small">
							{quiz.okCount} acertos · {quiz.failCount} erros · {quiz.accuracy} de acerto
						</Typography>
					</div>
					<Button type="button" variant="outline" size="sm" onClick={quiz.endQuiz}>
						Encerrar prática
					</Button>
				</div>
				<ProgressBar percent={quiz.progressPercent} label="Progresso da sessão" />
			</Card>

			<Card className="flex flex-col items-center gap-6 text-center">
				<div className="flex items-center gap-2">
					<Badge tone={current.category}>{CATEGORY_LABEL[current.category]}</Badge>
					{current.jlpt && <Badge tone="inverse">{current.jlpt}</Badge>}
				</div>

				<div className="relative size-54 overflow-hidden rounded-xl border border-border bg-background-subtle">
					<FittedGlyph char={current.char} fill="var(--color-text-primary)" fillRatio={0.6} />
				</div>

				{quiz.result && (
					<button
						type="button"
						onClick={() => speakJapanese(current.char)}
						aria-label="Ouvir pronúncia"
						className="flex size-11 items-center justify-center rounded-lg border border-border bg-surface"
					>
						<Volume2 className="size-5" aria-hidden="true" />
					</button>
				)}

				<Typography role="body" className="font-bold text-text-primary">
					Como se lê?
				</Typography>

				<form
					className="flex w-full flex-col items-center gap-3"
					onSubmit={(e) => {
						e.preventDefault();
						quiz.submit();
					}}
				>
					<input
						key={current.id}
						value={quiz.answer}
						onChange={(e) => quiz.setAnswer(e.target.value)}
						disabled={!!quiz.result}
						placeholder="Digite em romaji ou kana — ex.: ka"
						autoFocus
						className={cn(
							inputField(),
							"h-12 w-2/3 text-center text-lg",
							quiz.result && (quiz.result.ok ? "border-success bg-success-subtle" : "border-error bg-error-subtle"),
						)}
					/>

					{quiz.result && (
						<div className="flex flex-col gap-1">
							<Typography role="body" className={quiz.result.ok ? "text-success" : "text-text-primary"}>
								{quiz.result.ok ? "Correto!" : "Não confere."}
							</Typography>
							{quiz.answerOf && (
								<Typography role="small">
									Resposta: {quiz.answerOf.main} <span className="font-jp">({quiz.answerOf.kana})</span>
								</Typography>
							)}
						</div>
					)}

					<div className="flex w-2/3 items-center gap-3">
						{!quiz.result && (
							<button type="button" onClick={quiz.skip} className="text-sm font-bold text-text-primary">
								Pular
							</button>
						)}
						<Button type="submit" size="lg" className="flex-1" disabled={!quiz.result && !quiz.answer.trim()}>
							{quiz.result ? (quiz.isLast ? "Ver resultado" : "Próximo caractere") : "Responder"}
						</Button>
					</div>

					<Typography role="small" className="text-xs">
						Pressione Enter para responder
					</Typography>
				</form>
			</Card>
		</div>
	);
}
