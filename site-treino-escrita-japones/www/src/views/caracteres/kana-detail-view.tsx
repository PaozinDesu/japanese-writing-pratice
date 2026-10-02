import { PenLine } from "lucide-react";
import { AddToListMenu } from "@/components/layout/add-to-list-menu";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CharacterGlyph } from "@/components/ui/character-glyph";
import { Typography } from "@/components/ui/typography";
import { GROUP_LABEL } from "@/models/characters.model";
import type { KanaCharacter } from "@/models/characters.type";
import type { CharacterActions } from "@/view-models/use-character-actions";

export interface KanaDetailViewProps {
	character: KanaCharacter;
	vm: CharacterActions;
}

export function KanaDetailView({ character, vm }: KanaDetailViewProps) {
	return (
		<div className="flex flex-col gap-8">
			<div className="grid grid-cols-1 gap-6 lg:grid-cols-[auto_1fr]">
				<div className="flex justify-center rounded-xl border border-border bg-background-subtle p-10">
					<CharacterGlyph char={character.char} category={character.category} className="text-9xl" />
				</div>
				<div className="flex flex-col gap-4">
					<div className="flex flex-wrap items-baseline gap-3">
						<Typography role="h1" as="span">
							{character.romaji}
						</Typography>
						<Typography role="body">{GROUP_LABEL[character.group]}</Typography>
					</div>
					{character.note && <Typography role="small">{character.note}</Typography>}
					<div className="flex flex-wrap gap-3">
						<Button onClick={vm.practiceThis}>
							<PenLine className="size-4" aria-hidden="true" /> Praticar este caractere
						</Button>
						<AddToListMenu vm={vm} />
					</div>
				</div>
			</div>

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
		</div>
	);
}
