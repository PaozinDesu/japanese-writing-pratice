"use client";

import { BarChart3, ChevronDown, Flame, Home, LayoutGrid, ListChecks, LogOut, PenLine, User } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { LinkButton } from "@/components/ui/link-button";
import { useSession } from "@/view-models/use-session";
import { bottomNav, dropdown, menuItem, navLink, navbar } from "@/components/ui/variants";
import { cn } from "@/utils/cn";

const NAV_ITEMS = [
	{ href: "/", label: "Início", icon: Home },
	{ href: "/caracteres", label: "Caracteres", icon: LayoutGrid },
	{ href: "/praticar", label: "Praticar", icon: PenLine },
	{ href: "/progresso", label: "Progresso", icon: BarChart3 },
] as const;

function Logo() {
	return (
		<Link href="/" aria-label="Kaku, página inicial" className="flex items-center gap-3 text-text-primary">
			<span className="font-jp flex size-9 items-center justify-center rounded-lg bg-primary text-lg font-semibold text-white">
				書
			</span>
			<span className="font-serif text-xl font-bold tracking-wide">Kaku</span>
		</Link>
	);
}

function AccountMenu() {
	const { firstName, initials, streak, logout } = useSession();
	const [open, setOpen] = useState(false);

	return (
		<div className="relative flex items-center justify-self-end gap-3">
			<span
				title="Dias seguidos com prática"
				className="flex h-10 items-center gap-2 rounded-full border border-border bg-surface px-3 text-sm font-bold text-text-primary"
			>
				<Flame className="size-4 text-primary" aria-hidden="true" />
				{streak} {streak === 1 ? "dia" : "dias"}
			</span>
			<button
				type="button"
				aria-haspopup="menu"
				aria-expanded={open}
				onClick={() => setOpen((v) => !v)}
				className="flex h-11 items-center gap-2 rounded-lg border border-border bg-surface py-0 pr-3 pl-1 text-sm font-medium text-text-primary"
			>
				<span className="flex size-9 items-center justify-center rounded-full bg-primary text-sm font-bold text-white">
					{initials}
				</span>
				{firstName}
				<ChevronDown className="size-4 text-text-secondary" aria-hidden="true" />
			</button>
			{open && (
				<>
					<button
						type="button"
						aria-label="Fechar menu"
						className="fixed inset-0 z-40 cursor-default"
						onClick={() => setOpen(false)}
					/>
					<div className={cn(dropdown(), "absolute top-full right-0 z-50 mt-2")} role="menu">
						<Link href="/perfil" className={menuItem()} role="menuitem" onClick={() => setOpen(false)}>
							<User className="size-4" aria-hidden="true" /> Perfil
						</Link>
						<Link href="/listas" className={menuItem()} role="menuitem" onClick={() => setOpen(false)}>
							<ListChecks className="size-4" aria-hidden="true" /> Minhas listas
						</Link>
						<button
							type="button"
							className={menuItem()}
							role="menuitem"
							onClick={() => {
								setOpen(false);
								logout();
							}}
						>
							<LogOut className="size-4 text-primary" aria-hidden="true" /> Sair
						</button>
					</div>
				</>
			)}
		</div>
	);
}

export function Header() {
	const pathname = usePathname();
	const { isLoggedIn, initials } = useSession();

	return (
		<>
			{/* Desktop: navbar completa com pílulas de navegação e conta */}
			<header className={cn(navbar(), "hidden md:grid")}>
				<Logo />
				<nav aria-label="Principal" className="flex items-center gap-1 rounded-full bg-border p-1">
					{NAV_ITEMS.map((item) => (
						<Link
							key={item.href}
							href={item.href}
							aria-current={pathname === item.href ? "page" : undefined}
							className={navLink({ active: pathname === item.href })}
						>
							{item.label}
						</Link>
					))}
				</nav>
				{isLoggedIn ? (
					<AccountMenu />
				) : (
					<div className="flex items-center justify-self-end gap-3">
						<LinkButton href="/login" variant="outline" size="md">
							<User className="size-4" aria-hidden="true" /> Entrar
						</LinkButton>
						<LinkButton href="/cadastro" variant="primary" size="md">
							Criar conta
						</LinkButton>
					</div>
				)}
			</header>

			{/* Mobile: barra superior simples + barra inferior com os mesmos 4 destinos */}
			<header className="flex h-16 items-center justify-between px-5 md:hidden">
				<Link href="/" className="font-serif text-2xl font-bold text-text-primary">
					Kaku
				</Link>
				{isLoggedIn ? (
					<Link
						href="/perfil"
						aria-label="Meu perfil"
						className="flex h-10 items-center gap-2 rounded-full border border-border bg-surface py-0 pr-1 pl-3 text-sm font-bold text-text-primary"
					>
						<span className="flex size-8 items-center justify-center rounded-full bg-primary text-xs font-bold text-white">
							{initials}
						</span>
					</Link>
				) : (
					<LinkButton href="/login" variant="outline" size="sm">
						<User className="size-4" aria-hidden="true" /> Entrar
					</LinkButton>
				)}
			</header>
			<nav aria-label="Principal" className={bottomNav()}>
				{NAV_ITEMS.map((item) => {
					const Icon = item.icon;
					const active = pathname === item.href;
					return (
						<Link
							key={item.href}
							href={item.href}
							aria-current={active ? "page" : undefined}
							className={cn(
								"flex flex-1 flex-col items-center justify-center gap-1 text-xs",
								active ? "font-bold" : "font-medium text-text-muted",
							)}
						>
							{/* Item ativo em vermelho — a única exceção da regra "vermelho nunca é cor de texto". */}
							<Icon className={cn("size-5", active && "text-primary")} aria-hidden="true" />
							<span className={active ? "text-primary" : undefined}>{item.label}</span>
						</Link>
					);
				})}
			</nav>
		</>
	);
}
