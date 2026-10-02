import { BookOpen, PenLine } from "lucide-react";
import Link from "next/link";
import { tab, tabs } from "@/components/ui/variants";
import { cn } from "@/utils/cn";

export interface PracticeModeTabsProps {
	active: "escrita" | "leitura";
	className?: string;
}

/** Alterna entre /praticar (escrita) e /leitura — os dois telas linkam uma pra outra no handoff. */
export function PracticeModeTabs({ active, className }: PracticeModeTabsProps) {
	return (
		<div className={cn(tabs(), "self-start", className)} role="tablist" aria-label="Modo de prática">
			<Link
				href="/praticar"
				role="tab"
				aria-selected={active === "escrita"}
				className={cn(tab({ active: active === "escrita" }), "inline-flex items-center gap-1.5")}
			>
				<PenLine className="size-4" aria-hidden="true" /> Escrita
			</Link>
			<Link
				href="/leitura"
				role="tab"
				aria-selected={active === "leitura"}
				className={cn(tab({ active: active === "leitura" }), "inline-flex items-center gap-1.5")}
			>
				<BookOpen className="size-4" aria-hidden="true" /> Leitura
			</Link>
		</div>
	);
}
