"use client";

import { HomeView } from "@/views/home/home.view";
import { useHomeViewModel } from "@/view-models/use-home-view-model";

export default function HomePage() {
	const vm = useHomeViewModel();
	return <HomeView vm={vm} />;
}
