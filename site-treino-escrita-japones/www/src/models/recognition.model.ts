// Porte de source/js/rec.js (Ink + Rec): desenho no canvas e reconhecimento do traço por
// comparação com o glifo da fonte Klee One (distância chamfer). Só roda no cliente — todo
// componente que usar isto precisa de "use client". A referência é o próprio caractere
// renderizado com a fonte manuscrita: qualquer caractere da base ganha exercício, sem
// traçado cadastrado à mão.
import { shuffle } from "@/utils/array";
import type { CharacterDatabase } from "./characters.model";
import type { Character } from "./characters.type";

const GLYPH_FONT = '"Klee One","Hiragino Mincho ProN","Yu Mincho","Noto Serif CJK JP","Noto Sans CJK JP",serif';
const RESOLUTION = 2;
const N = 64;
const FIT_SIZE = 52;
const CORNER_RADIUS = 4;
const USER_LINE_WIDTH = 3;
const SIGMA = 4.5;
export const RECOGNITION_OK_THRESHOLD = 0.6;
export const RECOGNITION_ID_MIN = 0.33;

export interface StrokePoint {
	x: number;
	y: number;
	t: number;
	w: number;
}

export type Stroke = StrokePoint[];

/** Controlador de desenho num `<canvas>`: mantém os traços e desenha em tinta ao vivo. */
export class InkController {
	strokes: Stroke[] = [];
	private current: Stroke | null = null;
	private canvas: HTMLCanvasElement | null = null;
	private ctx: CanvasRenderingContext2D | null = null;
	private readonly size: number;

	constructor(size: number) {
		this.size = size;
	}

	attach(canvas: HTMLCanvasElement | null): void {
		if (!canvas || canvas === this.canvas) return;
		this.canvas = canvas;
		canvas.width = this.size * RESOLUTION;
		canvas.height = this.size * RESOLUTION;
		this.ctx = canvas.getContext("2d");
		this.redraw();
	}

	private point(e: { clientX: number; clientY: number; timeStamp: number }): StrokePoint {
		const rect = this.canvas!.getBoundingClientRect();
		return {
			x: ((e.clientX - rect.left) * (this.size * RESOLUTION)) / rect.width,
			y: ((e.clientY - rect.top) * (this.size * RESOLUTION)) / rect.height,
			t: e.timeStamp,
			w: 22,
		};
	}

	private lineWidthScale(): number {
		return this.size / 560 + 0.3;
	}

	private segment(a: StrokePoint, b: StrokePoint): void {
		const ctx = this.ctx;
		if (!ctx) return;
		ctx.strokeStyle = "#1F1C18";
		ctx.lineCap = "round";
		ctx.lineJoin = "round";
		ctx.lineWidth = ((a.w + b.w) / 2) * this.lineWidthScale();
		ctx.beginPath();
		ctx.moveTo(a.x, a.y);
		ctx.lineTo(b.x, b.y);
		ctx.stroke();
	}

	private dot(p: StrokePoint): void {
		const ctx = this.ctx;
		if (!ctx) return;
		ctx.fillStyle = "#1F1C18";
		ctx.beginPath();
		ctx.arc(p.x, p.y, (p.w / 2) * this.lineWidthScale(), 0, Math.PI * 2);
		ctx.fill();
	}

	redraw(): void {
		if (!this.ctx || !this.canvas) return;
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
		for (const stroke of this.strokes) {
			this.dot(stroke[0]);
			for (let i = 1; i < stroke.length; i++) this.segment(stroke[i - 1], stroke[i]);
		}
	}

	onPointerDown(e: { pointerId: number; clientX: number; clientY: number; timeStamp: number }): void {
		if (!this.ctx) return;
		try {
			this.canvas!.setPointerCapture(e.pointerId);
		} catch {
			// alguns navegadores não suportam captura de ponteiro em todo input — segue sem ela
		}
		const p = this.point(e);
		this.current = [p];
		this.dot(p);
	}

