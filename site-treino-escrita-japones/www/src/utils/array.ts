export function shuffle<T>(items: T[]): T[] {
	const result = items.slice();
	for (let i = result.length - 1; i > 0; i--) {
		const j = (Math.random() * (i + 1)) | 0;
		[result[i], result[j]] = [result[j], result[i]];
	}
	return result;
}

export function uniq<T>(items: T[]): T[] {
	return Array.from(new Set(items));
}
