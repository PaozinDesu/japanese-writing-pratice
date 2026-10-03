"use client";

import { Eye, EyeOff } from "lucide-react";
import Link from "next/link";
import { AuthShowcase } from "@/components/layout/auth-showcase";
import { Button } from "@/components/ui/button";
import { TextField } from "@/components/ui/text-field";
import { Typography } from "@/components/ui/typography";
import type { LoginViewModel } from "@/view-models/use-login-view-model";

export interface LoginViewProps {
	vm: LoginViewModel;
}

export function LoginView({ vm }: LoginViewProps) {
	return (
		<div className="mx-auto grid w-full max-w-6xl gap-8 px-5 py-10 sm:px-6 lg:grid-cols-2 lg:px-12 lg:py-16 xl:px-20">
			<AuthShowcase
				title="Seu progresso, suas listas."
				description="Entre para salvar cada sessão de prática, montar listas de estudo e acompanhar sua evolução."
			/>
			<div className="flex items-center justify-center">
				<section
					aria-labelledby="t-login"
					className="flex w-full max-w-md flex-col gap-6 rounded-xl border border-border bg-surface p-10"
				>
					<div className="flex flex-col gap-2">
						<Typography role="h1" id="t-login">
							Entrar
						</Typography>
						<Typography role="body">Que bom ver você de novo.</Typography>
					</div>
					<form className="flex flex-col gap-4" noValidate onSubmit={vm.submit}>
						<TextField
							label="Email"
							type="email"
							autoComplete="email"
							value={vm.email}
							onChange={(e) => vm.setEmail(e.target.value)}
							error={vm.errors.email}
						/>
						<TextField
							label="Senha"
							type={vm.showPassword ? "text" : "password"}
							autoComplete="current-password"
							value={vm.pw}
							onChange={(e) => vm.setPw(e.target.value)}
							error={vm.errors.pw}
							endAdornment={
								<button
									type="button"
									aria-label={vm.showPassword ? "Ocultar senha" : "Mostrar senha"}
									aria-pressed={vm.showPassword}
									onClick={vm.toggleShowPassword}
									className="flex size-10 items-center justify-center rounded-lg text-text-secondary"
								>
									{vm.showPassword ? <EyeOff className="size-5" aria-hidden="true" /> : <Eye className="size-5" aria-hidden="true" />}
								</button>
							}
						/>
						<Button type="submit" size="lg" isLoading={vm.submitting}>
							Entrar
						</Button>
					</form>
					<p className="text-center text-base text-text-secondary">
						Ainda não tem conta?{" "}
						<Link href="/cadastro" className="font-bold">
							Criar conta
						</Link>
					</p>
				</section>
			</div>
		</div>
	);
}
