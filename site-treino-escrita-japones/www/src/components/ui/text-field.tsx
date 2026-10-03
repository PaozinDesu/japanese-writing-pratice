import { AlertCircle } from "lucide-react";
import { type InputHTMLAttributes, type ReactNode, useId } from "react";
import { cn } from "@/utils/cn";
import { fieldLabel, fieldMessage, input as inputVariants } from "./variants";

export interface TextFieldProps extends InputHTMLAttributes<HTMLInputElement> {
	label: string;
	error?: string;
	hint?: string;
	/** Ícone/botão dentro do campo (ex.: alternar "mostrar senha"). */
	endAdornment?: ReactNode;
	ref?: React.Ref<HTMLInputElement>;
}

export function TextField({ label, error, hint, endAdornment, className, id, ref, ...props }: TextFieldProps) {
	const generatedId = useId();
	const fieldId = id ?? generatedId;
	const messageId = `${fieldId}-message`;
	const message = error ?? hint;

	return (
		<div className="flex flex-col gap-2">
			<label htmlFor={fieldId} className={fieldLabel()}>
				{label}
			</label>
			<div className="relative">
				<input
					id={fieldId}
					ref={ref}
					className={cn(inputVariants({ state: error ? "error" : "default" }), endAdornment && "pr-12", className)}
					aria-invalid={!!error}
					aria-describedby={message ? messageId : undefined}
					{...props}
				/>
				{endAdornment && (
					<div className="absolute inset-y-0 right-1 flex items-center">{endAdornment}</div>
				)}
			</div>
			{message && (
				<span id={messageId} className={fieldMessage({ tone: error ? "error" : "help" })}>
					{error && <AlertCircle className="size-4 shrink-0 text-primary" aria-hidden="true" />}
					{message}
				</span>
			)}
		</div>
	);
}
