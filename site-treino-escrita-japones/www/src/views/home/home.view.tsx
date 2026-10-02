"use client";

import { ArrowRight, BarChart3, BookOpen, Grid2x2, PenLine, Volume2 } from "lucide-react";
import { readingText, SAMPLE_GLYPH } from "@/models/characters.model";
import { isKanji } from "@/models/characters.type";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { LinkButton } from "@/components/ui/link-button";
import { ProgressBar } from "@/components/ui/progress-bar";
import { Skeleton } from "@/components/ui/skeleton";
import { Typography } from "@/components/ui/typography";
import { fmtInt } from "@/models/stats.model";
import { speakJapanese } from "@/utils/speech";
import type { HomeViewModel } from "@/view-models/use-home-view-model";

const HOW_IT_WORKS = [
	{
		icon: BookOpen,
		title: "Explore",
		description: "Conheça cada caractere: leitura, romaji, significado em português e inglês e a ordem correta dos traços.",
	},
	{
		icon: PenLine,
		title: "Pratique",
		description: "Escreva no quadro com o mouse ou o dedo. Ao clicar em Pronto, o Kaku identifica o caractere e compara com o exercício.",
	},
	{
		icon: BarChart3,
		title: "Acompanhe",
		description: "Veja sua sequência de estudos, a precisão por caractere e o que vale revisar na próxima sessão.",
	},
];

export interface HomeViewProps {
	vm: HomeViewModel;
}

