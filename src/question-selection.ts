import { sourceGroupFor } from "./source-groups.ts";

type StudyQuestion = {
  id: string;
  domain: string;
  sourceCategory: string;
  emerging: boolean;
};

type StudyFilters = {
  domain: string;
  source: string;
  group?: string;
  includeEmerging: boolean;
};

export const STUDY_SIZES = [10, 25, 50, 75, 100, 150, 200] as const;

export function filterStudyQuestions<T extends StudyQuestion>(bank: T[], filters: StudyFilters): T[] {
  return bank.filter((question) =>
    (filters.includeEmerging || !question.emerging)
    && (filters.domain === "all" || question.domain === filters.domain)
    && (!filters.group || filters.group === "all" || sourceGroupFor(question.sourceCategory) === filters.group)
    && (filters.source === "all" || question.sourceCategory === filters.source),
  );
}

export function shuffle<T>(values: T[]): T[] {
  const copy = [...values];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[randomIndex]] = [copy[randomIndex], copy[index]];
  }
  return copy;
}

export function selectStudyQuestions<T extends { id: string }>(pool: T[], size: number): string[] {
  if (!Number.isInteger(size) || size < 1 || size > pool.length) {
    throw new RangeError(`Choose between 1 and ${pool.length} available questions.`);
  }
  return shuffle(pool).slice(0, size).map((question) => question.id);
}
