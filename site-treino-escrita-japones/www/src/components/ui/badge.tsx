import type { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { badge, type BadgeVariants } from "./variants";

export interface BadgeProps extends HTMLAttributes<HTMLSpanElement>, BadgeVariants {}

export function Badge({ className, tone, ...props }: BadgeProps) {
	return <span className={cn(badge({ tone }), className)} {...props} />;
}