	onPointerMove(e: { clientX: number; clientY: number; timeStamp: number }): void {
		if (!this.current) return;
		const p = this.point(e);
		const a = this.current.at(-1)!;
		const dist = Math.hypot(p.x - a.x, p.y - a.y);
		if (dist < 2) return;
		const velocity = dist / Math.max(1, p.t - a.t);
		const targetWidth = Math.max(13, Math.min(28, 30 - velocity * 5));
		p.w = a.w * 0.65 + targetWidth * 0.35;
		this.current.push(p);
		this.segment(a, p);
	}

	onPointerUp(): void {
		if (!this.current) return;
		this.strokes.push(this.current);
		this.current = null;
	}

	undo(): void {
		this.strokes.pop();
		this.redraw();
	}

	clear(): void {
		this.strokes = [];
		this.current = null;
		this.redraw();
	}

	toDataUrl(): string {
		try {
			return this.canvas?.toDataURL("image/png") ?? "";
		} catch {
			return "";
		}
	}
}

type AlphaMask = Uint8Array;
interface GlyphMasks {
	thin: AlphaMask;
	wide: AlphaMask;
	d?: Float32Array;
}

const glyphCache = new Map<string, GlyphMasks | null>();

function offscreenContext(size: number): CanvasRenderingContext2D {
	const canvas = document.createElement("canvas");
	canvas.width = size;
	canvas.height = size;
	return canvas.getContext("2d", { willReadFrequently: true })!;
}

function alphaMask(ctx: CanvasRenderingContext2D, size: number): AlphaMask {
	const data = ctx.getImageData(0, 0, size, size).data;
	const mask = new Uint8Array(size * size);
	for (let i = 0; i < size * size; i++) mask[i] = data[i * 4 + 3] > 60 ? 1 : 0;
	return mask;
}

function boundingBox(mask: AlphaMask, size: number) {
	let x0 = size;
	let y0 = size;
	let x1 = -1;
	let y1 = -1;
	for (let y = 0; y < size; y++) {
		for (let x = 0; x < size; x++) {
			if (mask[y * size + x]) {
				if (x < x0) x0 = x;
				if (x > x1) x1 = x;
				if (y < y0) y0 = y;
				if (y > y1) y1 = y;
			}
		}
	}
	return x1 < 0 ? null : { x0, y0, w: x1 - x0 + 1, h: y1 - y0 + 1 };
}

/** Formas "normais" esticam pro mesmo quadrado; formas muito alongadas (一, ー, 丨) mantêm a proporção. */
function fitScale(w: number, h: number): { sx: number; sy: number } {
	const ratio = Math.min(w, h) / Math.max(w, h);
	if (ratio >= 0.35) return { sx: FIT_SIZE / w, sy: FIT_SIZE / h };
	const s = FIT_SIZE / Math.max(w, h);
	return { sx: s, sy: s };
}

function renderGlyph(ch: string): GlyphMasks | null {
	if (glyphCache.has(ch)) return glyphCache.get(ch)!;
	const stage = 220;
	const fontSize = 150;
	const font = fontSize + "px " + GLYPH_FONT;
	const probe = offscreenContext(stage);
	probe.font = font;
	probe.textAlign = "center";
	probe.textBaseline = "middle";
	probe.fillStyle = "#000";
	probe.fillText(ch, stage / 2, stage / 2);
	const box = boundingBox(alphaMask(probe, stage), stage);
	if (!box) {
		glyphCache.set(ch, null);
		return null;
	}
	const scale = fitScale(box.w, box.h);
	const meanScale = Math.sqrt(scale.sx * scale.sy);
	const draw = (lineWidth: number): AlphaMask => {
		const ctx = offscreenContext(N);
		ctx.setTransform(
			scale.sx,
			0,
			0,
			scale.sy,
			N / 2 - (box.x0 + box.w / 2) * scale.sx,
			N / 2 - (box.y0 + box.h / 2) * scale.sy,
		);
		ctx.font = font;
		ctx.textAlign = "center";
		ctx.textBaseline = "middle";
		ctx.fillStyle = "#000";
		ctx.fillText(ch, stage / 2, stage / 2);
		if (lineWidth) {
			ctx.lineWidth = lineWidth / meanScale;
			ctx.strokeStyle = "#000";
			ctx.lineJoin = "round";
			ctx.strokeText(ch, stage / 2, stage / 2);
		}
		return alphaMask(ctx, N);
	};
	const glyph: GlyphMasks = { thin: draw(0), wide: draw(2 * CORNER_RADIUS) };
	glyphCache.set(ch, glyph);
	return glyph;
}

