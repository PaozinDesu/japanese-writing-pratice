import type { ButtonHTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { chip, type ChipVariants } from "./variants";

export interface ChipProps extends ButtonHTMLAttributes<HTMLButtonElement>, ChipVariants {}

export function Chip({ className, selected, type = "button", ...props }: ChipProps) {
	return (
		<button
			type={type}
			className={cn(chip({ selected }), className)}
			aria-pressed={!!selected}
			{...props}
		/>
	);
}
