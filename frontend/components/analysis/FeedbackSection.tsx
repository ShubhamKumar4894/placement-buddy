import { Card, CardContent } from "@/components/ui/card";

interface Props {
  sections: any[];
}

export default function FeedbackSection({ sections }: Props) {
  return (
    <section>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">🧠 Detailed Feedback</h2>
      {sections.map((section, idx) => (
        <Card key={idx} className="mb-4">
          <CardContent className="p-6">
            <h3 className="text-xl font-semibold text-indigo-700 mb-2">
              {section.category} ({section.score}%)
            </h3>
            <p className="text-green-700 font-medium">✅ Strengths:</p>
            <ul className="list-disc list-inside text-gray-700 mb-3">
              {section.strengths.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
            <p className="text-red-700 font-medium">⚠️ Suggestions:</p>
            <ul className="list-disc list-inside text-gray-700">
              {section.suggestions.map((s: string, i: number) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
          </CardContent>
        </Card>
      ))}
    </section>
  );
}
