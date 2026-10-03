export function speakJapanese(text: string): void {
	if (typeof window === "undefined" || !window.speechSynthesis) return;
	const utterance = new SpeechSynthesisUtterance(text);
	utterance.lang = "ja-JP";
	window.speechSynthesis.cancel();
	window.speechSynthesis.speak(utterance);
}
