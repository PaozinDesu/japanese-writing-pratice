"use client";

import { useRouter } from "next/navigation";
import { fmtDate, fmtInt } from "@/models/stats.model";
import { UD } from "@/models/user-data.model";
import { useSession } from "./use-session";

export function usePerfilViewModel() {
	const router = useRouter();
	const session = useSession();

	if (!session.isLoggedIn || !session.user) {
		return { isLoggedIn: false as const };
	}

	const data = UD.load(session.user);
	const totalWritingItems = data.sessions.reduce((sum, s) => sum + s.items.length, 0);
	const totalReadingItems = data.readSessions.reduce((sum, s) => sum + s.items.length, 0);

	function logout() {
		session.logout();
		router.push("/");
	}

	return {
		isLoggedIn: true as const,
		name: session.user.name,
		email: session.user.email,
		age: session.user.age,
		initials: session.initials,
		memberSince: fmtDate(session.user.created),
		streak: session.streak,
		totalPracticed: fmtInt(totalWritingItems + totalReadingItems),
		listsCount: data.lists.length,
		logout,
	};
}

export type PerfilViewModel = ReturnType<typeof usePerfilViewModel>;
