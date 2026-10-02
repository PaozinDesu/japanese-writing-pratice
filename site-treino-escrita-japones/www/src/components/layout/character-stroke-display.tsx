import { CharacterGlyph } from "@/components/ui/character-glyph";
import { CharacterGuideLines } from "@/components/ui/character-guide-lines";
import type { Character } from "@/models/characters.type";
import type { StrokeSvgSegment } from "@/view-models/use-stroke-svg";

export interface CharacterStrokeDisplayProps {
	character: Character;
	segments: StrokeSvgSegment[] | null;
	notFound: boolean;
}

/**
 * Anima a ordem dos traços do caractere com os SVGs da animCJK (ver models/stroke-svg.model.ts),
 * já buscados e preparados por `useStrokeSvg` (view-models/use-stroke-svg.ts) — este componente só
 * desenha o que recebe. Caracteres de dois code points (ex.: きゃ) mostram os dois SVGs lado a
 * lado, animando um depois do outro (o atraso já vem calculado em cada `segment`). Sem SVG
 * correspondente na biblioteca (não deveria acontecer com a base atual — ver
 * scripts/fetch-stroke-svgs.mjs —, mas a base pode crescer), cai no glifo estático, sem quebrar o layout.
 */
export function CharacterStrokeDisplay({ character, segments, notFound }: CharacterStrokeDisplayProps) {
	return (
		<div className="relative aspect-square w-full shrink-0 overflow-hidden rounded-xl border border-border bg-background-subtle">
			<CharacterGuideLines />
			{notFound && (
				<div className="absolute inset-0 flex items-center justify-center">
					<CharacterGlyph
						char={character.char}
						category={character.category}
						className="font-semibold text-text-primary"
						style={{ fontSize: "11rem", lineHeight: 1 }}
					/>
				</div>
			)}
			{segments && (
				<div className="absolute inset-0 flex items-stretch justify-center" style={{ padding: "15%" }}>
					{segments.map((segment, i) => (
						// markup vem do model, que só troca ids/cores num SVG confiável (animCJK, buscado do próprio domínio)
						<div key={i} className="h-full flex-1" dangerouslySetInnerHTML={{ __html: segment.markup }} />
					))}
				</div>
			)}
		</div>
	);
}
