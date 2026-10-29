import { acceptedOptionIds, isCorrectAnswer } from "../src/answer-grading";
import type { ExplainedQuestion } from "../src/explanation-types";

export default function AnswerExplanations({ question, selected, originalCourseSelection }: { question: ExplainedQuestion; selected: string[]; originalCourseSelection?: string[] }) {
  const correctIds = acceptedOptionIds(question);
  const review = question.review;
  const ambiguous = review?.reviewStatus === "ambiguous";
  const historical = review?.reviewStatus === "historical";
  const accepted = isCorrectAnswer(question, selected);
  const answerSets = [question.correctIds, ...(question.acceptedAnswerSets ?? [])];
  return (
    <section className="answer-explanations" aria-label="คำอธิบายคำตอบ" lang="th">
      <div className="explanation-heading"><h3>เข้าใจเหตุผลของข้อนี้</h3><span>{question.id}</span></div>
      <p className="explanation-origin">คำอธิบายเพื่อการเรียนรู้ที่เขียนเพิ่มสำหรับแอป แยกจากเฉลยที่บันทึกจากคอร์ส{review && <> · ทบทวน {review.reviewedAt}</>}</p>
      {question.sourceCategory === "course-derived" && <p className="recap-provenance">ข้อนี้สร้างจากบันทึกคอร์สเพื่อทบทวนความรู้ ตัวเลือกลวงเป็นข้อความที่แอปสร้างเพิ่ม ไม่ใช่ตัวเลือกต้นฉบับของ AWS</p>}
      {originalCourseSelection?.length && <aside className="answer-caveat"><strong>คำตอบจากเวอร์ชันก่อน</strong><p>เดิมคุณเลือก {originalCourseSelection.join(" + ")} · แอปเก็บการตอบถูก/ผิดเดิมไว้และแปลงตำแหน่งเป็น {selected.join(" + ")} เนื่องจากตัวเลือกลวงของข้อนี้เขียนใหม่ทั้งหมด คำอธิบายและข้อความตัวเลือกด้านล่างเป็นเวอร์ชันปรับปรุง ไม่ใช่ข้อความตัวเลือกที่คุณเห็นตอนตอบครั้งแรก</p></aside>}
      {(review?.caveat || review?.reviewStatus || question.studyNote) && <aside className="answer-caveat"><strong>{ambiguous ? "โจทย์หรือเฉลยมีความกำกวม" : review?.reviewStatus === "historical" ? "บริบทบริการเปลี่ยนไปจากโจทย์เดิม" : "ข้อควรเข้าใจก่อนจำเฉลย"}</strong><p>{review?.caveat ?? question.studyNote}</p>{ambiguous && <p>ผลในแอปเทียบกับเฉลยที่บันทึกไว้ การไม่ตรงเฉลยนี้ไม่ได้ยืนยันว่าแนวทางนั้นทำไม่ได้จริง</p>}</aside>}
      <p className="answer-combination"><b>{ambiguous ? "เฉลยที่บันทึกไว้" : "ชุดคำตอบที่ยอมรับ"}:</b> {answerSets.map((ids) => ids.join(" + ")).join(" หรือ ")}{question.selectCount > 1 && <> · ต้องเลือกครบ {question.selectCount} ตัวเลือกในชุดเดียวกัน</>}</p>
      {!accepted && selected.length > 0 && selected.every((id) => correctIds.includes(id)) && question.selectCount > 1 && <p className="partial-answer">ตัวเลือกที่คุณเลือกอยู่ในเฉลย แต่ยังเลือกไม่ครบชุด จึงยังไม่ได้คะแนนข้อนี้</p>}
      {review ? <div className="reasoning-guide"><div><h4>โจทย์ให้ตัดสินจากอะไร</h4><p>{review.decisiveClue}</p></div><div><h4>วิธีคิดทีละขั้น</h4><p>{review.reasoning}</p></div></div> : <p>{question.rationale}</p>}
      <h4 className="compare-heading">เทียบทุกตัวเลือก</h4>
      <p className="explanation-origin">แสดงเหตุผลครบทั้งข้อที่เลือกและไม่ได้เลือก กดที่ตัวเลือกเพื่อย่อหรือขยาย</p>
      <div className="option-explanation-list">
        {question.options.map((option) => {
          const chosen = selected.includes(option.id);
          const correct = correctIds.includes(option.id);
          const status = ambiguous
            ? `${correct ? "อยู่ในเฉลยที่บันทึกไว้" : "ไม่อยู่ในเฉลยที่บันทึกไว้"}${chosen ? " · คุณเลือกข้อนี้" : ""}`
            : correct
              ? chosen ? historical ? "ถูกตามบริบทเดิม · คุณเลือกข้อนี้" : "ถูก · คุณเลือกข้อนี้" : question.selectCount === 1 && accepted ? "ยอมรับเป็นอีกคำตอบหนึ่ง" : "คำตอบที่ถูก · คุณไม่ได้เลือก"
              : chosen ? "ไม่ตรงเงื่อนไข · คุณเลือกข้อนี้" : "ไม่ใช่คำตอบของข้อนี้";
          return (
            <details key={`${question.id}-${option.id}`} className={`option-explanation ${ambiguous ? "ambiguous" : correct ? "correct" : chosen ? "chosen-wrong" : ""}`} open>
              <summary><span className="explanation-letter">{option.id}</span><span className="explanation-option-text"><span lang="en">{option.text}</span><small>{status}</small></span></summary>
              <p>{review?.options[option.id] ?? option.explanation}</p>
            </details>
          );
        })}
      </div>
      {review && <nav className="explanation-sources" aria-label="เอกสารประกอบคำอธิบาย"><h4>อ่านหลักการจาก AWS</h4><ul>{review.references.map(({ title, url }) => <li key={url}><a href={url} target="_blank" rel="noreferrer">{title} ↗</a></li>)}</ul></nav>}
      <details className="recorded-explanation"><summary>ดูเฉลยและหมายเหตุที่บันทึกไว้ก่อนรีวิว (อาจมีข้อมูลเก่า)</summary>{question.repairedRecap && <><p>ต้นฉบับบันทึกคอร์สก่อนแก้ความคลาดเคลื่อน:</p><p lang="en">{question.recordedCoursePrompt}</p><p lang="en">{question.recordedCourseAnswer}</p></>}<p lang="en">{question.rationale}</p>{question.studyNote && <p lang="en">{question.studyNote}</p>}{question.studyReferences?.map((url, index) => <a key={url} href={url} target="_blank" rel="noreferrer">แหล่งอ้างอิงเดิม {index + 1} ↗</a>)}</details>
    </section>
  );
}
