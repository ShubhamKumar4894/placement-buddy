import { Card } from "@/components/ui/card";
interface Props {
  results: any;
}

export default function AnalysisOverview({ results }: Props) {
  const stats = [
    {
      title: "Overall Score",
      value: results.overall_score,
      color: "text-blue-600",
    },
    { title: "ATS Score", value: results.ats_score, color: "text-green-600" },
    {
      title: "Skills Found",
      value: results.skills_found,
      color: "text-purple-600",
    },
    {
      title: "Experience (yrs)",
      value: results.experience_years,
      color: "text-orange-600",
    },
  ];

  return (
    <section className="grid md:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <Card key={stat.title} className="text-center p-6 rounded-full">
          <h3 className="text-lg font-semibold text-gray-700">{stat.title}</h3>
          <p className={`text-3xl font-bold ${stat.color}`}>{stat.value}</p>
        </Card>
      ))}
    </section>
  );
}
