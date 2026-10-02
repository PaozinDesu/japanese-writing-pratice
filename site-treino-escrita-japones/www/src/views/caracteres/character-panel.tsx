"use client";

import { RotateCcw, Volume2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { CharacterStrokeDisplay } from "@/components/layout/character-stroke-display";
import { AddToListMenu } from "@/components/layout/add-to-list-menu";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Typography } from "@/components/ui/typography";
import { GROUP_LABEL } from "@/models/characters.model";
import { isKanji, type Character, type CharacterCategory, type Difficulty } from "@/models/characters.type";
import { speakJapanese } from "@/utils/speech";
import { cn } from "@/utils/cn";
import type { CharacterActions } from "@/view-models/use-character-actions";
import { useStrokeSvg } from "@/view-models/use-stroke-svg";

const CATEGORY_LABEL: Record<CharacterCategory, string> = { hiragana: "Hiragana", katakana: "Katakana", kanji: "Kanji" };
const DIFFICULTY_LABEL: Record<Difficulty, string> = {
	iniciante: "Iniciante",
	intermediario: "Intermediário",
	avancado: "Avançado",
};
// Romaji em preto pra kanji (vermelho não é cor de texto neste app); hiragana/katakana mantêm
// a cor semântica da categoria (azul/âmbar), que não entra nessa restrição.
const ROMAJI_COLOR: Record<CharacterCategory, string> = {
	hiragana: "text-hiragana",
	katakana: "text-katakana",
	kanji: "text-text-primary",
};

function StatTile({ label, value }: { label: string; value: string }) {
	return (
		<div className="flex flex-col gap-1 rounded-lg bg-background-subtle p-3">
			<Typography role="overline">{label}</Typography>
			<Typography role="body" className="font-medium text-text-primary">
				{value}
			</Typography>
		</div>
	);
}

export interface CharacterPanelProps {
	character: Character | null;
	actions: CharacterActions;
}

/**
 * Painel de detalhe ao lado da lista de Caracteres — caractere em destaque (com animação da
 * ordem dos traços quando a base tem os dados) e a descrição, sem navegar pra uma página nova.
 * Altura fixa (igual à da grade ao lado); o conteúdo rola dentro do próprio card.
 */
export function CharacterPanel({ character, actions }: CharacterPanelProps) {
	const [replayKey, setReplayKey] = useState(0);
	const scrollRef = useRef<HTMLDivElement>(null);
	const { segments, notFound } = useStrokeSvg(character, replayKey);

	useEffect(() => {
		scrollRef.current?.scrollTo({ top: 0 });
	}, [character?.id]);

	if (!character) {
		return (
			<div className="flex h-full flex-col items-center justify-center gap-2 rounded-xl border border-dashed border-border-strong p-8 text-center">
				<Typography role="body">Selecione um caractere para ver os detalhes.</Typography>
			</div>
		);
	}

	function speakCurrent() {
		if (!character) return;
		const text = isKanji(character) ? (character.readings.kun[0]?.kana ?? character.readings.on[0]?.kana ?? character.char) : character.char;
		speakJapanese(text);
	}

	return (
		<div className="flex h-full flex-col overflow-hidden rounded-xl border border-border bg-surface">
			<div ref={scrollRef} className="kaku-scrollbar flex min-h-0 flex-1 flex-col gap-5 overflow-y-auto p-6">
				<div className="flex shrink-0 items-center justify-between gap-3">
					<div className="flex flex-wrap items-center gap-2">
						<Badge tone={character.category}>{CATEGORY_LABEL[character.category]}</Badge>
						{character.jlpt && <Badge tone="neutral">{character.jlpt}</Badge>}
						<Typography role="small">{DIFFICULTY_LABEL[character.difficulty]}</Typography>
					</div>
					<div className="flex items-center gap-2">
						<button
							type="button"
							onClick={() => setReplayKey((k) => k + 1)}
							aria-label="Repetir animação da escrita"
							className="flex size-10 shrink-0 items-center justify-center rounded-lg border border-border text-text-primary"
						>
							<RotateCcw className="size-4" aria-hidden="true" />
						</button>
						<button
							type="button"
							onClick={speakCurrent}
							aria-label="Ouvir pronúncia"
							className="flex size-10 shrink-0 items-center justify-center rounded-lg border border-border text-text-primary"
						>
							<Volume2 className="size-4" aria-hidden="true" />
						</button>
					</div>
				</div>

				<CharacterStrokeDisplay character={character} segments={segments} notFound={notFound} />

				<div className="flex shrink-0 items-center justify-center gap-2 py-2">
					<span className="font-jp text-4xl text-text-primary">{character.char}</span>
					<span className={cn("text-xl font-semibold", ROMAJI_COLOR[character.category])}>{character.romaji}</span>
				</div>

				<div className="grid shrink-0 grid-cols-2 gap-3 border-t border-border pt-4">
					<StatTile label="Português" value={character.meaning.pt.join(", ")} />
					<StatTile label="Inglês" value={character.meaning.en.join(", ")} />
				</div>

				<div className="grid shrink-0 grid-cols-3 gap-3">
					<StatTile label="Traços" value={String(character.strokes)} />
					<StatTile label="Tipo" value={GROUP_LABEL[character.group]} />
					<StatTile label="Nível" value={DIFFICULTY_LABEL[character.difficulty]} />
				</div>

				{isKanji(character) && (character.readings.on.length > 0 || character.readings.kun.length > 0) && (
					<div className="flex shrink-0 flex-wrap gap-6 border-t border-border pt-4 text-sm">
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
				)}

				{character.examples.length > 0 && (
					<div className="flex shrink-0 flex-col gap-3 border-t border-border pt-4">
						<Typography role="overline">Exemplos</Typography>
						<div className="flex flex-col gap-3">
							{character.examples.slice(0, 3).map((example) => (
								<div key={example.word} className="flex items-center gap-3">
									<span className="font-jp text-2xl text-text-primary">{example.word}</span>
									<div className="flex flex-col">
										<span className="text-sm font-medium text-text-primary">{example.romaji}</span>
										<span className="text-sm text-text-muted">
											{example.pt} · {example.en}
										</span>
									</div>
								</div>
							))}
						</div>
					</div>
				)}

				<div className="flex shrink-0 flex-col gap-2 border-t border-border pt-4">
					<Typography role="overline">Ordem dos traços</Typography>
					{notFound ? (
						<Typography role="small">
							Animação ainda não disponível para este caractere ({character.strokes}{" "}
							{character.strokes === 1 ? "traço" : "traços"}).
						</Typography>
					) : (
						<Typography role="small">Toque no ícone de repetir para ver a animação de novo.</Typography>
					)}
				</div>

				<div className="mt-auto flex shrink-0 flex-wrap gap-3 pt-2">
					<Button onClick={actions.practiceThis}>Praticar</Button>
					<AddToListMenu vm={actions} />
				</div>
			</div>
		</div>
	);
}
