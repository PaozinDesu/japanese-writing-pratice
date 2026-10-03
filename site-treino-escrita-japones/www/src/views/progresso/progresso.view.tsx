import { Flame, LogIn } from "lucide-react";
import { SAMPLE_GLYPH } from "@/models/characters.model";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { EmptyState } from "@/components/ui/empty-state";
import { LinkButton } from "@/components/ui/link-button";
import { ProgressBar } from "@/components/ui/progress-bar";
import { SegmentedControl } from "@/components/ui/segmented-control";
import { Typography } from "@/components/ui/typography";
import type { ProgressoViewModel } from "@/view-models/use-progresso-view-model";

const CATEGORY_LABEL: Record<string, string> = { hiragana: "Hiragana", katakana: "Katakana", kanji: "Kanji" };

export interface ProgressoViewProps {
	vm: ProgressoViewModel;
}

export function ProgressoView({ vm }: ProgressoViewProps) {
	if (!vm.isLoggedIn) {
		return (
			<div className="mx-auto flex w-full max-w-xl flex-col gap-6 px-5 py-16 sm:px-6">
				<EmptyState
					icon={<LogIn className="size-8 text-primary" aria-hidden="true" />}
					title="Entre para ver seu progresso"
					description="Seu histórico de prática, sequência de dias e estatísticas por caractere ficam salvos na sua conta."
					action={<LinkButton href="/login">Entrar</LinkButton>}
				/>
			</div>
		);
	}

	return (
		<div className="mx-auto flex w-full max-w-6xl flex-col gap-8 px-5 py-10 sm:px-6 lg:px-12 lg:py-12 xl:px-20">
			<div className="flex flex-wrap items-center justify-between gap-4">
				<div className="flex flex-col gap-2">
					<Typography role="h1">Progresso</Typography>
					<Typography role="body">Acompanhe sua evolução por período.</Typography>
				</div>
				<span className="flex h-11 items-center gap-2 rounded-full border border-border bg-surface px-4 text-sm font-bold">
					<Flame className="size-4 text-primary" aria-hidden="true" /> {vm.streak} {vm.streak === 1 ? "dia" : "dias"} seguidos
				</span>
			</div>

			<SegmentedControl
				aria-label="Período"
				options={vm.periods.map((p) => ({ value: p.id, label: p.label }))}
				value={vm.periods.find((p) => p.selected)!.id}
				onChange={(id) => vm.periods.find((p) => p.id === id)?.select()}
			/>

			<div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
				<Card padding="md" className="flex flex-col gap-1">
					<Typography role="caption">Praticados</Typography>
					<Typography role="h2" as="p">
						{vm.totals.practiced}
					</Typography>
				</Card>
				<Card padding="md" className="flex flex-col gap-1">
					<Typography role="caption">Acerto</Typography>
					<Typography role="h2" as="p">
						{vm.totals.accuracy}
					</Typography>
				</Card>
				<Card padding="md" className="flex flex-col gap-1">
					<Typography role="caption">Tempo</Typography>
					<Typography role="h2" as="p">
						{vm.totals.time}
					</Typography>
				</Card>
				<Card padding="md" className="flex flex-col gap-1">
					<Typography role="caption">Únicos</Typography>
					<Typography role="h2" as="p">
						{vm.totals.unique}
					</Typography>
				</Card>
			</div>

			<Card className="flex flex-col gap-4">
				<Typography role="h4">Evolução</Typography>
				<div className="flex h-32 items-end gap-1">
					{vm.series.map((point, i) => (
						<div key={i} title={point.full} className="flex flex-1 flex-col items-center justify-end gap-1">
							<div
								className={point.n ? "w-full rounded-t bg-primary" : "w-full rounded-t bg-border"}
								style={{ height: `${point.height}%` }}
							/>
							{point.label && <span className="text-xs text-text-muted">{point.label}</span>}
						</div>
					))}
				</div>
			</Card>

			<div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
				{vm.byCategory.map((c) => (
					<Card key={c.category} className="flex flex-col gap-3">
						<div className="flex items-center gap-3">
							<CharacterGlyph
								char={SAMPLE_GLYPH[c.category]}
								category={c.category}
								tile
								className="size-12 text-2xl"
							/>
							<Typography role="h4" as="span">
								{CATEGORY_LABEL[c.category]}
							</Typography>
						</div>
						<div className="flex flex-col gap-2">
							<div className="flex justify-between text-sm text-text-secondary">
								<span>
									{c.ok} de {c.total}
								</span>
								<strong>{Math.round(c.percent)}%</strong>
							</div>
							<ProgressBar percent={c.percent} label={`Progresso em ${CATEGORY_LABEL[c.category]}`} />
						</div>
					</Card>
				))}
			</div>

			<div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
				<Card className="flex flex-col gap-3">
					<Typography role="h4">Mais praticados</Typography>
					{vm.top.length ? (
						<div className="flex flex-wrap gap-2">
							{vm.top.map((t, i) => (
								<span key={i} className="font-jp flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-lg">
									{t.char} <span className="text-xs font-sans text-text-muted">{t.ok}/{t.n}</span>
								</span>
							))}
						</div>
					) : (
						<Typography role="small">Nenhuma prática neste período ainda.</Typography>
					)}
				</Card>
				<Card className="flex flex-col gap-3">
					<Typography role="h4">Mais errados</Typography>
					{vm.hard.length ? (
						<div className="flex flex-wrap gap-2">
							{vm.hard.map((t, i) => (
								<span key={i} className="font-jp flex items-center gap-2 rounded-lg border border-border px-3 py-2 text-lg">
									{t.char} <span className="text-xs font-sans text-text-muted">{t.fail} erros</span>
								</span>
							))}
						</div>
					) : (
						<Typography role="small">Nenhum erro neste período. Bom trabalho!</Typography>
					)}
				</Card>
			</div>

			<Card className="flex flex-col gap-3">
				<Typography role="h4">Sessões recentes</Typography>
				{vm.sessions.length ? (
					<div className="flex flex-col divide-y divide-border">
						{vm.sessions.map((s) => (
							<div key={s.id} className="flex items-center justify-between gap-3 py-3 text-sm">
								<div className="flex flex-col">
									<span className="font-bold">{s.label}</span>
									<span className="text-text-secondary">{s.when}</span>
								</div>
								<div className="flex flex-col items-end">
									<span>{s.n} caracteres</span>
									<span className="text-text-secondary">{s.accuracy} · {s.duration}</span>
								</div>
							</div>
						))}
					</div>
				) : (
					<Typography role="small">Nenhuma sessão neste período.</Typography>
				)}
			</Card>
		</div>
	);
}
