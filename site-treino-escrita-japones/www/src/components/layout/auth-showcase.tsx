import { CharacterGlyph } from "@/components/ui/character-glyph";
import { Typography } from "@/components/ui/typography";

export interface AuthShowcaseProps {
	title: string;
	description: string;
}

/** Painel escuro promocional ao lado dos formulários de Login/Cadastro (só em telas largas). */
export function AuthShowcase({ title, description }: AuthShowcaseProps) {
	return (
		<section
			aria-hidden="true"
			className="relative hidden flex-col justify-between overflow-hidden rounded-xl bg-secondary p-12 text-background lg:flex"
		>
			<span
				className="font-jp absolute -right-8 -bottom-20 leading-none text-secondary-hover"
				style={{ fontSize: 420 }}
				aria-hidden="true"
			>
				書
			</span>
			<span className="relative flex items-center gap-3 text-sm font-bold">
				<span className="font-jp text-lg">書く</span> kaku · escrever
			</span>
			<div className="relative flex max-w-md flex-col gap-4">
				<Typography role="h1" as="h2" className="text-background">
					{title}
				</Typography>
				<p className="text-base leading-relaxed text-stone-300">{description}</p>
			</div>
			<div className="relative flex gap-3">
				<CharacterGlyph
					char="あ"
					category="hiragana"
					className="flex size-14 items-center justify-center rounded-lg bg-secondary-hover text-3xl text-background"
				/>
				<CharacterGlyph
					char="ア"
					category="katakana"
					className="flex size-14 items-center justify-center rounded-lg bg-secondary-hover text-3xl text-background"
				/>
				<CharacterGlyph
					char="字"
					category="kanji"
					className="flex size-14 items-center justify-center rounded-lg bg-primary text-3xl text-background"
				/>
			</div>
		</section>
	);
}
