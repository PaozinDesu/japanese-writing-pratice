import type { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { card, type CardVariants } from "./variants";

export interface CardProps extends HTMLAttributes<HTMLDivElement>, CardVariants {}

export function Card({ className, padding, interactive, selected, ...props }: CardProps) {
	return <div className={cn(card({ padding, interactive, selected }), className)} {...props} />;
}
