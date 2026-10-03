import { BookOpen, Lock, Target } from "lucide-react";
import Link from "next/link";
import { PracticeModeTabs } from "@/components/layout/practice-mode-tabs";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Chip } from "@/components/ui/chip";
import { EmptyState } from "@/components/ui/empty-state";
import { LinkButton } from "@/components/ui/link-button";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { switchTrack } from "@/components/ui/variants";
import { Typography } from "@/components/ui/typography";
import { cn } from "@/utils/cn";
import { fmtInt } from "@/models/stats.model";
import type { LeituraViewModel } from "@/view-models/use-leitura-view-model";

export interface SetupViewProps {
	setup: LeituraViewModel["setup"];
}

export function SetupView({ setup }: SetupViewProps) {
	const kanjiCount = setup.categories.find((c) => c.id === "kanji")?.count ?? 0;
	const plannedCount = setup.poolCount === 0 ? 0 : Math.min(setup.size === "all" ? setup.poolCount : setup.size, setup.poolCount);

	return (
		<div className="mx-auto flex w-full flex-col gap-6 px-5 py-8 sm:px-6 lg:px-12 lg:py-10 xl:px-20">
			<PracticeModeTabs active="leitura" />

			<div className="flex flex-col gap-2">
				<Typography role="h1">Praticar — Leitura</Typography>
				<Typography role="body">
					Veja um caractere e digite como ele se lê. Todo caractere do Kaku — hiragana, katakana e os{" "}
					{fmtInt(kanjiCount)} kanji — pode entrar numa sessão.
				</Typography>
			</div>

			<div className="grid grid-cols-1 gap-6 lg:grid-cols-5 lg:items-start">
				<Card className="flex flex-col gap-6 lg:col-span-3">
					<div className="flex flex-wrap items-center justify-between gap-3">
						<Typography role="h3">Nova sessão</Typography>
						<SegmentedControl
							aria-label="Fonte dos caracteres"
							options={[
								{ value: "filters", label: "Filtros" },
								{ value: "list", label: "Minha lista" },
							]}
							value={setup.source}
							onChange={setup.setSource}
						/>
					</div>

					<div className="flex flex-col gap-3">
						<Typography role="overline">Sistema de escrita</Typography>
						{setup.source === "filters" ? (
							<div className="flex flex-wrap gap-2">
								<Chip selected={setup.noneSelected} onClick={setup.clearFilters}>
									Todos
								</Chip>
								{setup.categories.map((c) => (
									<Chip key={c.id} selected={c.selected} onClick={c.toggle}>
										{c.label} <span className={cn("text-xs", c.selected ? "text-text-inverse-muted" : "text-text-muted")}>{fmtInt(c.count)}</span>
									</Chip>
								))}
							</div>
						) : setup.lists.length ? (
							<div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
								{setup.lists.map((l) => (
									<button
										key={l.id}
										type="button"
										onClick={l.select}
										className={`flex flex-col gap-1 rounded-xl border p-4 text-left ${l.selected ? "border-primary bg-accent-subtle" : "border-border bg-surface"}`}
									>
										<span className="font-bold">{l.name}</span>
										<span className="text-sm text-text-secondary">{l.count} caracteres</span>
									</button>
								))}
							</div>
						) : (
							<EmptyState title="Você ainda não tem listas" description="Crie uma lista a partir do detalhe de um caractere." />
						)}
					</div>

					{setup.source === "filters" && (
						<div className="flex flex-col gap-3">
							<div className="flex items-baseline gap-2">
								<Typography role="overline">Nível JLPT</Typography>
								<span className="text-xs text-text-muted">
									{setup.jlptEnabled ? "· vale para os kanji" : "· selecione Todos ou Kanji para filtrar por nível"}
								</span>
							</div>
							<div className="flex flex-wrap gap-2">
								{setup.jlpt.map((j) => (
									<Chip
										key={j.level}
										selected={j.selected}
										onClick={j.toggle}
										disabled={!setup.jlptEnabled}
										aria-disabled={!setup.jlptEnabled}
									>
										{j.level} <span className={cn("text-xs", j.selected ? "text-text-inverse-muted" : "text-text-muted")}>{fmtInt(j.count)}</span>
									</Chip>
								))}
							</div>
						</div>
					)}

					<div className="rounded-xl bg-background-subtle p-4">
						<Typography role="body" className="font-bold text-text-primary">
							{setup.poolLabel}
						</Typography>
						<Typography role="small">{fmtInt(setup.poolCount)} caracteres disponíveis</Typography>
					</div>

					<div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
						<div className="flex flex-col gap-3">
							<Typography role="overline">Quantidade</Typography>
							<SegmentedControl
								aria-label="Quantidade de caracteres"
								className="self-start"
								options={[...setup.sizes.map((n) => ({ value: String(n), label: String(n) })), { value: "all", label: "Todos" }]}
								value={String(setup.size)}
								onChange={(value) => setup.setSize(value === "all" ? "all" : Number(value))}
							/>
						</div>

						<div className="flex flex-col gap-3">
							<Typography role="overline">Dificuldades</Typography>
							<div className="flex flex-col gap-1">
								<button
									type="button"
									role="switch"
									aria-checked={setup.prioritize}
									disabled={!setup.isLoggedIn}
									onClick={setup.togglePrioritize}
									className="flex h-9 items-center gap-3 disabled:opacity-50"
								>
									<span className={switchTrack({ on: setup.prioritize })}>
										<span
											className="absolute top-0.5 size-5 rounded-full bg-white transition-all"
											style={{ left: setup.prioritize ? "22px" : "2px" }}
										/>
									</span>
									<span className="text-left text-sm font-bold text-text-primary">Priorizar os que mais errei</span>
								</button>
								{!setup.isLoggedIn && <Typography role="small" className="pl-14">Disponível ao entrar na conta</Typography>}
							</div>
						</div>
					</div>

					<Button size="lg" disabled={!setup.canStart} onClick={setup.start}>
						<BookOpen className="size-4" aria-hidden="true" /> Iniciar prática · {plannedCount} caracteres
					</Button>
				</Card>

				<div className="flex flex-col gap-6 lg:col-span-2">
					{setup.isLoggedIn ? (
						<Card className="flex flex-col gap-4">
							<div className="flex items-center justify-between">
								<Typography role="h4">Minhas listas</Typography>
								<Link href="/listas" className="text-sm font-bold text-text-primary">
									Gerenciar
								</Link>
							</div>
							<div className="border-t border-border" />
							{setup.myLists.length ? (
								<div className="flex flex-col divide-y divide-border">
									{setup.myLists.map((l) => (
										<div key={l.id} className="flex items-center justify-between gap-3 py-3">
											<div className="flex flex-col">
												<span className="font-bold">{l.name}</span>
												<span className="text-sm text-text-muted">{l.count} caracteres</span>
											</div>
											<Button variant="outline" size="sm" onClick={l.practice}>
												<BookOpen className="size-4" aria-hidden="true" /> Praticar
											</Button>
										</div>
									))}
								</div>
							) : (
								<EmptyState title="Você ainda não tem listas" description="Crie uma lista a partir do detalhe de um caractere." />
							)}
						</Card>
					) : (
						<Card className="flex flex-col gap-4">
							<div className="flex items-start gap-3 rounded-xl bg-background-subtle p-4">
								<span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary-subtle text-primary">
									<Lock className="size-4" aria-hidden="true" />
								</span>
								<div className="flex flex-col gap-3">
									<div className="flex flex-col gap-1">
										<Typography role="body" className="font-bold text-text-primary">
											Salve seu progresso
										</Typography>
										<Typography role="small">
											Você pode praticar sem conta, mas o histórico, as estatísticas e as listas só ficam salvos quando
											você entra.
										</Typography>
									</div>
									<div className="flex gap-2">
										<LinkButton href="/login" variant="primary" size="sm">
											Entrar
										</LinkButton>
										<LinkButton href="/cadastro" variant="outline" size="sm">
											Criar conta
										</LinkButton>
									</div>
								</div>
							</div>
						</Card>
					)}

					<Card className="flex flex-col gap-4">
						<div className="flex items-center justify-between">
							<Typography role="h4">Para revisar</Typography>
							<span className="text-sm text-text-muted">mais erros</span>
						</div>
						{setup.hardCharacters.length ? (
							<>
								<div className="grid grid-cols-5 gap-2">
									{setup.hardCharacters.map((h, i) => (
										<div key={i} className="flex flex-col items-center gap-1 rounded-lg bg-background-subtle p-2">
											<span className="font-jp text-2xl text-text-primary">{h.char}</span>
											<span className="text-center text-xs text-text-muted">
												{h.fail} {h.fail === 1 ? "erro" : "erros"} · {h.accuracy}%
											</span>
										</div>
									))}
								</div>
								<Button variant="outline" className="w-full" onClick={setup.reviewHard}>
									<Target className="size-4" aria-hidden="true" /> Revisar estes caracteres
								</Button>
							</>
						) : (
							<Typography role="small">
								Os caracteres em que você errar aparecem aqui — e ganham prioridade nas próximas sessões.
							</Typography>
						)}
					</Card>
				</div>
			</div>
		</div>
	);
}
