"use client";

import { ArrowRight, ChevronLeft, ChevronRight, Search } from "lucide-react";
import { Badge, type BadgeProps } from "@/components/ui/badge";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { EmptyState } from "@/components/ui/empty-state";
import { Skeleton } from "@/components/ui/skeleton";
import { Typography } from "@/components/ui/typography";
import { card, input, paginationItem, tab, tabs } from "@/components/ui/variants";
import { fmtInt } from "@/models/stats.model";
import { cn } from "@/utils/cn";
import type { CaracteresViewModel } from "@/view-models/use-caracteres-view-model";
import { CharacterPanel } from "./character-panel";

const CATEGORY_BADGE_TONE: Record<string, BadgeProps["tone"]> = {
	hiragana: "hiragana",
	katakana: "katakana",
	kanji: "kanji",
};

const CATEGORY_LABEL: Record<string, string> = { hiragana: "Hiragana", katakana: "Katakana", kanji: "Kanji" };

export interface CaracteresViewProps {
	vm: CaracteresViewModel;
}

export function CaracteresView({ vm }: CaracteresViewProps) {
	return (
		<div className="caracteres-shell mx-auto flex w-full flex-col gap-6 px-5 py-8 sm:px-6 lg:px-12 lg:py-10 xl:px-20">
			<div className="flex flex-wrap items-end justify-between gap-4">
				<div className="flex flex-col gap-2">
					<Typography role="h1">Caracteres</Typography>
					<Typography role="body">
						Hiragana, katakana e kanji em um só lugar — pesquise, filtre e estude cada caractere.
					</Typography>
				</div>
				<div className="flex flex-wrap items-center gap-4">
					<button
						type="button"
						onClick={() => vm.categoryTabs.find((t) => t.id === "kanji")?.select()}
						className="flex h-11 items-center gap-2 rounded-lg border border-border bg-surface px-4 text-sm font-bold text-text-primary"
					>
						<CharacterGlyph char="字" category="kanji" className="text-lg text-primary" />
						Explorar kanji por componentes
						<ArrowRight className="size-4" aria-hidden="true" />
					</button>
					<Typography role="small" as="span">
						Mostrando <strong className="font-bold text-text-primary">{fmtInt(vm.totalResults)}</strong> de{" "}
						{fmtInt(vm.grandTotal)}
					</Typography>
				</div>
			</div>

			<div className="flex flex-col gap-3 lg:flex-row lg:items-center">
				<div className="relative lg:max-w-md lg:flex-1">
					<Search className="absolute top-1/2 left-4 size-5 -translate-y-1/2 text-text-placeholder" aria-hidden="true" />
					<input
						type="search"
						value={vm.query}
						onChange={(e) => vm.setQuery(e.target.value)}
						placeholder="Caractere, romaji, leitura ou significado"
						aria-label="Buscar caracteres"
						className={cn(input(), "pl-12")}
					/>
				</div>

				<div className={cn(tabs(), "w-full overflow-x-auto lg:w-auto lg:overflow-visible")} role="tablist" aria-label="Categoria">
					{vm.categoryTabs.map((t) => (
						<button
							key={t.id}
							type="button"
							role="tab"
							aria-selected={t.selected}
							onClick={t.select}
							className={cn(tab({ active: t.selected }), "shrink-0 whitespace-nowrap")}
						>
							{t.label} <span className="text-xs font-normal text-text-muted">{fmtInt(t.count)}</span>
						</button>
					))}
				</div>
			</div>

			<div className="flex flex-wrap items-center gap-x-4 gap-y-3">
				<div className="flex flex-wrap items-center gap-2">
					<Typography role="label" as="span">
						JLPT
					</Typography>
					{vm.jlptChips.map((chip) => (
						<button
							key={chip.level}
							type="button"
							aria-pressed={chip.selected}
							onClick={chip.toggle}
							className={cn(
								"flex h-9 items-center rounded-full border px-3 text-sm font-medium",
								chip.selected ? "border-primary bg-accent-subtle text-text-primary" : "border-border bg-surface text-text-secondary",
							)}
						>
							{chip.level}
						</button>
					))}
				</div>

				<span className="hidden h-6 w-px bg-border sm:block" aria-hidden="true" />

				<div className="flex flex-wrap items-center gap-2">
					<Typography role="label" as="span">
						Nível
					</Typography>
					{vm.difficultyChips.map((chip) => (
						<button
							key={chip.id}
							type="button"
							aria-pressed={chip.selected}
							onClick={chip.toggle}
							className={cn(
								"flex h-9 items-center rounded-full border px-3 text-sm font-medium",
								chip.selected ? "border-primary bg-accent-subtle text-text-primary" : "border-border bg-surface text-text-secondary",
							)}
						>
							{chip.label}
						</button>
					))}
				</div>
			</div>

			<div className="flex flex-1 flex-col gap-6 lg:min-h-0 lg:flex-row lg:items-stretch">
				<div className="flex flex-1 flex-col gap-6 lg:min-h-0 lg:overflow-y-auto lg:pr-1">
					{vm.loading ? (
						<div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
							{Array.from({ length: 20 }, (_, i) => (
								<Skeleton key={i} className="h-40 w-full" />
							))}
						</div>
					) : vm.results.length ? (
						<>
							<div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
								{vm.results.map((c) => {
									const selected = vm.selectedCharacter?.id === c.id;
									return (
										<button
											key={c.id}
											type="button"
											onClick={() => vm.select(c.id)}
											aria-pressed={selected}
											className={cn(card({ interactive: true, padding: "sm", selected }), "flex flex-col gap-3 text-left")}
										>
											<Badge tone={CATEGORY_BADGE_TONE[c.category]} className="w-fit">
												{CATEGORY_LABEL[c.category]}
											</Badge>
											<div className="flex flex-col items-center gap-1 py-2">
												<CharacterGlyph char={c.char} category={c.category} className="text-7xl font-semibold text-text-primary" />
												<span className="text-sm text-text-secondary">{c.romaji}</span>
											</div>
											<div className="flex flex-col gap-1 border-t border-border pt-3">
												<span className="truncate text-sm font-medium text-text-primary">{c.meaning.pt.join(", ")}</span>
												<span className="truncate text-xs text-text-muted">{c.meaning.en.join(", ")}</span>
											</div>
										</button>
									);
								})}
							</div>

							{vm.totalPages > 1 && (
								<nav aria-label="Páginas" className="flex items-center justify-center gap-2">
									<button
										type="button"
										className={paginationItem()}
										disabled={vm.page <= 1}
										onClick={() => vm.setPage(vm.page - 1)}
										aria-label="Página anterior"
									>
										<ChevronLeft className="size-4" aria-hidden="true" />
									</button>
									<Typography role="small" as="span">
										Página {vm.page} de {vm.totalPages}
									</Typography>
									<button
										type="button"
										className={paginationItem()}
										disabled={vm.page >= vm.totalPages}
										onClick={() => vm.setPage(vm.page + 1)}
										aria-label="Próxima página"
									>
										<ChevronRight className="size-4" aria-hidden="true" />
									</button>
								</nav>
							)}
						</>
					) : (
						<EmptyState
							icon={<Search className="size-8 text-text-muted" aria-hidden="true" />}
							title="Nenhum caractere encontrado"
							description="Ajuste a busca ou os filtros selecionados."
						/>
					)}
				</div>

				<aside className="lg:w-md lg:min-h-0 lg:shrink-0">
					<CharacterPanel character={vm.selectedCharacter} actions={vm.panel} />
				</aside>
			</div>
		</div>
	);
}
