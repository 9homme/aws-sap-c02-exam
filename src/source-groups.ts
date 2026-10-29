export type SourceCategory = "captured" | "csv" | "course-derived" | "original" | "professional" | "emerging";
export type SourceGroup = "recorded" | "course" | "generated";

export const SOURCE_NAMES: Record<SourceCategory, string> = {
  captured: "AWS Skill Builder · Week 8 practice exam",
  csv: "AWS Skill Builder · Previous assessment CSV",
  "course-derived": "Course-derived recap",
  original: "Original AI scenarios",
  professional: "AI Professional scenarios · multi-requirement",
  emerging: "Emerging AI (optional)",
};

export const SOURCE_GROUPS: { id: SourceGroup; label: string; description: string; sources: SourceCategory[] }[] = [
  {
    id: "recorded",
    label: "AWS Skill Builder · Recorded Questions",
    description: "Recorded AWS Skill Builder practice exam and earlier assessment questions; original sources remain identifiable.",
    sources: ["captured", "csv"],
  },
  {
    id: "course",
    label: "Course-derived recaps",
    description: "App-written questions based on course topics; answer options were authored for recap.",
    sources: ["course-derived"],
  },
  {
    id: "generated",
    label: "AI-generated practice",
    description: "Original practice plus long Professional-style scenarios with multiple requirements, detailed Thai answer explanations, and optional emerging topics.",
    sources: ["original", "professional", "emerging"],
  },
];

const SOURCE_TO_GROUP: Record<SourceCategory, SourceGroup> = {
  captured: "recorded",
  csv: "recorded",
  "course-derived": "course",
  original: "generated",
  professional: "generated",
  emerging: "generated",
};

export function sourceGroupFor(category: string): SourceGroup | null {
  return SOURCE_TO_GROUP[category as SourceCategory] ?? null;
}
