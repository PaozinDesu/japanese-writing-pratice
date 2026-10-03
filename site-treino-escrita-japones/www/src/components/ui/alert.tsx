import { AlertTriangle, CheckCircle2, Info, XCircle } from "lucide-react";
import type { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { alert, type AlertVariants } from "./variants";

const ICONS = {
	info: Info,
	success: CheckCircle2,
	warning: AlertTriangle,
	error: XCircle,
} as const;

export interface AlertProps extends HTMLAttributes<HTMLDivElement>, AlertVariants {}

export function Alert({ className, tone = "info", children, ...props }: AlertProps) {
	const Icon = ICONS[tone ?? "info"];
	return (
		<div role="alert" className={cn(alert({ tone }), className)} {...props}>
			<Icon className="size-5 shrink-0" aria-hidden="true" />
			<div>{children}</div>
		</div>
	);
}
