"use client";

import { Check, Eraser, Eye, EyeOff, Pencil, Undo2, Volume2, X } from "lucide-react";
import { isKanji, type CharacterCategory } from "@/models/characters.type";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { CharacterGuideLines } from "@/components/ui/character-guide-lines";
import { Chip } from "@/components/ui/chip";
import { FittedGlyph } from "@/components/ui/fitted-glyph";
import { ProgressBar } from "@/components/ui/progress-bar";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { Typography } from "@/components/ui/typography";
import { input as inputField } from "@/components/ui/variants";
import { StrokeCanvas } from "@/components/layout/stroke-canvas";
import type { PraticarViewModel } from "@/view-models/use-praticar-view-model";
import { speakJapanese } from "@/utils/speech";
import { cn } from "@/utils/cn";

const CATEGORY_LABEL: Record<CharacterCategory, string> = { hiragana: "Hiragana", katakana: "Katakana", kanji: "Kanji" };

export interface SessionViewProps {
	session: PraticarViewModel["session"];
}

export function SessionView({ session }: SessionViewProps) {
	const { current } = session;
	if (!current) return null;

	const kanji = isKanji(current);
	const scriptLabel = current.category === "hiragana" ? "hiragana" : "katakana";
	const memoryHint = kanji
		? `Escreva o kanji que significa "${current.meaning.pt[0]}".`
		: `Escreva em ${scriptLabel} o som "${current.romaji}".`;

	return (
		<div className="mx-auto flex w-full flex-col gap-6 px-5 py-8 sm:px-6 lg:px-12 lg:py-10 xl:px-20">
			<Card className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6">
				<div className="flex flex-col gap-0.5 sm:w-44 sm:shrink-0">
					<Typography role="small">{CATEGORY_LABEL[current.category]}</Typography>
					<Typography role="body" className="font-bold text-text-primary">
						{session.position} de {session.total} {session.total === 1 ? "caractere" : "caracteres"}
					</Typography>
				</div>

				<div className="flex-1">
					<ProgressBar percent={session.progressPercent} label="Progresso da sessão" />
				</div>

				<div className="flex items-center gap-2 sm:shrink-0">
					<Badge tone="success" className="gap-1">
						<Check className="size-3.5" aria-hidden="true" /> {session.okCount}
					</Badge>
					<Badge tone="error" className="gap-1">
						<X className="size-3.5" aria-hidden="true" /> {session.failCount}
					</Badge>
					<Button type="button" variant="outline" size="sm" onClick={session.endSession}>
						Encerrar sessão
					</Button>
				</div>
			</Card>

			<div className="grid grid-cols-1 items-start gap-6 lg:grid-cols-36">
				{/* Caractere pedido */}
				<Card className="flex flex-col gap-4 lg:col-span-10">
					<div className="flex items-center justify-between">
						<Badge tone={current.category}>{CATEGORY_LABEL[current.category]}</Badge>
						<Button
							type="button"
							variant="outline"
							size="icon"
							aria-label="Ouvir pronúncia"
							onClick={() =>
								speakJapanese(kanji ? (current.readings.kun[0]?.kana ?? current.readings.on[0]?.kana ?? current.char) : current.char)
							}
						>
							<Volume2 className="size-5" aria-hidden="true" />
						</Button>
					</div>

					<Typography role="small">{session.showCharacter ? "Escreva este caractere no quadro:" : memoryHint}</Typography>

					<div className="relative aspect-3/2 w-full overflow-hidden rounded-xl bg-background-subtle">
						{session.showCharacter && <FittedGlyph char={current.char} fill="var(--color-text-primary)" fillRatio={0.65} aspect={1.5} />}
					</div>

					<div className="flex items-center justify-between gap-2">
						<Typography role="small">
							{current.strokes} {current.strokes === 1 ? "traço" : "traços"}
						</Typography>
						<Button type="button" variant="outline" size="sm" onClick={session.toggleShowCharacter}>
							{session.showCharacter ? <EyeOff className="size-4" aria-hidden="true" /> : <Eye className="size-4" aria-hidden="true" />}
							{session.showCharacter ? "Ocultar caractere" : "Mostrar caractere"}
						</Button>
					</div>

					<div className="border-t border-border" />

					<div className="flex flex-col gap-2">
						<Typography role="overline">Som (romaji)</Typography>
						{session.readingResult && (
							<Typography role="small" className="font-bold text-text-primary">
								{current.char}・{session.correctRomaji}
							</Typography>
						)}
						<div className="flex gap-2">
							<input
								value={session.readingAnswer}
								onChange={(e) => session.setReadingAnswer(e.target.value)}
								onKeyDown={(e) => e.key === "Enter" && session.checkReading()}
								placeholder="romaji"
								className={cn(inputField(), "h-10 flex-1 text-sm")}
							/>
							<Button type="button" variant="outline" onClick={session.checkReading}>
								Verificar
							</Button>
						</div>
						{session.readingResult === "ok" && (
							<Badge tone="success" className="w-fit gap-1">
								<Check className="size-3.5" aria-hidden="true" /> Certo
							</Badge>
						)}
						{session.readingResult === "no" && (
							<Badge tone="error" className="w-fit gap-1">
								<X className="size-3.5" aria-hidden="true" /> Errado
							</Badge>
						)}
					</div>

					{kanji && (
						<div className="flex flex-col gap-2">
							<Typography role="overline">Significado</Typography>
							{session.meaningResult && (
								<Typography role="small" className="font-bold text-text-primary">
									{current.meaning.pt.join("; ")}
								</Typography>
							)}
							<div className="flex gap-2">
								<input
									value={session.meaningAnswer}
									onChange={(e) => session.setMeaningAnswer(e.target.value)}
									onKeyDown={(e) => e.key === "Enter" && session.checkMeaning()}
									placeholder="ex.: montanha"
									className={cn(inputField(), "h-10 flex-1 text-sm")}
								/>
								<Button type="button" variant="outline" onClick={session.checkMeaning}>
									Verificar
								</Button>
							</div>
							{session.meaningResult === "ok" && (
								<Badge tone="success" className="w-fit gap-1">
									<Check className="size-3.5" aria-hidden="true" /> Certo
								</Badge>
							)}
							{session.meaningResult === "no" && (
								<Badge tone="error" className="w-fit gap-1">
									<X className="size-3.5" aria-hidden="true" /> Errado
								</Badge>
							)}
						</div>
					)}
				</Card>

				{/* Área de escrita */}
				<Card className="flex flex-col gap-4 lg:col-span-16">
					<div className="flex flex-wrap items-center justify-between gap-3">
						<div className="flex items-center gap-2">
							<Typography role="h4" as="p">
								Área de escrita
							</Typography>
							<span className="rounded-full bg-background-subtle px-3 py-1 text-xs font-bold text-text-secondary">
								Traços: {session.strokeCount} / {current.strokes}
							</span>
						</div>
						<div className="flex gap-2">
							<Chip selected={session.guide} onClick={session.toggleGuide}>
								Grade
							</Chip>
							<Chip selected={session.ghost} onClick={session.toggleGhost}>
								Contorno
							</Chip>
						</div>
					</div>

					<div className="relative aspect-square w-full overflow-hidden">
						{session.guide && <CharacterGuideLines diagonals />}
						{session.ghost && session.showCharacter && (
							<FittedGlyph char={current.char} fill="var(--color-primary)" opacity={0.15} fillRatio={0.8} />
						)}
						<StrokeCanvas
							controller={session.ink}
							onStrokeEnd={session.onStrokeEnd}
							disabled={!!session.result || session.busy}
							className={cn("absolute inset-0 border border-border", session.warn > 0 && "animate-pulse")}
						/>
						{session.strokeCount === 0 && (
							<Typography role="small" className="pointer-events-none absolute inset-x-0 bottom-3 text-center text-text-muted">
								Escreva aqui com o mouse ou o dedo
							</Typography>
						)}
					</div>

					<div className="flex items-center justify-between gap-3">
						<div className="flex gap-2">
							<Button type="button" variant="outline" size="icon" aria-label="Desfazer" onClick={session.undo}>
								<Undo2 className="size-4" aria-hidden="true" />
							</Button>
							<Button type="button" variant="outline" onClick={session.clear}>
								<Eraser className="size-4" aria-hidden="true" /> Limpar
							</Button>
						</div>
						{!session.result && (
							<Button onClick={session.submitDrawing} isLoading={session.busy}>
								<Check className="size-4" aria-hidden="true" /> Pronto
							</Button>
						)}
					</div>
				</Card>

				{/* Resultado */}
				<Card className="flex flex-col gap-4 lg:col-span-10">
					<Typography role="h3" as="p">
						Resultado
					</Typography>

					{!session.result ? (
						<div className="flex flex-col items-center gap-3 py-2 text-center">
							<span className="flex size-16 items-center justify-center rounded-full bg-background-subtle text-text-secondary">
								<Pencil className="size-7" aria-hidden="true" />
							</span>
							<Typography role="body" className="font-bold text-text-primary">
								Escreva o caractere e clique em <strong>Pronto</strong>
							</Typography>
							<Typography role="small">O Kaku compara seu desenho com o caractere e mostra o que reconheceu.</Typography>

							<div className="w-full rounded-xl bg-background-subtle p-4 text-left">
								<Typography role="overline">Dicas</Typography>
								<ol className="mt-2 flex flex-col gap-2 text-sm text-text-secondary">
									<li className="flex gap-2">
										<span className="font-bold text-text-primary">1</span> De cima para baixo, da esquerda para a direita.
									</li>
									<li className="flex gap-2">
										<span className="font-bold text-text-primary">2</span> Use o número de traços indicado.
									</li>
									<li className="flex gap-2">
										<span className="font-bold text-text-primary">3</span> &ldquo;Contorno&rdquo; mostra o caractere por baixo do quadro.
									</li>
								</ol>
							</div>
						</div>
					) : (
						<div className="flex flex-col gap-5">
							{/* Banner de status */}
							<div
								className={cn(
									"flex items-start gap-3 rounded-xl border p-4",
									session.finalOk ? "border-success-border bg-success-subtle" : "border-error-border bg-error-subtle",
								)}
							>
								<span
									className={cn(
										"flex size-8 shrink-0 items-center justify-center rounded-full text-white",
										session.finalOk ? "bg-success-solid" : "bg-error-solid",
									)}
								>
									{session.finalOk ? <Check className="size-5" aria-hidden="true" /> : <X className="size-5" aria-hidden="true" />}
								</span>
								<div className="flex flex-col gap-0.5">
									<Typography role="body" className={cn("font-bold", session.finalOk ? "text-success" : "text-text-primary")}>
										{session.finalOk ? "Correto!" : "Não corresponde"}
									</Typography>
									<Typography role="small">
										{session.finalOk
											? "Seu desenho corresponde ao caractere pedido."
											: "Seu desenho não corresponde ao caractere pedido."}
									</Typography>
								</div>
							</div>

							{/* Caractere identificado */}
							<div className="flex flex-col gap-2">
								<Typography role="overline">Caractere identificado</Typography>
								{session.identified ? (
									<div className="flex items-center gap-3">
										<div className="relative size-16 shrink-0 overflow-hidden rounded-lg bg-background-subtle">
											<FittedGlyph char={session.identified.char} fill="var(--color-text-primary)" fillRatio={0.7} />
										</div>
										<div className="flex flex-col">
											<Typography role="body" className="font-bold text-text-primary">
												{session.identified.char}・{session.identifiedRomaji}
											</Typography>
											<Typography role="small">{session.identifiedRomaji}</Typography>
											<Typography role="small">{session.identified.meaning.pt[0]}</Typography>
										</div>
									</div>
								) : (
									<Typography role="small">Nenhum caractere reconhecido</Typography>
								)}
							</div>

							{/* Comparação lado a lado */}
							<div className="grid grid-cols-2 gap-4">
								<div className="flex flex-col items-center gap-2">
									<div className="relative aspect-square w-full overflow-hidden rounded-xl border border-border">
										<CharacterGuideLines />
										{session.result.img && (
											// eslint-disable-next-line @next/next/no-img-element -- data URL do canvas, não um asset otimizável pelo next/image
											<img
												src={session.result.img}
												alt="Seu desenho"
												className="absolute inset-0 h-full w-full object-contain"
											/>
										)}
									</div>
									<Typography role="small">Seu desenho</Typography>
								</div>
								<div className="flex flex-col items-center gap-2">
									<div className="relative aspect-square w-full overflow-hidden rounded-xl border border-border">
										<CharacterGuideLines />
										<FittedGlyph char={current.char} fill="var(--color-text-primary)" fillRatio={0.7} />
									</div>
									<Typography role="small">Modelo・{current.char}</Typography>
								</div>
							</div>

							{/* Métricas */}
							<div className="flex flex-col gap-3">
								<div className="flex flex-col gap-1.5">
									<div className="flex items-center justify-between">
										<Typography role="small">Semelhança da forma</Typography>
										<span className="text-sm font-bold text-text-primary">{session.result.sim}%</span>
									</div>
									<ProgressBar
										percent={session.result.sim}
										tone={session.finalOk ? "success" : "error"}
										label="Semelhança da forma"
									/>
								</div>

								<div className="flex items-center justify-between">
									<Typography role="small">Número de traços</Typography>
									<span className="text-sm font-bold text-text-primary">
										{session.result.user} / {session.result.exp}
									</span>
								</div>
								{session.result.user !== session.result.exp && (
									<Typography role="small">
										Você usou {Math.abs(session.result.user - session.result.exp)}{" "}
										{Math.abs(session.result.user - session.result.exp) === 1 ? "traço" : "traços"} a{" "}
										{session.result.user > session.result.exp ? "mais" : "menos"}
									</Typography>
								)}
							</div>

							{/* Resultado deste caractere */}
							<div className="flex flex-col gap-3 rounded-xl border border-border p-4">
								<div className="flex items-center justify-between gap-3">
									<Typography role="body" className="font-bold text-text-primary">
										Resultado deste caractere
									</Typography>
									<Badge tone={session.finalOk ? "success" : "error"}>{session.finalOk ? "Acerto" : "Erro"}</Badge>
								</div>
								<Typography role="small">
									{session.overrideValue == null ? "Desenho reconhecido." : "Marcado manualmente."}
								</Typography>
								<div className="flex items-center justify-between gap-3">
									<Typography role="small" className="font-bold text-text-primary">
										Contar como
									</Typography>
									<SegmentedControl
										aria-label="Contar este caractere como"
										options={[
											{ value: "acerto", label: "Acerto" },
											{ value: "erro", label: "Erro" },
										]}
										value={session.finalOk ? "acerto" : "erro"}
										onChange={(value) => session.override(value === "acerto")}
									/>
								</div>
							</div>

							<Button size="lg" className="w-full" onClick={session.next}>
								{session.isLast ? "Ver resumo" : "Próximo"}
							</Button>
						</div>
					)}

					{session.upNext.length > 0 && (
						<div className="flex flex-col gap-2">
							<Typography role="overline">A seguir</Typography>
							<div className="flex flex-wrap gap-2">
								{session.upNext.map((c) => (
									<span key={c.id} className="flex size-10 items-center justify-center rounded-lg border border-border">
										<CharacterGlyph char={c.char} category={c.category} className="text-lg text-text-primary" />
									</span>
								))}
							</div>
						</div>
					)}

					{!session.saved && <Alert tone="warning">Você está praticando sem conta: o resultado não será salvo no seu histórico.</Alert>}
				</Card>
			</div>
		</div>
	);
}
