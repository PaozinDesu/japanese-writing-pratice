"use client";

import { LoginView } from "@/views/login/login.view";
import { useLoginViewModel } from "@/view-models/use-login-view-model";

export default function LoginPage() {
	const vm = useLoginViewModel();
	return <LoginView vm={vm} />;
}