function userMasks(strokes: Stroke[]): GlyphMasks {
	let x0 = Number.POSITIVE_INFINITY;
	let y0 = Number.POSITIVE_INFINITY;
	let x1 = Number.NEGATIVE_INFINITY;
	let y1 = Number.NEGATIVE_INFINITY;
	for (const stroke of strokes) {
		for (const p of stroke) {
			x0 = Math.min(x0, p.x);
			x1 = Math.max(x1, p.x);
			y0 = Math.min(y0, p.y);
			y1 = Math.max(y1, p.y);
		}
	}
	const w = Math.max(x1 - x0, 1);
	const h = Math.max(y1 - y0, 1);
	const scale = fitScale(w, h);
	const meanScale = Math.sqrt(scale.sx * scale.sy);
	const draw = (lineWidth: number): AlphaMask => {
		const ctx = offscreenContext(N);
		ctx.setTransform(
			scale.sx,
			0,
			0,
			scale.sy,
			N / 2 - (x0 + w / 2) * scale.sx,
			N / 2 - (y0 + h / 2) * scale.sy,
		);
		ctx.lineWidth = lineWidth / meanScale;
		ctx.lineCap = "round";
		ctx.lineJoin = "round";
		ctx.strokeStyle = "#000";
		for (const stroke of strokes) {
			ctx.beginPath();
			ctx.moveTo(stroke[0].x, stroke[0].y);
			if (stroke.length === 1) ctx.lineTo(stroke[0].x + 0.5, stroke[0].y);
			for (let i = 1; i < stroke.length; i++) ctx.lineTo(stroke[i].x, stroke[i].y);
			ctx.stroke();
		}
		return alphaMask(ctx, N);
	};
	return { thin: draw(USER_LINE_WIDTH), wide: draw(USER_LINE_WIDTH + 2 * CORNER_RADIUS) };
}

/** Distância de cada pixel até o traço mais próximo (chanfro 3-4), pra uma comparação tolerante. */
function chamferDistance(mask: AlphaMask): Float32Array {
	const dist = new Float32Array(N * N);
	for (let i = 0; i < N * N; i++) dist[i] = mask[i] ? 0 : 1e6;
	for (let y = 0; y < N; y++) {
		for (let x = 0; x < N; x++) {
			const i = y * N + x;
			let v = dist[i];
			if (x > 0) v = Math.min(v, dist[i - 1] + 3);
			if (y > 0) {
				v = Math.min(v, dist[i - N] + 3);
				if (x > 0) v = Math.min(v, dist[i - N - 1] + 4);
				if (x < N - 1) v = Math.min(v, dist[i - N + 1] + 4);
			}
			dist[i] = v;
		}
	}
	for (let y = N - 1; y >= 0; y--) {
		for (let x = N - 1; x >= 0; x--) {
			const i = y * N + x;
			let v = dist[i];
			if (x < N - 1) v = Math.min(v, dist[i + 1] + 3);
			if (y < N - 1) {
				v = Math.min(v, dist[i + N] + 3);
				if (x < N - 1) v = Math.min(v, dist[i + N + 1] + 4);
				if (x > 0) v = Math.min(v, dist[i + N - 1] + 4);
			}
			dist[i] = v;
		}
	}
	for (let i = 0; i < N * N; i++) dist[i] /= 3;
	return dist;
}

