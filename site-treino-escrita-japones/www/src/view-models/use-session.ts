"use client";

// Porte de `acctVals`/`acctBind` (source/js/account.js): sessão do usuário reativa a
// mudanças no localStorage (outra aba, logout, foco da janela).
import { useCallback, useEffect, useState } from "react";
import { Auth, type User } from "@/models/auth.model";
import { subscribeToStoreChanges } from "@/models/local-store.model";
import { streakOf } from "@/models/practice-session.model";
import { UD } from "@/models/user-data.model";

export interface SessionInfo {
	user: User | null;
	isLoggedIn: boolean;
	firstName: string;
	initials: string;
	streak: number;
	logout: () => void;
}

function initials(name: string): string {
	return name
		.split(/\s+/)
		.filter(Boolean)
		.slice(0, 2)
		.map((w) => w[0]?.toUpperCase())
		.join("");
}

export function useSession(): SessionInfo {
	const [user, setUser] = useState<User | null>(null);

	useEffect(() => {
		const sync = () => setUser(Auth.current());
		sync();
		return subscribeToStoreChanges(sync);
	}, []);

	const logout = useCallback(() => {
		Auth.logout();
		setUser(null);
	}, []);

	if (!user) {
		return { user: null, isLoggedIn: false, firstName: "", initials: "", streak: 0, logout };
	}

	return {
		user,
		isLoggedIn: true,
		firstName: user.name.split(/\s+/)[0],
		initials: initials(user.name),
		streak: streakOf(UD.load(user)),
		logout,
	};
}