export function HomeView({ vm }: HomeViewProps) {
	const { heroCharacter } = vm;

	return (
		<div className="mx-auto flex w-full max-w-7xl flex-col gap-16 px-5 py-10 sm:px-6 lg:gap-24 lg:px-12 lg:py-16 xl:px-20">
			<section className="grid grid-cols-1 items-center gap-12 lg:grid-cols-[1.15fr_0.85fr]">
				<div className="flex flex-col gap-6">
					<Badge tone="error" className="w-fit">
						<span className="font-jp">書く</span> kaku · escrever
					</Badge>
					<Typography role="display" as="h1">
						Aprenda a escrever japonês, traço a traço.
					</Typography>
					<Typography role="body" className="max-w-lg text-lg">
						Explore Hiragana, Katakana e Kanji, pratique à mão livre no quadro e receba feedback imediato sobre cada
						caractere que você escreve.
					</Typography>
					<div className="flex flex-wrap gap-3">
						<LinkButton href="/praticar" size="lg">
							<PenLine className="size-5" aria-hidden="true" /> Começar a praticar
						</LinkButton>
						<LinkButton href="/caracteres" variant="outline" size="lg">
							<Grid2x2 className="size-5" aria-hidden="true" /> Explorar caracteres
						</LinkButton>
					</div>
					<div className="flex flex-wrap gap-6 pt-2">
						<div className="flex items-center gap-3">
							<CharacterGlyph char="あ" category="hiragana" className="text-3xl text-hiragana" />
							<span className="flex flex-col">
								<strong className="text-base">Hiragana</strong>
								<span className="text-sm text-text-secondary">46 básicos</span>
							</span>
						</div>
						<div className="flex items-center gap-3">
							<CharacterGlyph char="ア" category="katakana" className="text-3xl text-katakana" />
							<span className="flex flex-col">
								<strong className="text-base">Katakana</strong>
								<span className="text-sm text-text-secondary">46 básicos</span>
							</span>
						</div>
						<div className="flex items-center gap-3">
							<CharacterGlyph char="字" category="kanji" className="text-3xl text-text-primary" />
							<span className="flex flex-col">
								<strong className="text-base">Kanji</strong>
								<span className="text-sm text-text-secondary">2.136 de uso comum</span>
							</span>
						</div>
					</div>
				</div>

				<Card className="flex flex-col gap-5">
					<div className="flex items-center justify-between">
						<Typography role="overline">Caractere do dia</Typography>
						{heroCharacter && <Badge tone="kanji">Kanji</Badge>}
					</div>
					{heroCharacter ? (
						<>
							<div className="flex justify-center rounded-xl border border-border bg-background-subtle py-8">
								<CharacterGlyph char={heroCharacter.char} category={heroCharacter.category} className="text-9xl" />
							</div>
							<div className="flex items-end justify-between">
								<div className="flex flex-col gap-1">
									<span className="flex items-baseline gap-3">
										<span className="font-jp text-2xl font-semibold">{readingText(heroCharacter)}</span>
									</span>
									<span className="text-base">
										{heroCharacter.meaning.pt.join("; ")}{" "}
										<span className="text-text-secondary">· {heroCharacter.meaning.en.join("; ")}</span>
									</span>
								</div>
								<button
									type="button"
									aria-label="Ouvir pronúncia"
									onClick={() => speakJapanese(isKanji(heroCharacter) ? heroCharacter.readings.kun[0]?.kana ?? heroCharacter.readings.on[0]?.kana ?? heroCharacter.char : heroCharacter.char)}
									className="flex size-12 items-center justify-center rounded-lg border border-border bg-surface text-text-primary"
								>
									<Volume2 className="size-5" aria-hidden="true" />
								</button>
							</div>
							<button
								type="button"
								onClick={() => vm.practiceCharacterNow(heroCharacter)}
								className="flex h-12 items-center justify-center gap-3 rounded-lg bg-secondary text-base font-bold text-white"
							>
								Praticar {heroCharacter.char} agora
								<ArrowRight className="size-4" aria-hidden="true" />
							</button>
						</>
					) : (
						<Skeleton className="h-72 w-full" />
					)}
				</Card>
			</section>

			<section aria-labelledby="continue-heading" className="flex flex-col gap-6">
				<div className="flex items-end justify-between">
					<Typography role="h2" id="continue-heading">
						{vm.isLoggedIn ? "Continue de onde parou" : "Por onde começar"}
					</Typography>
					<LinkButton href="/progresso" variant="link">
						Ver progresso <ArrowRight className="size-4" aria-hidden="true" />
					</LinkButton>
				</div>
				<div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
					{vm.loading
						? Array.from({ length: 3 }, (_, i) => <Skeleton key={i} className="h-56 w-full" />)
						: vm.categories.map((c) => (
								<Card key={c.category} interactive className="flex flex-col gap-4">
									<div className="flex items-center gap-4">
										<CharacterGlyph
											char={SAMPLE_GLYPH[c.category]}
											category={c.category}
											tile
											className="size-16 text-4xl"
										/>
										<div className="flex flex-col gap-0.5">
											<span className="text-lg font-bold">{c.label}</span>
											<span className="text-sm text-text-secondary">{c.description}</span>
										</div>
									</div>
									<div className="flex flex-col gap-2">
										<div className="flex justify-between text-sm">
											<span className="text-text-secondary">
												{vm.isLoggedIn
													? `${fmtInt(c.masteredCount)} de ${fmtInt(c.total)} já acertados`
													: `${fmtInt(c.total)} caracteres`}
											</span>
											{vm.isLoggedIn && <strong>{Math.round(c.percent)}%</strong>}
										</div>
										<ProgressBar percent={vm.isLoggedIn ? c.percent : 0} label={`Progresso em ${c.label}`} />
									</div>
									<LinkButton href="/praticar" variant="link">
										Praticar {c.label} <ArrowRight className="size-4" aria-hidden="true" />
									</LinkButton>
								</Card>
							))}
				</div>
			</section>

			<section aria-labelledby="how-heading" className="flex flex-col gap-6">
				<Typography role="h2" id="how-heading">
					Como funciona
				</Typography>
				<div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
					{HOW_IT_WORKS.map((step) => (
						<Card key={step.title} className="flex flex-col gap-3">
							<span className="flex size-12 items-center justify-center rounded-lg bg-primary-subtle text-primary">
								<step.icon className="size-6" aria-hidden="true" />
							</span>
							<Typography role="h3">{step.title}</Typography>
							<Typography role="body">{step.description}</Typography>
						</Card>
					))}
				</div>
			</section>
		</div>
	);
}
