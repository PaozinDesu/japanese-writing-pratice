"use client";

import { Loader2 } from "lucide-react";
import type { ButtonHTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { button, spinner, type ButtonVariants } from "./variants";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement>, ButtonVariants {
	isLoading?: boolean;
}

export function Button({
	className,
	variant,
	size,
	isLoading = false,
	disabled,
	children,
	...props
}: ButtonProps) {
	return (
		<button
			className={cn(button({ variant, size, loading: isLoading }), className)}
			disabled={disabled ?? isLoading}
			aria-busy={isLoading}
			{...props}
		>
			{isLoading && <Loader2 className={spinner({ size: "sm" })} aria-hidden="true" />}
			{children}
		</button>
	);
}
