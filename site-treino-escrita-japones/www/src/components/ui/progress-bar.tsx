import { cn } from "@/utils/cn";
import { progress } from "./variants";

const FILL_CLASSES = {
	primary: "bg-primary",
	success: "bg-success-solid",
	error: "bg-error-solid",
} as const;

export interface ProgressBarProps {
	/** 0–100 */
	percent: number;
	className?: string;
	label?: string;
	/** Cor do preenchimento — "primary" (vermelho) é o padrão usado no progresso de sessão/quiz. */
	tone?: keyof typeof FILL_CLASSES;
}

export function ProgressBar({ percent, className, label, tone = "primary" }: ProgressBarProps) {
	const clamped = Math.min(100, Math.max(0, percent));
	return (
		<div
			className={cn(progress(), className)}
			role="progressbar"
			aria-valuenow={Math.round(clamped)}
			aria-valuemin={0}
			aria-valuemax={100}
			aria-label={label}
		>
			<div className={cn("h-full rounded-full transition-[width]", FILL_CLASSES[tone])} style={{ width: `${clamped}%` }} />
		</div>
	);
}
