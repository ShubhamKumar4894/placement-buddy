interface Props {
  suggestions: string[];
}

export default function TopSuggestions({ suggestions }: Props) {
  return (
    <section>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">⭐ Top Suggestions</h2>
      <ul className="list-disc list-inside space-y-2 text-gray-700">
        {suggestions.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </section>
  );
}
