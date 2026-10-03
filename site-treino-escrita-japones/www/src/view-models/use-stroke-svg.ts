"use client";

import { useEffect, useState } from "react";
import type { Character } from "@/models/characters.type";
import {
	countStrokesInSvg,
	loadStrokeSvgText,
	nextStrokeSvgInstanceId,
	prepareStrokeSvgMarkup,
	strokeAnimationDuration,
} from "@/models/stroke-svg.model";

export interface StrokeSvgSegment {
	markup: string;
}

export interface StrokeSvgState {
	/** `null` enquanto carrega; array vazio nunca acontece (character.char sempre tem ao menos 1 code point). */
	segments: StrokeSvgSegment[] | null;
	/** `true` quando pelo menos um dos code points do caractere não tem SVG na animCJK. */
	notFound: boolean;
}

/**
 * Busca (e prepara) o SVG animado de um caractere — ou os dois SVGs, em sequência, quando o
 * caractere é uma combinação de dois code points (ex.: きゃ). Refaz a busca sempre que o
 * caractere muda ou `replayKey` muda, gerando ids de instância novos a cada vez.
 */
export function useStrokeSvg(character: Character | null, replayKey: number): StrokeSvgState {
	const [state, setState] = useState<StrokeSvgState>({ segments: null, notFound: false });

	useEffect(() => {
		if (!character) {
			setState({ segments: null, notFound: false });
			return;
		}
		let cancelled = false;
		setState({ segments: null, notFound: false });

		const codePoints = [...character.char].map((ch) => ch.codePointAt(0)!);

		loadCombined(codePoints).then((result) => {
			if (!cancelled) setState(result);
		});

		return () => {
			cancelled = true;
		};
		// eslint-disable-next-line react-hooks/exhaustive-deps -- refaz só quando o caractere ou o replay mudam
	}, [character?.id, replayKey]);

	return state;
}

async function loadCombined(codePoints: number[]): Promise<StrokeSvgState> {
	const texts = await Promise.all(codePoints.map((cp) => loadStrokeSvgText(cp)));
	if (texts.some((text) => !text)) return { segments: null, notFound: true };

	let delayOffset = 0;
	const segments: StrokeSvgSegment[] = [];
	for (const text of texts as string[]) {
		const instanceId = nextStrokeSvgInstanceId();
		segments.push({ markup: prepareStrokeSvgMarkup(text, instanceId, delayOffset) });
		delayOffset += strokeAnimationDuration(countStrokesInSvg(text));
	}
	return { segments, notFound: false };
}
