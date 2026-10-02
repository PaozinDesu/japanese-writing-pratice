import Link, { type LinkProps } from "next/link";
import type { AnchorHTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { button, type ButtonVariants } from "./variants";

export interface LinkButtonProps
	extends LinkProps,
		Omit<AnchorHTMLAttributes<HTMLAnchorElement>, keyof LinkProps>,
		ButtonVariants {}

export function LinkButton({ className, variant, size, ...props }: LinkButtonProps) {
	return <Link className={cn(button({ variant, size }), className)} {...props} />;
}
