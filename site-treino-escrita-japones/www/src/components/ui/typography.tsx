import type { ElementType, HTMLAttributes } from "react";
import { cn } from "@/utils/cn";
import { text, type TextProps as TextVariants } from "./variants";

const DEFAULT_TAG: Record<NonNullable<TextVariants["role"]>, ElementType> = {
	display: "h1",
	h1: "h1",
	h2: "h2",
	h3: "h3",
	h4: "h4",
	body: "p",
	small: "p",
	label: "span",
	caption: "span",
	overline: "span",
};

export interface TypographyProps extends Omit<HTMLAttributes<HTMLElement>, "role">, TextVariants {
	as?: ElementType;
}

export function Typography({ role = "body", as, className, children, ...props }: TypographyProps) {
	const Tag = as ?? DEFAULT_TAG[role ?? "body"];
	return (
		<Tag className={cn(text({ role }), className)} {...props}>
			{children}
		</Tag>
	);
}
