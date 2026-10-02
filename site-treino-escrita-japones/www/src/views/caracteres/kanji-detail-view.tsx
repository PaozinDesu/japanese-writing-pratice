import { PenLine } from "lucide-react";
import { AddToListMenu } from "@/components/layout/add-to-list-menu";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { Typography } from "@/components/ui/typography";
import type { KanjiCharacter } from "@/models/characters.type";
import type { CharacterActions } from "@/view-models/use-character-actions";

const FORMATION_ROLE_LABEL: Record<"semantico" | "fonetico", string> = {
	semantico: "significado",
	fonetico: "som",
};

export interface KanjiDetailViewProps {
	character: KanjiCharacter;
	vm: CharacterActions;
}

export function KanjiDetailView({ character, vm }: KanjiDetailViewProps) {
	return (
		<div className="flex flex-col gap-8">
			<div className="grid grid-cols-1 gap-6 lg:grid-cols-[auto_1fr]">
				<div className="flex justify-center rounded-xl border border-border bg-background-subtle p-10">
					<CharacterGlyph char={character.char} category="kanji" className="text-9xl" />
				</div>
				<div className="flex flex-col gap-4">
					<div className="flex flex-wrap items-center gap-2">
						{character.jlpt && <Badge tone="kanji">{character.jlpt}</Badge>}
						{character.gradeLabel && <Badge tone="neutral">{character.gradeLabel}</Badge>}
						<Badge tone="neutral">{character.strokes} traços</Badge>
					</div>
					<Typography role="h1" as="h1">
						{character.meaning.pt.join("; ")}
					</Typography>
					<Typography role="body">{character.meaning.en.join("; ")}</Typography>

					<div className="flex flex-col gap-2 sm:flex-row sm:gap-8">
						{character.readings.on.length > 0 && (
							<div>
								<Typography role="caption" as="span">
									ON&apos;YOMI
								</Typography>
								<p className="font-jp text-lg">{character.readings.on.map((r) => r.kana).join("、")}</p>
							</div>
						)}
						{character.readings.kun.length > 0 && (
							<div>
								<Typography role="caption" as="span">
									KUN&apos;YOMI
								</Typography>
								<p className="font-jp text-lg">{character.readings.kun.map((r) => r.display).join("、")}</p>
							</div>
						)}
					</div>

					<div className="flex flex-wrap gap-3">
						<Button onClick={vm.practiceThis}>
							<PenLine className="size-4" aria-hidden="true" /> Praticar este caractere
						</Button>
						<AddToListMenu vm={vm} />
					</div>
				</div>
			</div>

			<div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
				<Card className="flex flex-col gap-3">
					<Typography role="h4">Radical</Typography>
					<div className="flex items-center gap-4">
						<CharacterGlyph char={character.radical.char} category="kanji" tile className="size-14 text-3xl" />
						<div className="flex flex-col">
							<span className="font-bold">{Object.values(character.radical.meaning)[0]}</span>
							<span className="text-sm text-text-secondary">Radical Kangxi nº {character.radical.number}</span>
						</div>
					</div>
				</Card>

				{character.formation && (
					<Card className="flex flex-col gap-3">
						<Typography role="h4">{character.formation.label}</Typography>
						<Typography role="small">{character.formation.description}</Typography>
						{character.formation.parts && character.formation.parts.length > 0 && (
							<div className="flex flex-wrap gap-2">
								{character.formation.parts.map((part) => (
									<span
										key={part.c + part.role}
										className="flex items-center gap-2 rounded-lg border border-border px-2 py-1 text-sm"
									>
										<span className="font-jp text-lg">{part.c}</span>
										{part.meaning ?? part.reading} · {FORMATION_ROLE_LABEL[part.role]}
									</span>
								))}
							</div>
						)}
					</Card>
				)}
			</div>

			{character.decomposition.length > 0 && (
				<section className="flex flex-col gap-4">
					<Typography role="h3">Composição</Typography>
					<div className="flex flex-wrap gap-3">
						{character.decomposition.map((part) => (
							<span
								key={part.c}
								className="flex items-center gap-3 rounded-xl border border-border bg-surface px-3 py-2"
							>
								<span className="font-jp text-2xl">{part.c}</span>
								<span className="text-sm text-text-secondary">{part.meaning}</span>
							</span>
						))}
					</div>
				</section>
			)}

			{character.sentence && (
				<Card className="flex flex-col gap-1">
					<span className="font-jp text-lg">{character.sentence.ja}</span>
					<span className="text-sm">{character.sentence.pt}</span>
					<span className="text-sm text-text-secondary">{character.sentence.en}</span>
				</Card>
			)}

			{character.examples.length > 0 && (
				<section className="flex flex-col gap-4">
					<Typography role="h3">Exemplos</Typography>
					<div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
						{character.examples.map((example) => (
							<Card key={example.word} padding="md" className="flex flex-col gap-1">
								<span className="font-jp text-xl">{example.word}</span>
								<span className="text-sm text-text-secondary">
									{example.reading} · {example.romaji}
								</span>
								<span className="text-sm">
									{example.pt} <span className="text-text-secondary">· {example.en}</span>
								</span>
							</Card>
						))}
					</div>
				</section>
			)}

			{character.related.length > 0 && (
				<section className="flex flex-col gap-4">
					<Typography role="h3">Kanji relacionados</Typography>
					<div className="flex flex-wrap gap-2">
						{character.related.slice(0, 12).map((relatedId) => (
							<button
								key={relatedId}
								type="button"
								onClick={() => vm.goToCharacter(relatedId)}
								className="font-jp flex size-12 items-center justify-center rounded-lg border border-border bg-surface text-xl"
							>
								{relatedId.split(":")[1]}
							</button>
						))}
					</div>
				</section>
			)}
		</div>
	);
}
