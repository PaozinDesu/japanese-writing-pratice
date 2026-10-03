"use client";

import { ListPlus, Plus } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { dropdown, menuItem } from "@/components/ui/variants";
import { cn } from "@/utils/cn";
import type { CharacterActions } from "@/view-models/use-character-actions";

export interface AddToListMenuProps {
	vm: CharacterActions;
}

/** Porte de `listPickerVals` (source/js/account.js): adicionar/remover o caractere das listas do usuário. */
export function AddToListMenu({ vm }: AddToListMenuProps) {
	const [open, setOpen] = useState(false);

	if (!vm.isLoggedIn) {
		return (
			<Button variant="outline" onClick={vm.goToLogin}>
				<ListPlus className="size-4" aria-hidden="true" /> Entrar para adicionar à lista
			</Button>
		);
	}

	return (
		<div className="relative">
			<Button variant="outline" onClick={() => setOpen((v) => !v)} aria-haspopup="menu" aria-expanded={open}>
				<ListPlus className="size-4" aria-hidden="true" />
				{vm.inCount ? `Em ${vm.inCount} ${vm.inCount === 1 ? "lista" : "listas"}` : "Adicionar à lista de prática"}
			</Button>
			{open && (
				<>
					<button
						type="button"
						aria-label="Fechar menu de listas"
						className="fixed inset-0 z-40"
						onClick={() => setOpen(false)}
					/>
					<div className={cn(dropdown(), "absolute top-full left-0 z-50 mt-2 w-72")} role="menu">
						{vm.lists.length ? (
							<div className="flex flex-col gap-1 pb-2">
								{vm.lists.map((l) => (
									<button
										key={l.id}
										type="button"
										role="menuitemcheckbox"
										aria-checked={l.has}
										className={menuItem({ active: l.has })}
										onClick={l.toggle}
									>
										{l.name} <span className="ml-auto text-xs text-text-muted">{l.count}</span>
									</button>
								))}
							</div>
						) : (
							<p className="px-3 py-2 text-sm text-text-muted">Você ainda não tem listas.</p>
						)}
						<form onSubmit={vm.createList} className="flex gap-2 border-t border-border p-2">
							<input
								value={vm.newListName}
								onChange={(e) => vm.setNewListName(e.target.value)}
								placeholder="Nova lista"
								aria-label="Nome da nova lista"
								className="h-9 flex-1 rounded-lg border border-border-strong px-3 text-sm"
							/>
							<button
								type="submit"
								aria-label="Criar lista"
								className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-secondary text-white"
							>
								<Plus className="size-4" aria-hidden="true" />
							</button>
						</form>
						{vm.feedbackError && <p className="px-3 pb-2 text-xs font-bold text-text-primary">{vm.feedbackError}</p>}
						{vm.feedback && <p className="px-3 pb-2 text-xs text-success">{vm.feedback}</p>}
					</div>
				</>
			)}
		</div>
	);
}
