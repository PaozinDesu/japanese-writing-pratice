#!/usr/bin/env node
// Copia de docs/handoff/kaku-handoff (na verdade, do repositório oficial da animCJK) só os
// SVGs de ordem de traço que os caracteres da base do Kaku realmente usam — não o repositório
// inteiro (svgsJa sozinho tem mais de 7.000 arquivos).
//
// Uso: node scripts/fetch-stroke-svgs.mjs
// Reexecute sempre que a base de caracteres (public/data/kaku-caracteres.json) mudar.
//
// Fonte: https://github.com/parsimonhi/animCJK
// - Kanji: pasta svgsJa (Arphic Public License).
// - Hiragana/katakana: pasta svgsJaKana (LGPL).
// As licenças completas ficam em public/stroke-svgs/LICENSES/ (copiadas por este script).

import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync, copyFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = fileURLToPath(new URL("..", import.meta.url));
const DATA_PATH = join(ROOT, "public", "data", "kaku-caracteres.json");
const OUT_DIR = join(ROOT, "public", "stroke-svgs");
const LICENSES_DIR = join(OUT_DIR, "LICENSES");
const REPO_URL = "https://github.com/parsimonhi/animCJK.git";

function log(msg) {
	console.log(`[fetch-stroke-svgs] ${msg}`);
}

function collectNeededCodepoints(characters) {
	const kanji = new Set();
	const kana = new Set();
	for (const c of characters) {
		const codepoints = [...c.char].map((ch) => ch.codePointAt(0));
		const bucket = c.category === "kanji" ? kanji : kana;
		for (const cp of codepoints) bucket.add(cp);
	}
	return { kanji, kana };
}

function main() {
	log("Lendo public/data/kaku-caracteres.json...");
	const db = JSON.parse(readFileSync(DATA_PATH, "utf8"));
	const { kanji, kana } = collectNeededCodepoints(db.characters);
	log(`Codepoints únicos necessários: ${kanji.size} de kanji (svgsJa), ${kana.size} de kana (svgsJaKana).`);

	const cloneDir = mkdtempSync(join(tmpdir(), "animcjk-"));
	log(`Clonando animCJK (sparse, sem histórico) em ${cloneDir}...`);
	try {
		execFileSync("git", ["clone", "--depth", "1", "--filter=blob:none", "--sparse", REPO_URL, cloneDir], {
			stdio: "inherit",
		});
		execFileSync("git", ["sparse-checkout", "set", "svgsJa", "svgsJaKana", "licenses"], {
			cwd: cloneDir,
			stdio: "inherit",
		});

		mkdirSync(OUT_DIR, { recursive: true });
		mkdirSync(LICENSES_DIR, { recursive: true });

		const missing = { kanji: [], kana: [] };
		let copied = 0;

		for (const [set, folder, missingBucket] of [
			[kanji, "svgsJa", missing.kanji],
			[kana, "svgsJaKana", missing.kana],
		]) {
			for (const cp of set) {
				const src = join(cloneDir, folder, `${cp}.svg`);
				if (!existsSync(src)) {
					missingBucket.push(cp);
					continue;
				}
				copyFileSync(src, join(OUT_DIR, `${cp}.svg`));
				copied++;
			}
		}

		log(`Copiados ${copied} SVGs para public/stroke-svgs/.`);
		if (missing.kanji.length || missing.kana.length) {
			log(
				`Sem correspondência na animCJK: ${missing.kanji.length} kanji, ${missing.kana.length} kana. ` +
					`Codepoints: ${JSON.stringify({ kanji: missing.kanji, kana: missing.kana })}`,
			);
		} else {
			log("Todos os codepoints necessários têm SVG correspondente.");
		}

		log("Copiando licenças (Arphic Public License + LGPL)...");
		copyFileSync(join(cloneDir, "licenses", "COPYING.txt"), join(LICENSES_DIR, "COPYING.txt"));
		copyFileSync(join(cloneDir, "licenses", "LGPL.txt"), join(LICENSES_DIR, "LGPL.txt"));
		copyFileSync(join(cloneDir, "licenses", "APL", "english", "ARPHICPL.TXT"), join(LICENSES_DIR, "ARPHICPL.TXT"));
		writeFileSync(
			join(LICENSES_DIR, "README.md"),
			`# Licenças dos SVGs de ordem de traço (public/stroke-svgs/)

Os arquivos \`.svg\` desta pasta vêm do projeto [animCJK](https://github.com/parsimonhi/animCJK)
(Copyright FM-SH), reproduzidos aqui sem modificação de conteúdo (só copiados seletivamente
por \`scripts/fetch-stroke-svgs.mjs\`).

- Os SVGs de **kanji** (baixados de \`svgsJa/\`) representam um caractere e são distribuídos sob a
  **Arphic Public License** — ver \`ARPHICPL.TXT\`.
- Os SVGs de **hiragana/katakana** (baixados de \`svgsJaKana/\`) representam kana/traços e são
  distribuídos sob a **GNU Lesser General Public License (LGPL) v3+** — ver \`LGPL.txt\`.
- \`COPYING.txt\` é a nota de licenciamento geral da animCJK, explicando essa divisão.
`,
		);

		log("Concluído.");
	} finally {
		rmSync(cloneDir, { recursive: true, force: true });
	}
}

main();
