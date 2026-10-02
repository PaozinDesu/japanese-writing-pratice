"use client";

import { useLayoutEffect, useRef, useState } from "react";

export interface FittedGlyphProps {
	char: string;
	fill: string;
	opacity?: number;
	/** Fração (0–1) do quadro que o caractere deve preencher no eixo mais limitante — mede o conjunto inteiro, então combinações de dois caracteres escalam juntas. */
	fillRatio?: number;
	/** Proporção largura:altura do quadro (padrão 1:1, quadrado). Um viewBox quadrado dentro de um quadro retangular deixaria sobra nas laterais por causa do `preserveAspectRatio` padrão do SVG — por isso o viewBox aqui acompanha essa proporção. */
	aspect?: number;
	className?: string;
}

/** Caractere (ou combinação) redimensionado por SVG para caber numa fração do quadro, medindo a caixa real do glifo em vez de um font-size fixo — necessário porque o quadro tem largura responsiva. */
export function FittedGlyph({ char, fill, opacity = 1, fillRatio = 0.65, aspect = 1, className }: FittedGlyphProps) {
	const textRef = useRef<SVGTextElement>(null);
	const [scale, setScale] = useState(1);

	const vbWidth = aspect >= 1 ? 100 * aspect : 100;
	const vbHeight = aspect >= 1 ? 100 : 100 / aspect;
	const minDim = Math.min(vbWidth, vbHeight);
	const cx = vbWidth / 2;
	const cy = vbHeight / 2 + vbHeight * 0.02;

	useLayoutEffect(() => {
		function measure() {
			const el = textRef.current;
			if (!el) return;
			const box = el.getBBox();
			if (box.width <= 0) return;
			// getBBox().height inclui o ascent/descent da fonte (bem maior que a tinta real do
			// glifo — chegamos a medir ~1.44x o font-size numa única kanji). largura é confiável
			// (cada célula CJK "cheia" mede exatamente 1em), então tratamos a altura de cada célula
			// como quadrada a partir dela, em vez de confiar na altura reportada pelo SVG.
			const cellCount = [...char].length || 1;
			const cellSize = box.width / cellCount;
			const target = fillRatio * minDim;
			setScale(Math.min(target / box.width, target / cellSize));
		}
		measure();
		document.fonts?.ready?.then(measure);
	}, [char, fillRatio, minDim]);

	return (
		<svg
			viewBox={`0 0 ${vbWidth} ${vbHeight}`}
			aria-hidden="true"
			className={className}
			style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
		>
			<g transform={`translate(${cx} ${cy}) scale(${scale})`}>
				<text
					ref={textRef}
					x="0"
					y="0"
					textAnchor="middle"
					dominantBaseline="central"
					fontSize={minDim}
					fill={fill}
					opacity={opacity}
					style={{ fontFamily: "var(--font-klee-one)" }}
				>
					{char}
				</text>
			</g>
		</svg>
	);
}
