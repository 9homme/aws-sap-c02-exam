"use client";

import { type CSSProperties, useEffect, useMemo, useState } from "react";

type SourceCategory = "captured" | "csv" | "course-derived" | "original" | "emerging";
type Mode = "study" | "exam";
type Screen = "dashboard" | "attempt" | "result";

type Question = {
  id: string;
  sourceCategory: SourceCategory;
  sourceLabel: string;
  sourceDetail: string;
  coreEligible: boolean;
  emerging: boolean;
  domain: string;
  task: string;
  topic: string;
  type: "multiple-choice" | "multiple-response";
  selectCount: number;
  prompt: string;
  options: { id: string; text: string }[];
  correctIds: string[];
  rationale: string;
  wrongAnswerHelp: string;
  references: string[];
};

type ActiveAttempt = {
  id: string;
  mode: Mode;
  questionIds: string[];
  answers: Record<string, string[]>;
  checked: Record<string, boolean>;
  flags: string[];
  currentIndex: number;
  startedAt: number;
  deadline: number | null;
};

type HistoryItem = Omit<ActiveAttempt, "checked" | "currentIndex"> & {
  finishedAt: number;
  elapsedSeconds: number;
};

type StoredState = {
  activeAttempt: ActiveAttempt | null;
  history: HistoryItem[];
};

type ResultState = {
  item: HistoryItem;
  autoSubmitted: boolean;
};

const STORAGE_KEY = "sap-c02-practice-state-v1";
const DOMAIN_NAMES: Record<string, string> = {
  "1": "Organizational Complexity",
  "2": "New Solutions",
  "3": "Continuous Improvement",
  "4": "Migration & Modernization",
};
const EXAM_QUOTAS: Record<string, number> = { "1": 19, "2": 22, "3": 19, "4": 15 };

const sourceNames: Record<SourceCategory, string> = {
  captured: "Week 8 captured",
  csv: "Assessment CSV",
  "course-derived": "Course-derived",
  original: "Original mock",
  emerging: "Emerging AI",
};

function shuffle<T>(values: T[]) {
  const copy = [...values];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const randomIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[randomIndex]] = [copy[randomIndex], copy[index]];
  }
  return copy;
}

function sameAnswers(left: string[] = [], right: string[] = []) {
  return left.length === right.length && [...left].sort().every((value, index) => value === [...right].sort()[index]);
}

function formatDuration(seconds: number) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = seconds % 60;
  return hours > 0
    ? `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`
    : `${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`;
}

