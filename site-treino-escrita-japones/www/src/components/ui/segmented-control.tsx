import { cn } from "@/utils/cn";
import { tab, tabs } from "./variants";

export interface SegmentedOption<T extends string> {
	value: T;
	label: string;
}

export interface SegmentedControlProps<T extends string> {
	options: SegmentedOption<T>[];
	value: T;
	onChange: (value: T) => void;
	className?: string;
	"aria-label": string;
}

export function SegmentedControl<T extends string>({
	options,
	value,
	onChange,
	className,
	...props
}: SegmentedControlProps<T>) {
	return (
		<div className={cn(tabs(), className)} role="tablist" aria-label={props["aria-label"]}>
			{options.map((option) => (
				<button
					key={option.value}
					type="button"
					role="tab"
					aria-selected={option.value === value}
					className={tab({ active: option.value === value })}
					onClick={() => onChange(option.value)}
				>
					{option.label}
				</button>
			))}
		</div>
	);
}
