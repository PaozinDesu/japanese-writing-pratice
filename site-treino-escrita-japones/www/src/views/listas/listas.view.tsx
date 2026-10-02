"use client";

import { AlertCircle, ChevronDown, LogIn, PenLine, Plus, Trash2, X } from "lucide-react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { EmptyState } from "@/components/ui/empty-state";
import { LinkButton } from "@/components/ui/link-button";
import { Typography } from "@/components/ui/typography";
import { cn } from "@/utils/cn";
import type { ListasViewModel } from "@/view-models/use-listas-view-model";

export interface ListasViewProps {
	vm: ListasViewModel;
}

export function ListasView({ vm }: ListasViewProps) {
	if (!vm.isLoggedIn) {
		return (
			<div className="mx-auto flex w-full max-w-xl flex-col gap-6 px-5 py-16 sm:px-6">
				<EmptyState
					icon={<LogIn className="size-8 text-primary" aria-hidden="true" />}
					title="Entre para ver suas listas"
					description="Monte listas de estudo com os caracteres que quiser e pratique por lista."
					action={<LinkButton href="/login">Entrar</LinkButton>}
				/>
			</div>
		);
	}

	return (
		<div className="mx-auto flex w-full max-w-3xl flex-col gap-8 px-5 py-10 sm:px-6 lg:px-12 lg:py-12 xl:px-20">
			<div className="flex flex-col gap-2">
				<Typography role="h1">Minhas listas</Typography>
				<Typography role="body">Organize caracteres em listas e pratique por lista.</Typography>
			</div>

			<form onSubmit={vm.createList} className="flex gap-2">
				<input
					value={vm.newName}
					onChange={(e) => vm.setNewName(e.target.value)}
					placeholder="Nome da nova lista"
					aria-label="Nome da nova lista"
					className="h-11 flex-1 rounded-lg border border-border-strong px-4"
				/>
				<Button type="submit">
					<Plus className="size-4" aria-hidden="true" /> Criar lista
				</Button>
			</form>
			{vm.error && (
				<Typography role="small" className="flex items-center gap-1.5 font-bold text-text-primary">
					<AlertCircle className="size-4 shrink-0 text-primary" aria-hidden="true" /> {vm.error}
				</Typography>
			)}

			{vm.lists.length === 0 ? (
				<EmptyState title="Nenhuma lista ainda" description='Adicione caracteres a uma lista pelo botão "Adicionar à lista" no detalhe de cada caractere.' />
			) : (
				<div className="flex flex-col gap-3">
					{vm.lists.map((l) => (
						<Card key={l.id} padding="none" className="flex flex-col">
							<div className="flex items-center gap-3 p-4">
								<button type="button" onClick={l.toggle} className="flex flex-1 items-center gap-2 text-left">
									<ChevronDown className={cn("size-4 transition-transform", !l.open && "-rotate-90")} aria-hidden="true" />
									{l.isRenaming ? (
										<form onSubmit={vm.confirmRename} className="flex flex-1 gap-2" onClick={(e) => e.stopPropagation()}>
											<input
												value={vm.renameValue}
												onChange={(e) => vm.setRenameValue(e.target.value)}
												autoFocus
												className="h-9 flex-1 rounded-lg border border-border-strong px-3"
											/>
											<Button type="submit" size="sm">
												Salvar
											</Button>
										</form>
									) : (
										<div className="flex flex-col">
											<span className="font-bold">{l.name}</span>
											<span className="text-sm text-text-secondary">{l.count} caracteres</span>
										</div>
									)}
								</button>
								{!l.isRenaming && (
									<div className="flex items-center gap-1">
										<Button variant="outline" size="sm" disabled={!l.count} onClick={l.practice}>
											<PenLine className="size-4" aria-hidden="true" /> Praticar
										</Button>
										<button
											type="button"
											onClick={l.startRename}
											aria-label={`Renomear ${l.name}`}
											className="flex size-9 items-center justify-center rounded-lg text-text-secondary hover:bg-surface-muted"
										>
											<PenLine className="size-4" aria-hidden="true" />
										</button>
										<button
											type="button"
											onClick={l.remove}
											aria-label={`Excluir ${l.name}`}
											className="flex size-9 items-center justify-center rounded-lg text-error hover:bg-error-subtle"
										>
											<Trash2 className="size-4" aria-hidden="true" />
										</button>
									</div>
								)}
							</div>

							{l.open && (
								<div className="flex flex-wrap gap-2 border-t border-border p-4">
									{l.characters.length ? (
										l.characters.map(
											(c) =>
												c && (
													<span
														key={c.id}
														className="flex items-center gap-2 rounded-lg border border-border bg-surface py-1 pr-1 pl-2"
													>
														<Link href={`/caracteres/${encodeURIComponent(c.id)}`} className="flex items-center gap-2">
															<CharacterGlyph char={c.char} category={c.category} className="text-lg" />
															<span className="text-sm text-text-secondary">{c.romaji}</span>
														</Link>
														<button
															type="button"
															onClick={() => l.removeChar(c.id)}
															aria-label={`Remover ${c.char} da lista`}
															className="flex size-6 items-center justify-center rounded-full text-text-muted hover:bg-surface-muted"
														>
															<X className="size-3.5" aria-hidden="true" />
														</button>
													</span>
												),
										)
									) : (
										<Typography role="small">
											Lista vazia. Adicione caracteres pelo botão &quot;Adicionar à lista&quot; no detalhe de cada
											caractere.
										</Typography>
									)}
								</div>
							)}
						</Card>
					))}
				</div>
			)}
		</div>
	);
}
