"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";
import { Auth, type RegisterErrors } from "@/models/auth.model";

export function useCadastroViewModel() {
	const router = useRouter();
	const [name, setName] = useState("");
	const [email, setEmail] = useState("");
	const [age, setAge] = useState("");
	const [pw, setPw] = useState("");
	const [pw2, setPw2] = useState("");
	const [showPassword, setShowPassword] = useState(false);
	const [errors, setErrors] = useState<RegisterErrors>({});
	const [submitting, setSubmitting] = useState(false);

	async function submit(event?: FormEvent) {
		event?.preventDefault();
		setSubmitting(true);
		const result = await Auth.register({ name, email, age, pw, pw2 });
		setSubmitting(false);
		if (!result.ok) {
			setErrors(result.errors);
			return;
		}
		router.push(Auth.takeReturnTo());
	}

	return {
		name,
		setName,
		email,
		setEmail,
		age,
		setAge,
		pw,
		setPw,
		pw2,
		setPw2,
		showPassword,
		toggleShowPassword: () => setShowPassword((v) => !v),
		errors,
		submitting,
		submit,
	};
}

export type CadastroViewModel = ReturnType<typeof useCadastroViewModel>;
