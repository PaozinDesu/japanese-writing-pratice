// Porte de `KS` (source/js/account.js): tudo do Kaku vive no localStorage do navegador,
// separado por usuário, com fallback em memória quando localStorage não está disponível.
// Guarda tudo por `typeof window` porque componentes "use client" ainda rodam uma vez no
// servidor durante o SSR inicial do Next.js.

const PREFIX = "kaku.v1.";
const memoryStore: Record<string, string> = {};
let persistentChecked: boolean | null = null;

function checkPersistent(): boolean {
	if (typeof window === "undefined") return false;
	if (persistentChecked != null) return persistentChecked;
	try {
		window.localStorage.setItem(PREFIX + "__t", "1");
		window.localStorage.removeItem(PREFIX + "__t");
		persistentChecked = true;
	} catch {
		persistentChecked = false;
	}
	return persistentChecked;
}

function emitChange() {
	if (typeof window === "undefined") return;
	window.dispatchEvent(new CustomEvent("kaku:change"));
}

export const KS = {
	isPersistent: checkPersistent,
	get<T>(key: string, fallback: T): T {
		try {
			const raw = checkPersistent() ? window.localStorage.getItem(PREFIX + key) : memoryStore[key];
			return raw == null ? fallback : (JSON.parse(raw) as T);
		} catch {
			return fallback;
		}
	},
	set(key: string, value: unknown): void {
		const serialized = JSON.stringify(value);
		let saved = false;
		if (checkPersistent()) {
			try {
				window.localStorage.setItem(PREFIX + key, serialized);
				saved = true;
			} catch {
				saved = false;
			}
		}
		if (!saved) memoryStore[key] = serialized;
		emitChange();
	},
	del(key: string): void {
		try {
			if (checkPersistent()) window.localStorage.removeItem(PREFIX + key);
		} catch {
			// ignora — mesmo comportamento do protótipo
		}
		delete memoryStore[key];
		emitChange();
	},
};

/** Assina mudanças de estado (outra aba via `storage`, a própria aba via o evento `kaku:change`, e o foco da janela). */
export function subscribeToStoreChanges(onChange: () => void): () => void {
	if (typeof window === "undefined") return () => {};
	const onStorage = (e: StorageEvent) => {
		if (!e.key || e.key.indexOf(PREFIX) === 0) onChange();
	};
	window.addEventListener("storage", onStorage);
	window.addEventListener("kaku:change", onChange);
	window.addEventListener("focus", onChange);
	return () => {
		window.removeEventListener("storage", onStorage);
		window.removeEventListener("kaku:change", onChange);
		window.removeEventListener("focus", onChange);
	};
}
