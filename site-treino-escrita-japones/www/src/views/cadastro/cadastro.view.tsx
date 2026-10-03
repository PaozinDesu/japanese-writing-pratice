"use client";

import { Eye, EyeOff } from "lucide-react";
import Link from "next/link";
import { AuthShowcase } from "@/components/layout/auth-showcase";
import { Button } from "@/components/ui/button";
import { TextField } from "@/components/ui/text-field";
import { Typography } from "@/components/ui/typography";
import type { CadastroViewModel } from "@/view-models/use-cadastro-view-model";

export interface CadastroViewProps {
	vm: CadastroViewModel;
}

export function CadastroView({ vm }: CadastroViewProps) {
	return (
		<div className="mx-auto grid w-full max-w-6xl gap-8 px-5 py-10 sm:px-6 lg:grid-cols-2 lg:px-12 lg:py-16 xl:px-20">
			<AuthShowcase
				title="Comece a escrever em japonês."
				description="Crie sua conta para guardar listas de estudo, histórico de prática e estatísticas — tudo separado por usuário."
			/>
			<div className="flex items-center justify-center">
				<section
					aria-labelledby="t-cad"
					className="flex w-full max-w-md flex-col gap-5 rounded-xl border border-border bg-surface p-10"
				>
					<div className="flex flex-col gap-2">
						<Typography role="h1" id="t-cad">
							Criar conta
						</Typography>
						<Typography role="body">Leva menos de um minuto.</Typography>
					</div>
					<form className="flex flex-col gap-3" noValidate onSubmit={vm.submit}>
						<TextField
							label="Nome"
							type="text"
							autoComplete="name"
							value={vm.name}
							onChange={(e) => vm.setName(e.target.value)}
							error={vm.errors.name}
						/>
						<div className="flex flex-col gap-3 sm:flex-row sm:items-start">
							<div className="sm:flex-1">
								<TextField
									label="Email"
									type="email"
									autoComplete="email"
									value={vm.email}
									onChange={(e) => vm.setEmail(e.target.value)}
									error={vm.errors.email}
								/>
							</div>
							<div className="sm:w-36">
								<TextField
									label="Idade"
									type="number"
									autoComplete="off"
									value={vm.age}
									onChange={(e) => vm.setAge(e.target.value)}
									error={vm.errors.age}
								/>
							</div>
						</div>
						<TextField
							label="Senha"
							type={vm.showPassword ? "text" : "password"}
							autoComplete="new-password"
							value={vm.pw}
							onChange={(e) => vm.setPw(e.target.value)}
							error={vm.errors.pw}
							hint={vm.errors.pw ? undefined : "Pelo menos 6 caracteres."}
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
						<TextField
							label="Confirmar senha"
							type={vm.showPassword ? "text" : "password"}
							autoComplete="new-password"
							value={vm.pw2}
							onChange={(e) => vm.setPw2(e.target.value)}
							error={vm.errors.pw2}
						/>
						<Button type="submit" size="lg" isLoading={vm.submitting} className="mt-1">
							Criar conta
						</Button>
					</form>
					<p className="text-center text-base text-text-secondary">
						Já tem conta?{" "}
						<Link href="/login" className="font-bold">
							Entrar
						</Link>
					</p>
				</section>
			</div>
		</div>
	);
}