function formatDate(timestamp: number) {
  return new Intl.DateTimeFormat("en", { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" }).format(timestamp);
}

function questionOutcome(question: Question, answers: Record<string, string[]>) {
  const selected = answers[question.id] ?? [];
  return { selected, answered: selected.length > 0, correct: sameAnswers(selected, question.correctIds) };
}

function getResult(item: HistoryItem, questionsById: Map<string, Question>) {
  const questions = item.questionIds.map((id) => questionsById.get(id)).filter((question): question is Question => Boolean(question));
  const outcomes = questions.map((question) => ({ question, ...questionOutcome(question, item.answers) }));
  const correct = outcomes.filter((outcome) => outcome.correct).length;
  const answered = outcomes.filter((outcome) => outcome.answered).length;
  const byDomain = ["1", "2", "3", "4"].map((domain) => {
    const domainOutcomes = outcomes.filter((outcome) => outcome.question.domain === domain);
    const domainCorrect = domainOutcomes.filter((outcome) => outcome.correct).length;
    return { domain, total: domainOutcomes.length, correct: domainCorrect, accuracy: domainOutcomes.length ? Math.round((domainCorrect / domainOutcomes.length) * 100) : 0 };
  });
  return {
    questions,
    outcomes,
    correct,
    answered,
    incorrect: outcomes.length - correct,
    score: outcomes.length ? Math.round((correct / outcomes.length) * 100) : 0,
    byDomain,
  };
}

export default function Home() {
  const [bank, setBank] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [hydrated, setHydrated] = useState(false);
  const [screen, setScreen] = useState<Screen>("dashboard");
  const [activeAttempt, setActiveAttempt] = useState<ActiveAttempt | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [resultState, setResultState] = useState<ResultState | null>(null);
  const [now, setNow] = useState(Date.now());
  const [domainFilter, setDomainFilter] = useState("all");
  const [sourceFilter, setSourceFilter] = useState<"all" | SourceCategory>("all");
  const [includeEmerging, setIncludeEmerging] = useState(false);
  const [reviewFilter, setReviewFilter] = useState<"all" | "incorrect" | "unanswered" | "flagged">("incorrect");

  useEffect(() => {
    let mounted = true;
    fetch("/question-bank.json")
      .then((response) => {
        if (!response.ok) throw new Error("The question library could not be loaded.");
        return response.json() as Promise<Question[]>;
      })
      .then((data) => {
        if (!mounted) return;
        setBank(data);
        setLoading(false);
      })
      .catch((error: Error) => {
        if (!mounted) return;
        setLoadError(error.message);
        setLoading(false);
      });
    return () => {
      mounted = false;
    };
  }, []);

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved) as StoredState;
        setActiveAttempt(parsed.activeAttempt ?? null);
        setHistory(Array.isArray(parsed.history) ? parsed.history : []);
      }
    } catch {
      window.localStorage.removeItem(STORAGE_KEY);
    } finally {
      setHydrated(true);
    }
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    const state: StoredState = { activeAttempt, history };
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [activeAttempt, history, hydrated]);

  const questionsById = useMemo(() => new Map(bank.map((question) => [question.id, question])), [bank]);
  const sourceCounts = useMemo(
    () => bank.reduce<Record<SourceCategory, number>>((counts, question) => ({ ...counts, [question.sourceCategory]: (counts[question.sourceCategory] ?? 0) + 1 }), { captured: 0, csv: 0, "course-derived": 0, original: 0, emerging: 0 }),
    [bank],
  );
  const activeQuestions = useMemo(
    () => (activeAttempt ? activeAttempt.questionIds.map((id) => questionsById.get(id)).filter((question): question is Question => Boolean(question)) : []),
    [activeAttempt, questionsById],
  );

  useEffect(() => {
    if (!activeAttempt?.deadline) return;
    const tick = () => setNow(Date.now());
    tick();
    const timer = window.setInterval(tick, 1000);
    return () => window.clearInterval(timer);
  }, [activeAttempt?.deadline]);

  function buildHistoryItem(attempt: ActiveAttempt, autoSubmitted = false) {
    const finishedAt = autoSubmitted && attempt.deadline ? attempt.deadline : Date.now();
    return {
      id: attempt.id,
      mode: attempt.mode,
      questionIds: attempt.questionIds,
      answers: attempt.answers,
      flags: attempt.flags,
      startedAt: attempt.startedAt,
      deadline: attempt.deadline,
      finishedAt,
      elapsedSeconds: Math.max(0, Math.floor((finishedAt - attempt.startedAt) / 1000)),
    } satisfies HistoryItem;
  }

  function finishAttempt(autoSubmitted = false) {
    if (!activeAttempt) return;
    const item = buildHistoryItem(activeAttempt, autoSubmitted);
    setHistory((current) => [item, ...current]);
    setResultState({ item, autoSubmitted });
    setActiveAttempt(null);
    setScreen("result");
  }

  useEffect(() => {
    if (activeAttempt?.deadline && now >= activeAttempt.deadline) finishAttempt(true);
    // The timer only needs to respond when the persisted deadline crosses.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [now, activeAttempt?.deadline]);

  function startAttempt(mode: Mode, questionIds: string[]) {
    if (activeAttempt && !window.confirm("Discard the saved attempt and start a new one?")) return;
    const startedAt = Date.now();
    setActiveAttempt({
      id: `${mode}-${startedAt}`,
      mode,
      questionIds,
      answers: {},
      checked: {},
      flags: [],
      currentIndex: 0,
      startedAt,
      deadline: mode === "exam" ? startedAt + 180 * 60 * 1000 : null,
    });
    setResultState(null);
    setScreen("attempt");
  }

  function startFullExam() {
    const eligible = bank.filter((question) => question.coreEligible && !question.emerging);
    const selected = Object.entries(EXAM_QUOTAS).flatMap(([domain, count]) => shuffle(eligible.filter((question) => question.domain === domain)).slice(0, count));
    const selectedIds = selected.map((question) => question.id);
    if (selectedIds.length < 75) {
      const remaining = shuffle(eligible.filter((question) => !selectedIds.includes(question.id))).slice(0, 75 - selectedIds.length);
      selectedIds.push(...remaining.map((question) => question.id));
    }
    startAttempt("exam", shuffle(selectedIds));
  }

  function startStudy(size: number, weakOnly = false) {
    const missedIds = new Set(
      history.flatMap((item) => item.questionIds.filter((id) => {
        const question = questionsById.get(id);
        return question && !questionOutcome(question, item.answers).correct;
      })),
    );
    const filtered = bank.filter((question) => {
      if (!includeEmerging && question.emerging) return false;
      if (domainFilter !== "all" && question.domain !== domainFilter) return false;
      if (sourceFilter !== "all" && question.sourceCategory !== sourceFilter) return false;
      return !weakOnly || missedIds.has(question.id);
    });
    const chosen = shuffle(filtered).slice(0, Math.min(size, filtered.length)).map((question) => question.id);
    if (chosen.length === 0) return;
    startAttempt("study", chosen);
  }

  function resumeAttempt() {
    if (!activeAttempt) return;
    setScreen("attempt");
  }

  function updateSelection(question: Question, optionId: string) {
    if (!activeAttempt || (activeAttempt.mode === "study" && activeAttempt.checked[question.id])) return;
    setActiveAttempt((current) => {
      if (!current) return current;
      const currentAnswers = current.answers[question.id] ?? [];
      const nextAnswers = question.selectCount === 1
        ? [optionId]
        : currentAnswers.includes(optionId)
          ? currentAnswers.filter((value) => value !== optionId)
          : [...currentAnswers, optionId];
      return { ...current, answers: { ...current.answers, [question.id]: nextAnswers } };
    });
  }

  function checkStudyAnswer(questionId: string) {
    if (!activeAttempt) return;
    setActiveAttempt((current) => current ? { ...current, checked: { ...current.checked, [questionId]: true } } : current);
  }

  function moveTo(index: number) {
    setActiveAttempt((current) => current ? { ...current, currentIndex: Math.max(0, Math.min(index, current.questionIds.length - 1)) } : current);
  }

  function toggleFlag(questionId: string) {
    setActiveAttempt((current) => {
      if (!current) return current;
      return {
        ...current,
        flags: current.flags.includes(questionId) ? current.flags.filter((id) => id !== questionId) : [...current.flags, questionId],
      };
    });
  }

  function submitExam() {
    if (!activeAttempt) return;
    const answeredCount = Object.values(activeAttempt.answers).filter((answer) => answer.length > 0).length;
    if (window.confirm(`Submit this exam now? ${answeredCount} of ${activeAttempt.questionIds.length} questions are answered.`)) finishAttempt(false);
  }

  function clearAllProgress() {
    if (!window.confirm("Clear the saved attempt and all local history from this browser?")) return;
    window.localStorage.removeItem(STORAGE_KEY);
    setActiveAttempt(null);
    setHistory([]);
    setResultState(null);
    setScreen("dashboard");
  }

  const cumulativeStats = useMemo(() => {
    const examAttempts = history.filter((item) => item.mode === "exam");
    const examScores = examAttempts.map((item) => getResult(item, questionsById).score);
    return {
      attempts: history.length,
      exams: examAttempts.length,
      bestExam: examScores.length ? Math.max(...examScores) : null,
      latestExam: examScores[0] ?? null,
    };
  }, [history, questionsById]);

  const weakTopics = useMemo(() => {
    const totals = new Map<string, { correct: number; total: number }>();
    history.forEach((item) => item.questionIds.forEach((id) => {
      const question = questionsById.get(id);
      if (!question) return;
      const current = totals.get(question.topic) ?? { correct: 0, total: 0 };
      current.total += 1;
      if (questionOutcome(question, item.answers).correct) current.correct += 1;
      totals.set(question.topic, current);
    }));
    return [...totals.entries()]
      .filter(([, value]) => value.total >= 2)
      .map(([topic, value]) => ({ topic, accuracy: Math.round((value.correct / value.total) * 100), total: value.total }))
      .sort((left, right) => left.accuracy - right.accuracy || right.total - left.total)
      .slice(0, 4);
  }, [history, questionsById]);

  if (loading || !hydrated) {
    return <main className="loading-shell"><div className="pulse-orb" /><p>Loading your SAP-C02 practice library…</p></main>;
  }

  if (loadError) {
    return <main className="loading-shell"><p>{loadError}</p><button className="button primary" onClick={() => window.location.reload()}>Try again</button></main>;
  }

  if (screen === "attempt" && activeAttempt && activeQuestions.length > 0) {
    const question = activeQuestions[activeAttempt.currentIndex];
    const selected = activeAttempt.answers[question.id] ?? [];
    const checked = activeAttempt.mode === "study" && activeAttempt.checked[question.id];
    const outcome = questionOutcome(question, activeAttempt.answers);
    const remainingSeconds = activeAttempt.deadline ? Math.max(0, Math.ceil((activeAttempt.deadline - now) / 1000)) : null;
    const answeredCount = Object.values(activeAttempt.answers).filter((answer) => answer.length > 0).length;
    return (
      <main className="app-shell">
        <header className="attempt-header">
          <button className="brand button-text" onClick={() => setScreen("dashboard")} aria-label="Return to dashboard"><span>◈</span> Architect Lab</button>
          <div className="attempt-meta">
            <span>{activeAttempt.mode === "exam" ? "Full mock exam" : "Study set"}</span>
            {remainingSeconds !== null && <strong className={remainingSeconds < 600 ? "timer urgent" : "timer"}>◷ {formatDuration(remainingSeconds)}</strong>}
          </div>
        </header>
        <section className="attempt-layout">
          <aside className="question-rail" aria-label="Question navigator">
            <div className="rail-top"><span>Questions</span><strong>{answeredCount}/{activeQuestions.length}</strong></div>
            <div className="question-grid">
              {activeQuestions.map((item, index) => {
                const hasAnswer = (activeAttempt.answers[item.id] ?? []).length > 0;
                const isChecked = activeAttempt.checked[item.id];
                const state = index === activeAttempt.currentIndex ? "current" : isChecked && questionOutcome(item, activeAttempt.answers).correct ? "correct" : isChecked ? "incorrect" : hasAnswer ? "answered" : activeAttempt.flags.includes(item.id) ? "flagged" : "";
                return <button key={item.id} className={`question-index ${state}`} onClick={() => moveTo(index)} aria-label={`Question ${index + 1}${hasAnswer ? ", answered" : ""}`}>{index + 1}</button>;
              })}
            </div>
            <div className="rail-legend"><span><i className="legend-dot answered" /> Answered</span><span><i className="legend-dot flagged" /> Flagged</span></div>
          </aside>
          <section className="question-pane">
            <div className="question-topline">
              <div><span className="eyebrow">Question {activeAttempt.currentIndex + 1} of {activeQuestions.length}</span><span className="chip domain">D{question.domain} · {DOMAIN_NAMES[question.domain]}</span></div>
              <button className={`flag-button ${activeAttempt.flags.includes(question.id) ? "active" : ""}`} onClick={() => toggleFlag(question.id)}>{activeAttempt.flags.includes(question.id) ? "★ Marked" : "☆ Mark for review"}</button>
            </div>
            <article className="question-card">
              <div className="question-badges"><span className="chip source">{question.sourceLabel}</span><span className="chip muted">{question.selectCount > 1 ? `Select ${question.selectCount}` : "Select one"}</span></div>
              <h1>{question.prompt}</h1>
              <p className="question-instruction">{question.selectCount > 1 ? `Select exactly ${question.selectCount} responses.` : "Select the best response."}</p>
              <fieldset className="options" disabled={checked}>
                <legend className="sr-only">Answer options</legend>
                {question.options.map((option) => {
                  const isSelected = selected.includes(option.id);
                  const correctOption = question.correctIds.includes(option.id);
                  const optionState = checked ? (correctOption ? "is-correct" : isSelected ? "is-wrong" : "") : isSelected ? "is-selected" : "";
                  return (
                    <label key={option.id} className={`option ${optionState}`}>
                      <input type={question.selectCount > 1 ? "checkbox" : "radio"} name={question.id} checked={isSelected} onChange={() => updateSelection(question, option.id)} />
                      <span className="option-letter">{option.id}</span><span>{option.text}</span>
                    </label>
                  );
                })}
              </fieldset>
              {checked && (
                <div className={`feedback ${outcome.correct ? "good" : "bad"}`} role="status">
                  <strong>{outcome.correct ? "Correct — strong reasoning." : "Not quite — here is the decision rule."}</strong>
                  {!outcome.correct && <p><b>Correct answer{question.correctIds.length > 1 ? "s" : ""}:</b> {question.correctIds.join(", ")}. {question.wrongAnswerHelp}</p>}
                  <p>{question.rationale}</p>
                  <a href={question.references[0]} target="_blank" rel="noreferrer">Open SAP-C02 guide ↗</a>
                </div>
              )}
              {activeAttempt.mode === "study" && !checked && <button className="button primary check-answer" disabled={selected.length === 0} onClick={() => checkStudyAnswer(question.id)}>Check answer</button>}
            </article>
            <div className="question-actions">
              <button className="button secondary" onClick={() => moveTo(activeAttempt.currentIndex - 1)} disabled={activeAttempt.currentIndex === 0}>← Previous</button>
              {activeAttempt.currentIndex < activeQuestions.length - 1 ? <button className="button primary" onClick={() => moveTo(activeAttempt.currentIndex + 1)}>Next question →</button> : activeAttempt.mode === "exam" ? <button className="button primary" onClick={submitExam}>Submit exam</button> : <button className="button primary" onClick={() => finishAttempt(false)}>Finish study set</button>}
            </div>
          </section>
        </section>
      </main>
    );
  }

  if (screen === "result" && resultState) {
    const result = getResult(resultState.item, questionsById);
    const filteredOutcomes = result.outcomes.filter((outcome) => {
      if (reviewFilter === "incorrect") return outcome.answered && !outcome.correct;
      if (reviewFilter === "unanswered") return !outcome.answered;
      if (reviewFilter === "flagged") return resultState.item.flags.includes(outcome.question.id);
      return true;
    });
    const missedIds = result.outcomes.filter((outcome) => !outcome.correct).map((outcome) => outcome.question.id);
    return (
      <main className="app-shell">
        <header className="site-header"><button className="brand button-text" onClick={() => setScreen("dashboard")}><span>◈</span> Architect Lab</button><button className="button secondary" onClick={() => setScreen("dashboard")}>Dashboard</button></header>
        <section className="results-wrap">
          <div className="result-hero">
            <span className="eyebrow">{resultState.item.mode === "exam" ? "Mock exam complete" : "Study set complete"}</span>
            <h1>{result.score >= 75 ? "You’re on track." : "Your next study targets are clear."}</h1>
            {resultState.autoSubmitted && <p className="timeout-note">Time expired, so unanswered questions were submitted as blank.</p>}
            <div className="score-ring" style={{ "--score": `${result.score}%` } as CSSProperties}><span>{result.score}%</span><small>raw score</small></div>
            <p>{result.correct} correct · {result.incorrect} incorrect · {result.questions.length - result.answered} unanswered · {formatDuration(resultState.item.elapsedSeconds)}</p>
            <p className="benchmark">Practice benchmark: 75% raw. AWS Certification uses a separate scaled score, so this site never estimates an official score.</p>
            <div className="hero-actions"><button className="button primary" onClick={() => { if (missedIds.length) startAttempt("study", shuffle(missedIds).slice(0, Math.min(25, missedIds.length))); }}>Practice missed questions</button><button className="button secondary" onClick={() => setScreen("dashboard")}>Back to dashboard</button></div>
          </div>
          <section className="result-section"><div className="section-heading"><div><span className="eyebrow">Domain performance</span><h2>See where to focus next</h2></div></div><div className="domain-results">{result.byDomain.map((domain) => <article key={domain.domain} className="domain-result"><div><span>D{domain.domain}</span><strong>{domain.accuracy}%</strong></div><h3>{DOMAIN_NAMES[domain.domain]}</h3><p>{domain.correct} of {domain.total} correct</p><div className="progress"><i style={{ width: `${domain.accuracy}%` }} /></div></article>)}</div></section>
          <section className="result-section"><div className="review-heading"><div><span className="eyebrow">Answer review</span><h2>Turn misses into rules you remember</h2></div><div className="review-filters">{(["incorrect", "unanswered", "flagged", "all"] as const).map((filter) => <button key={filter} className={reviewFilter === filter ? "selected" : ""} onClick={() => setReviewFilter(filter)}>{filter}</button>)}</div></div><div className="review-list">{filteredOutcomes.length ? filteredOutcomes.map((outcome, index) => {
            const correctText = outcome.question.correctIds.map((id) => outcome.question.options.find((option) => option.id === id)?.text).join(" · ");
            const selectedText = outcome.selected.length ? outcome.selected.map((id) => `${id}. ${outcome.question.options.find((option) => option.id === id)?.text}`).join(" · ") : "No answer";
            return <details key={outcome.question.id} className={`review-item ${outcome.correct ? "review-correct" : "review-missed"}`} open={index === 0}><summary><span className="review-status">{outcome.correct ? "✓" : "!"}</span><span><b>Question {resultState.item.questionIds.indexOf(outcome.question.id) + 1}</b> · {outcome.question.topic}<small>{outcome.question.sourceLabel}</small></span><span>{outcome.correct ? "Correct" : "Review"}</span></summary><div className="review-body"><p className="review-prompt">{outcome.question.prompt}</p><p><b>Your answer:</b> {selectedText}</p>{!outcome.correct && <p><b>Correct answer:</b> {correctText}</p>}<div className="rationale"><b>Why:</b> {outcome.question.rationale}</div><a href={outcome.question.references[0]} target="_blank" rel="noreferrer">Study the AWS guide ↗</a></div></details>;
          }) : <p className="empty-review">No questions match this filter.</p>}</div></section>
        </section>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="site-header"><button className="brand button-text" onClick={() => setScreen("dashboard")}><span>◈</span> Architect Lab</button><div className="header-actions">{history.length > 0 && <button className="button-text subtle" onClick={clearAllProgress}>Clear local data</button>}<span className="local-badge">Saved on this device</span></div></header>
      <section className="hero">
        <div className="hero-copy"><span className="eyebrow">AWS Certified Solutions Architect – Professional</span><h1>Practice the architecture decisions that matter.</h1><p>A realistic SAP-C02 study companion built from your course record, with explanations that turn every miss into a reusable decision rule.</p><div className="hero-metrics"><div><strong>{bank.length}</strong><span>questions</span></div><div><strong>75</strong><span>exam questions</span></div><div><strong>3h</strong><span>full mock timer</span></div></div></div>
        <div className="hero-panel"><span className="panel-mark">↗</span><p className="eyebrow">Your readiness</p><strong>{cumulativeStats.latestExam ?? "—"}{cumulativeStats.latestExam !== null && "%"}</strong><p>{cumulativeStats.exams ? `Latest full mock · best ${cumulativeStats.bestExam}%` : "Take a full mock to establish your baseline."}</p><button className="button primary" onClick={startFullExam}>Start full mock</button></div>
      </section>
      <section className="dashboard-grid">
        <div className="main-column">
          {activeAttempt && <article className="resume-card"><div><span className="eyebrow">Saved session</span><h2>{activeAttempt.mode === "exam" ? "Your full mock is ready to resume" : "Your study set is ready to resume"}</h2><p>{Object.values(activeAttempt.answers).filter((answer) => answer.length > 0).length} of {activeAttempt.questionIds.length} answered · saved automatically in this browser</p></div><button className="button primary" onClick={resumeAttempt}>Resume →</button></article>}
          <section className="mode-section"><div className="section-heading"><div><span className="eyebrow">Exam simulation</span><h2>Build real exam stamina</h2></div><span className="mode-kicker">Professional-style questions only</span></div><article className="exam-card"><div className="exam-card-number">75</div><div><h3>Full SAP-C02 mock</h3><p>Three-hour timer · 19 / 22 / 19 / 15 domain mix · answer review after submission</p><div className="mini-tags"><span>Timed</span><span>Autosaves</span><span>No hints</span></div></div><button className="button primary" onClick={startFullExam}>Start exam</button></article></section>
          <section className="mode-section"><div className="section-heading"><div><span className="eyebrow">Study mode</span><h2>Get immediate feedback</h2></div><span className="mode-kicker">Foundation and advanced topics</span></div><article className="study-card"><div className="filters"><label>Domain<select value={domainFilter} onChange={(event) => setDomainFilter(event.target.value)}><option value="all">All domains</option>{Object.entries(DOMAIN_NAMES).map(([value, label]) => <option key={value} value={value}>D{value} · {label}</option>)}</select></label><label>Source<select value={sourceFilter} onChange={(event) => setSourceFilter(event.target.value as "all" | SourceCategory)}><option value="all">All sources</option>{Object.entries(sourceNames).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label><label className="checkbox-label"><input type="checkbox" checked={includeEmerging} onChange={(event) => setIncludeEmerging(event.target.checked)} /> Include optional emerging-AI practice</label></div><div className="study-actions"><div><h3>Choose your set length</h3><p>Answers are checked immediately, with a concise explanation and source link.</p></div><div className="set-buttons">{[10, 25, 50].map((size) => <button key={size} className="button secondary" onClick={() => startStudy(size)}>{size} questions</button>)}</div></div></article></section>
          {history.length > 0 && <section className="mode-section history-section"><div className="section-heading"><div><span className="eyebrow">Attempt history</span><h2>Track the trend, not one score</h2></div></div><div className="history-list">{history.slice(0, 6).map((item) => { const result = getResult(item, questionsById); return <article key={item.id}><div className="history-score"><strong>{result.score}%</strong><span>{item.mode === "exam" ? "Mock exam" : "Study"}</span></div><div><h3>{item.questionIds.length} questions · {result.correct} correct</h3><p>{formatDate(item.finishedAt)} · {formatDuration(item.elapsedSeconds)}</p></div><button className="button-text" onClick={() => { setResultState({ item, autoSubmitted: false }); setScreen("result"); }}>Review →</button></article>; })}</div></section>}
        </div>
        <aside className="side-column"><section className="side-card"><span className="eyebrow">Your study signal</span><h2>Weak topics</h2>{weakTopics.length ? <ul className="weak-list">{weakTopics.map((topic) => <li key={topic.topic}><div><b>{topic.topic}</b><span>{topic.total} answered</span></div><strong>{topic.accuracy}%</strong></li>)}</ul> : <p>Complete at least two questions in a topic to see a dependable signal here.</p>}<button className="button secondary full-width" disabled={history.length === 0} onClick={() => startStudy(25, true)}>Practice missed questions</button></section><section className="side-card library-card"><span className="eyebrow">Question library</span><h2>Know what you are practicing</h2><ul>{(Object.keys(sourceNames) as SourceCategory[]).map((source) => <li key={source}><span className={`source-dot ${source}`} /> <span>{sourceNames[source]}</span><b>{sourceCounts[source]}</b></li>)}</ul><p className="library-note">Only Week 8 is a captured official-practice-exam record. Other source labels keep course-derived and original scenarios distinct.</p></section></aside>
      </section>
    </main>
  );
}