function similarityScore(user: GlyphMasks, glyph: GlyphMasks): number {
	user.d ??= chamferDistance(user.thin);
	glyph.d ??= chamferDistance(glyph.thin);
	const s2 = 2 * SIGMA * SIGMA;
	let a = 0;
	let precisionSum = 0;
	let b = 0;
	let recallSum = 0;
	for (let i = 0; i < user.thin.length; i++) {
		if (user.thin[i]) {
			a++;
			precisionSum += Math.exp((-glyph.d[i] * glyph.d[i]) / s2);
		}
		if (glyph.thin[i]) {
			b++;
			recallSum += Math.exp((-user.d[i] * user.d[i]) / s2);
		}
	}
	const precision = a ? precisionSum / a : 0;
	const recall = b ? recallSum / b : 0;
	return precision + recall ? (2 * precision * recall) / (precision + recall) : 0;
}

function relatedIds(c: Character): string[] {
	return "related" in c ? c.related : [];
}

function candidates(db: CharacterDatabase, target: Character, userStrokeCount: number): Character[] {
	const out: Character[] = [target];
	const seen = new Set([target.id]);
	const add = (c: Character | undefined) => {
		if (c && !seen.has(c.id)) {
			seen.add(c.id);
			out.push(c);
		}
	};
	for (const id of relatedIds(target).slice(0, 8)) add(db.byId.get(id));
	const targetLength = [...target.char].length;
	const near = db.characters.filter(
		(c) =>
			c.id !== target.id &&
			Math.abs(c.strokes - userStrokeCount) <= 1 &&
			[...c.char].length === targetLength &&
			(target.category === "kanji"
				? c.category === "kanji" || c.strokes <= 4
				: c.category !== "kanji" || c.strokes <= 5),
	);
	shuffle(near)
		.sort((a, b) => (a.jlpt === target.jlpt ? 0 : 1) - (b.jlpt === target.jlpt ? 0 : 1))
		.slice(0, 60)
		.forEach(add);
	return out;
}

async function ensureFontsLoaded(text: string): Promise<void> {
	try {
		if (document.fonts?.load) {
			await Promise.race([
				document.fonts.load('150px "Klee One"', text),
				new Promise((resolve) => setTimeout(resolve, 1500)),
			]);
		}
	} catch {
		// segue sem esperar — a comparação ainda funciona com a fonte de fallback
	}
}

export interface RecognitionResult {
	id: string | null;
	verdict: "ok" | "almost" | "no";
	sim: number;
	user: number;
	exp: number;
	shapeOk: boolean;
	strokesOk: boolean;
	img: string;
}

export async function evaluateDrawing(
	strokes: Stroke[],
	db: CharacterDatabase,
	target: Character,
	toDataUrl: () => string,
): Promise<RecognitionResult> {
	const strokeCount = strokes.length;
	const candidateList = candidates(db, target, strokeCount);
	await ensureFontsLoaded(candidateList.map((c) => c.char).join(""));
	const user = userMasks(strokes);

	let best: Character | null = null;
	let bestTotal = -9;
	let bestScore = 0;
	let targetScore = 0;
	let targetTotal = -9;

	for (const c of candidateList) {
		const glyph = renderGlyph(c.char);
		if (!glyph) continue;
		const score = similarityScore(user, glyph);
		const total = score - 0.035 * Math.abs(strokeCount - c.strokes);
		if (c === target) {
			targetScore = score;
			targetTotal = total;
		}
		if (total > bestTotal) {
			bestTotal = total;
			best = c;
			bestScore = score;
		}
	}

	let matched: Character | null = targetTotal >= bestTotal - 0.04 ? target : best;
	const matchedScore = matched === target ? targetScore : bestScore;
	if (matchedScore < RECOGNITION_ID_MIN) matched = null;

	const shapeOk = targetScore >= RECOGNITION_OK_THRESHOLD;
	const strokesOk = strokeCount === target.strokes;
	const verdict = matched === target && shapeOk && strokesOk ? "ok" : matched === target ? "almost" : "no";

	return {
		id: matched?.id ?? null,
		verdict,
		sim: Math.round(targetScore * 100),
		user: strokeCount,
		exp: target.strokes,
		shapeOk,
		strokesOk,
		img: toDataUrl(),
	};
}
