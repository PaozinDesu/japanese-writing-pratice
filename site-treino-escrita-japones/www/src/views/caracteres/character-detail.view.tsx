import Link from "next/link";
import { EmptyState } from "@/components/ui/empty-state";
import { LinkButton } from "@/components/ui/link-button";
import { Skeleton } from "@/components/ui/skeleton";
import { isKanji } from "@/models/characters.type";
import type { CharacterDetailViewModel } from "@/view-models/use-character-detail-view-model";
import { KanaDetailView } from "./kana-detail-view";
import { KanjiDetailView } from "./kanji-detail-view";

export interface CharacterDetailViewProps {
	vm: CharacterDetailViewModel;
}

export function CharacterDetailView({ vm }: CharacterDetailViewProps) {
	return (
		<div className="mx-auto flex w-full max-w-5xl flex-col gap-6 px-5 py-10 sm:px-6 lg:px-12 lg:py-12 xl:px-20">
			<Link href="/caracteres" className="text-sm font-bold text-text-secondary">
				← Voltar para Caracteres
			</Link>

			{vm.loading ? (
				<Skeleton className="h-96 w-full" />
			) : vm.character ? (
				isKanji(vm.character) ? (
					<KanjiDetailView character={vm.character} vm={vm} />
				) : (
					<KanaDetailView character={vm.character} vm={vm} />
				)
			) : (
				<EmptyState
					title="Caractere não encontrado"
					description="Ele pode ter sido removido ou o link está incorreto."
					action={<LinkButton href="/caracteres">Ver todos os caracteres</LinkButton>}
				/>
			)}
		</div>
	);
}
