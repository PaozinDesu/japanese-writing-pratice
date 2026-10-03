"use client";

import { useEffect, useRef } from "react";
import type { InkController } from "@/models/recognition.model";
import { cn } from "@/utils/cn";

export interface StrokeCanvasProps {
	controller: InkController;
	onStrokeEnd?: () => void;
	disabled?: boolean;
	className?: string;
}

/** O quadro de desenho da prática de escrita — encapsula o `InkController` (models/recognition.model). Ocupa toda a largura do pai, mantendo proporção quadrada; a resolução interna do canvas vem do `InkController`. */
export function StrokeCanvas({ controller, onStrokeEnd, disabled = false, className }: StrokeCanvasProps) {
	const canvasRef = useRef<HTMLCanvasElement | null>(null);

	useEffect(() => {
		controller.attach(canvasRef.current);
	}, [controller]);

	return (
		<canvas
			ref={canvasRef}
			style={{ touchAction: "none" }}
			className={cn("aspect-square w-full rounded-xl", className)}
			onPointerDown={disabled ? undefined : (e) => controller.onPointerDown(e.nativeEvent)}
			onPointerMove={disabled ? undefined : (e) => controller.onPointerMove(e.nativeEvent)}
			onPointerUp={
				disabled
					? undefined
					: () => {
							controller.onPointerUp();
							onStrokeEnd?.();
						}
			}
			onPointerLeave={
				disabled
					? undefined
					: () => {
							controller.onPointerUp();
							onStrokeEnd?.();
						}
			}
		/>
	);
}
