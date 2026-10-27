type AnswerKey = { correctIds: string[]; acceptedAnswerSets?: string[][] };

export function sameAnswers(left: string[] = [], right: string[] = []) {
  const sortedRight = [...right].sort();
  return left.length === right.length && [...left].sort().every((value, index) => value === sortedRight[index]);
}

export function isCorrectAnswer(question: AnswerKey, selected: string[]) {
  return [question.correctIds, ...(question.acceptedAnswerSets ?? [])].some((answer) => sameAnswers(selected, answer));
}

export function acceptedOptionIds(question: AnswerKey) {
  return [...new Set([question.correctIds, ...(question.acceptedAnswerSets ?? [])].flat())];
}
