export interface CharacterGuideLinesProps {
	className?: string;
	/** Também desenha as duas diagonais, mais claras que a cruz central — usado no quadro de escrita. */
	diagonals?: boolean;
}

/**
 * Guia de escrita atrás do caractere: linhas tracejadas formando uma cruz no centro,
 * igual ao quadro de prática do handoff (opcionalmente com as diagonais também).
 */
export function CharacterGuideLines({ className, diagonals = false }: CharacterGuideLinesProps) {
	return (
		<svg
			viewBox="0 0 100 100"
			aria-hidden="true"
			className={className}
			style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }}
		>
			{diagonals && (
				<>
					<line x1="0" y1="0" x2="100" y2="100" stroke="var(--color-border)" strokeWidth="0.4" strokeDasharray="2 2" opacity="0.5" />
					<line x1="100" y1="0" x2="0" y2="100" stroke="var(--color-border)" strokeWidth="0.4" strokeDasharray="2 2" opacity="0.5" />
				</>
			)}
			<line x1="50" y1="0" x2="50" y2="100" stroke="var(--color-border)" strokeWidth="0.6" strokeDasharray="2 2" />
			<line x1="0" y1="50" x2="100" y2="50" stroke="var(--color-border)" strokeWidth="0.6" strokeDasharray="2 2" />
		</svg>
	);
}
