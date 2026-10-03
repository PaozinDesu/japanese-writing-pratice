import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "@/utils/cn";
import { emptyState } from "./variants";
import { Typography } from "./typography";

export interface EmptyStateProps extends HTMLAttributes<HTMLDivElement> {
	icon?: ReactNode;
	title: string;
	description?: string;
	action?: ReactNode;
}

export function EmptyState({ icon, title, description, action, className, ...props }: EmptyStateProps) {
	return (
		<div className={cn(emptyState(), className)} {...props}>
			{icon}
			<Typography role="h4">{title}</Typography>
			{description && <Typography role="small">{description}</Typography>}
			{action}
		</div>
	);
}
