"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";
import { Auth, type LoginErrors } from "@/models/auth.model";

export function useLoginViewModel() {
	const router = useRouter();
	const [email, setEmail] = useState("");
	const [pw, setPw] = useState("");
	const [showPassword, setShowPassword] = useState(false);
	const [errors, setErrors] = useState<LoginErrors>({});
	const [submitting, setSubmitting] = useState(false);

	async function submit(event?: FormEvent) {
		event?.preventDefault();
		setSubmitting(true);
		const result = await Auth.login({ email, pw });
		setSubmitting(false);
		if (!result.ok) {
			setErrors(result.errors);
			return;
		}
		router.push(Auth.takeReturnTo());
	}

	return {
		email,
		setEmail,
		pw,
		setPw,
		showPassword,
		toggleShowPassword: () => setShowPassword((v) => !v),
		errors,
		submitting,
		submit,
	};
}

export type LoginViewModel = ReturnType<typeof useLoginViewModel>;
