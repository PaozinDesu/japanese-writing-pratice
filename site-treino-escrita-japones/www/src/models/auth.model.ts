// Porte de `Auth` (source/js/account.js). Protótipo: contas e senha (hash) ficam no
// localStorage do navegador — ver limitação conhecida no handoff (README §6). Trocar por
// um backend de verdade é trabalho futuro, fora desta leva.
import { generateId } from "@/utils/id";
import { KS } from "./local-store.model";

export interface User {
	id: string;
	name: string;
	email: string;
	age: number;
	salt: string;
	hash: string;
	created: number;
}

export interface RegisterInput {
	name: string;
	email: string;
	age: string;
	pw: string;
	pw2: string;
}

export interface LoginInput {
	email: string;
	pw: string;
}

export type RegisterErrors = Partial<Record<"name" | "email" | "age" | "pw" | "pw2", string>>;
export type LoginErrors = Partial<Record<"email" | "pw", string>>;

export type RegisterResult = { ok: true; user: User } | { ok: false; errors: RegisterErrors };
export type LoginResult = { ok: true; user: User } | { ok: false; errors: LoginErrors };

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function normEmail(email: string): string {
	return String(email ?? "").trim().toLowerCase();
}

function toBase64(buffer: ArrayBuffer | Uint8Array): string {
	let binary = "";
	const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
	bytes.forEach((b) => {
		binary += String.fromCodePoint(b);
	});
	return btoa(binary);
}

function weakHash(s: string): string {
	let h1 = 0x811c9dc5;
	let h2 = 0x01000193;
	for (let r = 0; r < 3000; r++) {
		for (let i = 0; i < s.length; i++) {
			const c = s.charCodeAt(i);
			h1 = Math.imul(h1 ^ c, 16777619) >>> 0;
			h2 = Math.imul(h2 ^ (c + r), 2246822519) >>> 0;
		}
	}
	return h1.toString(16) + h2.toString(16);
}

async function hashPw(pw: string, salt: string, algo?: string): Promise<string> {
	if (algo !== "weak" && typeof crypto !== "undefined" && crypto.subtle) {
		try {
			const enc = new TextEncoder();
			const key = await crypto.subtle.importKey("raw", enc.encode(pw), "PBKDF2", false, [
				"deriveBits",
			]);
			const bits = await crypto.subtle.deriveBits(
				{ name: "PBKDF2", salt: enc.encode(salt), iterations: 100000, hash: "SHA-256" },
				key,
				256,
			);
			return "pbkdf2$" + toBase64(bits);
		} catch {
			if (algo === "pbkdf2") throw new Error("PBKDF2 indisponível");
		}
	}
	return "weak$" + weakHash(salt + "|" + pw);
}

function newSalt(): string {
	const bytes = new Uint8Array(16);
	try {
		crypto.getRandomValues(bytes);
	} catch {
		for (let i = 0; i < bytes.length; i++) bytes[i] = Math.trunc(Math.random() * 256);
	}
	return toBase64(bytes);
}

function usersMap(): Record<string, User> {
	return KS.get<Record<string, User>>("users", {});
}

interface Session {
	uid: string;
	email: string;
	at: number;
}

export const Auth = {
	users(): Record<string, User> {
		return usersMap();
	},

	current(): User | null {
		const session = KS.get<Session | null>("session", null);
		if (!session) return null;
		const user = usersMap()[session.email];
		return user?.id === session.uid ? user : null;
	},

	checkLogin(input: LoginInput): LoginErrors {
		const errors: LoginErrors = {};
		const email = normEmail(input.email);
		if (!email) errors.email = "Informe seu email.";
		else if (!EMAIL_RE.test(email)) errors.email = "Digite um email válido, como nome@exemplo.com.";
		if (!input.pw) errors.pw = "Informe sua senha.";
		return errors;
	},

	checkRegister(input: RegisterInput): RegisterErrors {
		const errors: RegisterErrors = {};
		const email = normEmail(input.email);
		const age = String(input.age ?? "").trim();
		if (!String(input.name ?? "").trim()) errors.name = "Informe seu nome.";
		if (!email) errors.email = "Informe seu email.";
		else if (!EMAIL_RE.test(email)) errors.email = "Digite um email válido, como nome@exemplo.com.";
		else if (usersMap()[email]) errors.email = "Este email já está cadastrado. Entre com ele ou use outro email.";
		if (!age) errors.age = "Informe sua idade.";
		else if (!/^\d{1,3}$/.test(age) || +age < 1 || +age > 120) errors.age = "Digite uma idade entre 1 e 120.";
		if (!input.pw) errors.pw = "Crie uma senha.";
		else if (input.pw.length < 6) errors.pw = "A senha precisa ter pelo menos 6 caracteres.";
		if (!input.pw2) errors.pw2 = "Confirme sua senha.";
		else if (input.pw && input.pw !== input.pw2) errors.pw2 = "As senhas não coincidem.";
		return errors;
	},

	async register(input: RegisterInput): Promise<RegisterResult> {
		const errors = Auth.checkRegister(input);
		if (Object.keys(errors).length) return { ok: false, errors };
		const email = normEmail(input.email);
		const salt = newSalt();
		const hash = await hashPw(input.pw, salt);
		const users = usersMap();
		if (users[email]) {
			return {
				ok: false,
				errors: { email: "Este email já está cadastrado. Entre com ele ou use outro email." },
			};
		}
		const user: User = {
			id: generateId("u"),
			name: String(input.name).trim(),
			email,
			age: +String(input.age).trim(),
			salt,
			hash,
			created: Date.now(),
		};
		users[email] = user;
		KS.set("users", users);
		KS.set("lastEmail", email);
		return { ok: true, user };
	},

	async login(input: LoginInput): Promise<LoginResult> {
		const errors = Auth.checkLogin(input);
		if (Object.keys(errors).length) return { ok: false, errors };
		const email = normEmail(input.email);
		const user = usersMap()[email];
		if (!user) {
			return {
				ok: false,
				errors: { email: "Não encontramos uma conta com este email. Confira o endereço ou crie uma conta." },
			};
		}
		const algo = user.hash.split("$")[0];
		const hash = await hashPw(input.pw, user.salt, algo);
		if (hash !== user.hash) return { ok: false, errors: { pw: "Senha incorreta. Tente novamente." } };
		KS.set("session", { uid: user.id, email, at: Date.now() } satisfies Session);
		KS.set("lastEmail", email);
		return { ok: true, user };
	},

	logout(): void {
		KS.del("session");
	},

	/** Guarda de onde o usuário veio antes de mandá-lo pra /login (porte de `toLogin`/`returnTo`). */
	setReturnTo(path: string): void {
		KS.set("returnTo", path);
	},

	takeReturnTo(): string {
		const path = KS.get<string>("returnTo", "/");
		KS.del("returnTo");
		return path;
	},
};
