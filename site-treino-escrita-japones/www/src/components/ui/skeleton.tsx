import type { HTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { skeleton } from "./variants";

export function Skeleton({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
	return <div className={cn(skeleton(), className)} {...props} />;
}
