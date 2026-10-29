// The 69 course-derived recaps originally displayed their recorded answer in
// slot A and three generic distractors in B-D. The October 2026 review replaced
// the distractors and rotated the correct answer. Previously saved selections
// must keep their right/wrong meaning when the updated bank is loaded.
// Version 3: the 20 original/emerging AI scenarios were rewritten at
// Professional level and their correct answer moved out of slot A.
export const CURRENT_ANSWER_BANK_VERSION = 3;

// New correct slot for each rewritten AI scenario (previously always A).
const REWRITTEN_AI_CORRECT: Record<string, string> = {
  "original-01": "B", "original-02": "C", "original-03": "D", "original-04": "A", "original-05": "B",
  "original-06": "C", "original-07": "D", "original-08": "A", "original-09": "B", "original-10": "C",
  "original-11": "D", "original-12": "A", "original-13": "B", "original-14": "C", "original-15": "D",
  "emerging-01": "A", "emerging-02": "B", "emerging-03": "C", "emerging-04": "D", "emerging-05": "A",
};

type SavedAnswers = {
  answers: Record<string, string[]>;
  answerBankVersion?: number;
  originalCourseAnswers?: Record<string, string[]>;
};

export function migrateSavedCourseAnswers<T extends SavedAnswers>(attempt: T): T {
  const version = attempt.answerBankVersion ?? 0;
  if (version >= CURRENT_ANSWER_BANK_VERSION) return attempt;
  const answers = { ...attempt.answers };
  const originalCourseAnswers = { ...(attempt.originalCourseAnswers ?? {}) };
  for (const [questionId, choices] of Object.entries(answers)) {
    if (!choices.length || originalCourseAnswers[questionId]) continue;
    const match = /^course-(\d{2})$/.exec(questionId);
    if (match && version < 2) {
      const questionNumber = Number(match[1]);
      if (questionNumber < 1 || questionNumber > 69) continue;
      const correctSlot = (questionNumber - 1) % 4;
      originalCourseAnswers[questionId] = [...choices];
      // A was originally correct; B-D were distractors. Map by source ordinal,
      // so old correctness is retained regardless of new on-screen letter.
      answers[questionId] = choices.map((letter) => {
        const previousSlot = letter.charCodeAt(0) - 65;
        if (previousSlot < 0 || previousSlot > 3) return letter;
        return String.fromCharCode(65 + (previousSlot + correctSlot) % 4);
      });
      continue;
    }
    const correct = REWRITTEN_AI_CORRECT[questionId];
    if (!correct) continue;
    // Old A maps to the new correct slot; old B-D keep their order among the new distractors.
    const distractors = ["A", "B", "C", "D"].filter((letter) => letter !== correct);
    originalCourseAnswers[questionId] = [...choices];
    answers[questionId] = choices.map((letter) => {
      if (letter === "A") return correct;
      const previousSlot = letter.charCodeAt(0) - 66;
      return previousSlot >= 0 && previousSlot < 3 ? distractors[previousSlot] : letter;
    });
  }
  return { ...attempt, answers, originalCourseAnswers, answerBankVersion: CURRENT_ANSWER_BANK_VERSION };
}
