import { Card, CardContent } from "@/components/ui/card";

interface Props {
  categories: Record<string, string[]>;
}

export default function SkillCategories({ categories }: Props) {
  return (
    <section>
      <h2 className="text-2xl font-semibold text-gray-800 mb-4">💻 Skill Categories</h2>
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
        {Object.entries(categories || {}).map(([category, skills]) => (
          <Card key={category}>
            <CardContent className="p-4">
              <h3 className="font-semibold text-blue-700 mb-2 capitalize">{category}</h3>
              <div className="flex flex-wrap gap-2">
                {skills.map((skill) => (
                  <span
                    key={skill}
                    className="bg-blue-100 text-blue-800 text-sm font-medium px-2 py-1 rounded-lg"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
