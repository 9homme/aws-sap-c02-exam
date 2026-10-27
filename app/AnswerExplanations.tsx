import { acceptedOptionIds } from "../src/answer-grading";

type ExplainedQuestion = {
  options: { id: string; text: string; explanation: string }[];
  correctIds: string[];
  selectCount: number;
  acceptedAnswerSets?: string[][];
  studyNote?: string;
  studyReferences?: string[];
};

export default function AnswerExplanations({ question, selected }: { question: ExplainedQuestion; selected: string[] }) {
  const correctIds = acceptedOptionIds(question);
  return (
    <section className="answer-explanations" aria-label="Answer explanations">
      <h3>Understand each option</h3>
      <p className="explanation-origin">Study explanations added for this app. Expand any option to compare the reasoning.</p>
      {question.studyNote && <aside className="answer-caveat"><strong>Answer-key note</strong><p>{question.studyNote}</p>{question.studyReferences?.map((url, index) => <a key={url} href={url} target="_blank" rel="noreferrer">AWS documentation{question.studyReferences!.length > 1 ? ` ${index + 1}` : ""} ↗</a>)}</aside>}
      <div className="option-explanation-list">
        {question.options.map((option) => {
          const chosen = selected.includes(option.id);
          const correct = correctIds.includes(option.id);
          const status = correct ? chosen ? "Correct · your choice" : question.selectCount === 1 && selected.some((id) => correctIds.includes(id)) ? "Also accepted" : "Correct choice" : chosen ? "Incorrect · your choice" : "Not correct here";
          return (
            <details key={option.id} className={`option-explanation ${correct ? "correct" : chosen ? "chosen-wrong" : ""}`} open={chosen || correct}>
              <summary><span className="explanation-letter">{option.id}</span><span className="explanation-option-text">{option.text}<small>{status}</small></span></summary>
              <p>{option.explanation}</p>
            </details>
          );
        })}
      </div>
    </section>
  );
}
