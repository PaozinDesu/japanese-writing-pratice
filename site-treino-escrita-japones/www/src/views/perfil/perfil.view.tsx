import { LogIn, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { EmptyState } from "@/components/ui/empty-state";
import { LinkButton } from "@/components/ui/link-button";
import { Typography } from "@/components/ui/typography";
import type { PerfilViewModel } from "@/view-models/use-perfil-view-model";

export interface PerfilViewProps {
	vm: PerfilViewModel;
}

export function PerfilView({ vm }: PerfilViewProps) {
	if (!vm.isLoggedIn) {
		return (
			<div className="mx-auto flex w-full max-w-xl flex-col gap-6 px-5 py-16 sm:px-6">
				<EmptyState
					icon={<LogIn className="size-8 text-primary" aria-hidden="true" />}
					title="Entre para ver seu perfil"
					description="Seus dados de conta e resumo de prática ficam aqui."
					action={<LinkButton href="/login">Entrar</LinkButton>}
				/>
			</div>
		);
	}

	return (
		<div className="mx-auto flex w-full max-w-xl flex-col gap-6 px-5 py-10 sm:px-6 lg:py-12">
			<Typography role="h1">Perfil</Typography>

			<Card className="flex items-center gap-4">
				<span className="flex size-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-white">
					{vm.initials}
				</span>
				<div className="flex flex-col">
					<Typography role="h3" as="p">
						{vm.name}
					</Typography>
					<Typography role="small">{vm.email}</Typography>
					<Typography role="caption">Na Kaku desde {vm.memberSince}</Typography>
				</div>
			</Card>

			<div className="grid grid-cols-3 gap-4">
				<Card padding="md" className="flex flex-col gap-1 text-center">
					<Typography role="h2" as="p">
						{vm.streak}
					</Typography>
					<Typography role="caption">dias seguidos</Typography>
				</Card>
				<Card padding="md" className="flex flex-col gap-1 text-center">
					<Typography role="h2" as="p">
						{vm.totalPracticed}
					</Typography>
					<Typography role="caption">caracteres praticados</Typography>
				</Card>
				<Card padding="md" className="flex flex-col gap-1 text-center">
					<Typography role="h2" as="p">
						{vm.listsCount}
					</Typography>
					<Typography role="caption">listas</Typography>
				</Card>
			</div>

			<Card className="flex flex-col gap-3">
				<Typography role="h4">Dados da conta</Typography>
				<dl className="flex flex-col gap-2 text-sm">
					<div className="flex justify-between">
						<dt className="text-text-secondary">Nome</dt>
						<dd className="font-bold">{vm.name}</dd>
					</div>
					<div className="flex justify-between">
						<dt className="text-text-secondary">Email</dt>
						<dd className="font-bold">{vm.email}</dd>
					</div>
					<div className="flex justify-between">
						<dt className="text-text-secondary">Idade</dt>
						<dd className="font-bold">{vm.age}</dd>
					</div>
				</dl>
			</Card>

			<Button variant="outline" onClick={vm.logout}>
				<LogOut className="size-4" aria-hidden="true" /> Sair da conta
			</Button>
		</div>
	);
}
