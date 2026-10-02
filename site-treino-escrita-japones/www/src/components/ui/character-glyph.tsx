import type { HTMLAttributes } from "react";
import type { CharacterCategory } from "@/models/characters.type";
import { cn } from "@/utils/cn";

// O vermelho só aparece como fundo/destaque, nunca como cor de texto — por isso o tile de
// kanji usa texto preto sobre o fundo avermelhado, diferente de hiragana/katakana (azul/âmbar
// não entram nessa regra).
const TILE_CLASSES: Record<CharacterCategory, string> = {
	hiragana: "bg-hiragana-bg text-hiragana",
	katakana: "bg-katakana-bg text-katakana",
	kanji: "bg-kanji-bg text-text-primary",
};

export interface CharacterGlyphProps extends HTMLAttributes<HTMLSpanElement> {
	char: string;
	category: CharacterCategory;
	/** Fundo colorido em ladrilho (como nos cards da Início); sem isso é só o glifo, sem fundo. */
	tile?: boolean;
}

export function CharacterGlyph({ char, category, tile = false, className, ...props }: CharacterGlyphProps) {
	return (
		<span
			className={cn(
				"font-jp inline-flex items-center justify-center",
				tile && ["rounded-xl", TILE_CLASSES[category]],
				className,
			)}
			{...props}
		>
			{char}
		</span>
	);
}
