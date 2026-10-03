// Porte da técnica de animação de traço da animCJK (https://github.com/parsimonhi/animCJK,
// ver public/stroke-svgs/LICENSES/). Cada SVG (copiado seletivamente por
// scripts/fetch-stroke-svgs.mjs, nunca todo o repositório) já vem com dois grupos de <path>:
// um com `id` — a silhueta preenchida de cada traço, usada como guia — e outro com
// `clip-path` — o traçado central animado via stroke-dasharray, recortado pela silhueta
// correspondente. Só precisamos: (1) deixar os ids únicos por instância (os ids de clipPath
// colidem se o mesmo SVG aparecer mais de uma vez na tela), (2) trocar as cores fixas da
// biblioteca pelos tokens do design system, (3) atrasar o segundo SVG de uma combinação de
// dois caracteres (ex.: きゃ) pra ele animar só depois do primeiro terminar.

const svgCache = new Map<number, Promise<string | null>>();

/** Busca o SVG de um caractere (por code point) uma vez só; chamadas repetidas reusam a mesma promise. */
export function loadStrokeSvgText(codePoint: number): Promise<string | null> {
	let pending = svgCache.get(codePoint);
	if (!pending) {
		pending = fetch(`/stroke-svgs/${codePoint}.svg`)
			.then((res) => (res.ok ? res.text() : null))
			.catch(() => null);
		svgCache.set(codePoint, pending);
	}
	return pending;
}

let instanceCounter = 0;

/** Um id novo por chamada, pra nunca colidir mesmo com o mesmo SVG montado em paralelo. */
export function nextStrokeSvgInstanceId(): string {
	instanceCounter += 1;
	return `si${instanceCounter}`;
}

/** Quantos traços o SVG anima — usado pra calcular quanto atrasar o próximo SVG de uma combinação. */
export function countStrokesInSvg(svgText: string): number {
	return (svgText.match(/clip-path="url\(#/g) ?? []).length;
}

/** Duração total (segundos) da animação de um SVG com esse número de traços (1s por traço + a cauda de 0.8s do último). */
export function strokeAnimationDuration(strokeCount: number): number {
	return strokeCount + 0.8;
}

/**
 * Prepara o SVG bruto pra inserção no DOM: ids únicos, `width`/`height` 100% (o SVG original
 * não define nenhum, então cairia no tamanho padrão de 300×150 do SVG em vez de preencher o
 * contêiner), cores nos tokens do design system, e o atraso acumulado de uma combinação.
 */
export function prepareStrokeSvgMarkup(svgText: string, instanceId: string, delayOffsetSeconds = 0): string {
	let markup = svgText;

	const rootIdMatch = /id="(z\d+)"/.exec(markup);
	if (rootIdMatch) {
		const original = rootIdMatch[1];
		markup = markup.split(original).join(`${original}-${instanceId}`);
	}

	markup = markup.replace("<svg ", '<svg width="100%" height="100%" ');
	markup = markup.replaceAll("fill:#ccc;", "fill:var(--border-strong);").replaceAll("stroke:#000;", "stroke:var(--text-primary);");

	if (delayOffsetSeconds > 0) {
		markup = markup.replace(/--d:(\d+(?:\.\d+)?)s;/g, (_match, seconds: string) => `--d:${Number(seconds) + delayOffsetSeconds}s;`);
	}

	return markup;
}
