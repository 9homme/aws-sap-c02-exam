export type TeachingReview = {
  decisiveClue: string;
  reasoning: string;
  options: Record<string, string>;
  references: { title: string; url: string }[];
  caveat?: string;
  reviewStatus?: "ambiguous" | "historical";
  reviewedAt: string;
};

export type ExplainedQuestion = {
  id: string;
  sourceCategory: string;
  options: { id: string; text: string; explanation: string }[];
  correctIds: string[];
  selectCount: number;
  acceptedAnswerSets?: string[][];
  studyNote?: string;
  studyReferences?: string[];
  repairedRecap?: boolean;
  recordedCoursePrompt?: string;
  recordedCourseAnswer?: string;
  rationale: string;
  review?: TeachingReview;
};
