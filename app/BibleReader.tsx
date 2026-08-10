"use client";

import { Fragment, type ReactNode, useEffect, useMemo, useState } from "react";
import bibleMarkdown from "../content/aws-sap-c02-thai-exam-bible.md?raw";

type BibleReaderProps = {
  hasActiveAttempt: boolean;
  onPractice: () => void;
};

type BibleSection = {
  id: string;
  title: string;
  lines: string[];
  searchText: string;
  subtopics: { id: string; title: string }[];
};

function renderInline(text: string): ReactNode[] {
  const tokens = text.split(/(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\(https?:\/\/[^)]+\))/g).filter(Boolean);
  return tokens.map((token, index) => {
    if (token.startsWith("**") && token.endsWith("**")) return <strong key={index}>{token.slice(2, -2)}</strong>;
    if (token.startsWith("`") && token.endsWith("`")) return <code key={index}>{token.slice(1, -1)}</code>;
    const link = token.match(/^\[([^\]]+)\]\((https?:\/\/[^)]+)\)$/);
    if (link) return <a key={index} href={link[2]} target="_blank" rel="noreferrer">{link[1]} ↗</a>;
    return <Fragment key={index}>{token}</Fragment>;
  });
}

function isBlockStart(line: string) {
  return !line.trim() || /^#{1,3}\s/.test(line) || /^>/.test(line) || /^---+$/.test(line.trim()) || /^\|/.test(line) || /^[-*]\s/.test(line) || /^\d+\.\s/.test(line);
}

function tableCells(line: string) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((cell) => cell.trim());
}

function renderBlocks(lines: string[], sectionId: string) {
  const blocks: ReactNode[] = [];
  let index = 0;
  let subtopicIndex = 0;

  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) {
      index += 1;
      continue;
    }

    if (/^---+$/.test(line.trim())) {
      blocks.push(<hr key={`hr-${index}`} />);
      index += 1;
      continue;
    }

    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const content = heading[2];
      if (level === 1) blocks.push(<h1 key={`h1-${index}`}>{renderInline(content)}</h1>);
      if (level === 3) {
        const id = `${sectionId}-sub-${subtopicIndex}`;
        subtopicIndex += 1;
        blocks.push(<h3 id={id} key={id}>{renderInline(content)}</h3>);
      }
      index += 1;
      continue;
    }

    if (line.startsWith(">")) {
      const quote: string[] = [];
      while (index < lines.length && lines[index].startsWith(">")) {
        quote.push(lines[index].replace(/^>\s?/, ""));
        index += 1;
      }
      blocks.push(<blockquote key={`quote-${index}`}>{quote.map((item, quoteIndex) => item ? <p key={quoteIndex}>{renderInline(item)}</p> : <br key={quoteIndex} />)}</blockquote>);
      continue;
    }

    if (line.startsWith("|")) {
      const rows: string[][] = [];
      while (index < lines.length && lines[index].startsWith("|")) {
        rows.push(tableCells(lines[index]));
        index += 1;
      }
      const usableRows = rows.filter((row) => !row.every((cell) => /^:?-+:?$/.test(cell)));
      const [head, ...body] = usableRows;
      if (head) {
        blocks.push(
          <div className="bible-table-wrap" key={`table-${index}`} tabIndex={0} aria-label="Scrollable comparison table">
            <table>
              <thead><tr>{head.map((cell, cellIndex) => <th key={cellIndex}>{renderInline(cell)}</th>)}</tr></thead>
              <tbody>{body.map((row, rowIndex) => <tr key={rowIndex}>{row.map((cell, cellIndex) => <td key={cellIndex}>{renderInline(cell)}</td>)}</tr>)}</tbody>
            </table>
          </div>,
        );
      }
      continue;
    }

    if (/^[-*]\s/.test(line)) {
      const items: { text: string; check: boolean }[] = [];
      while (index < lines.length && /^[-*]\s/.test(lines[index])) {
        const text = lines[index].replace(/^[-*]\s+/, "");
        items.push({ text: text.replace(/^\[ \]\s*/, ""), check: /^\[ \]/.test(text) });
        index += 1;
      }
      blocks.push(
        <ul className={items.some((item) => item.check) ? "checklist" : undefined} key={`ul-${index}`}>
          {items.map((item, itemIndex) => <li key={itemIndex}>{item.check && <span className="check-box" aria-hidden="true" />}{renderInline(item.text)}</li>)}
        </ul>,
      );
      continue;
    }

    if (/^\d+\.\s/.test(line)) {
      const items: string[] = [];
      while (index < lines.length && /^\d+\.\s/.test(lines[index])) {
        items.push(lines[index].replace(/^\d+\.\s+/, ""));
        index += 1;
      }
      blocks.push(<ol key={`ol-${index}`}>{items.map((item, itemIndex) => <li key={itemIndex}>{renderInline(item)}</li>)}</ol>);
      continue;
    }

    const paragraph: string[] = [line.trim()];
    index += 1;
    while (index < lines.length && !isBlockStart(lines[index])) {
      paragraph.push(lines[index].trim());
      index += 1;
    }
    blocks.push(<p key={`p-${index}`}>{renderInline(paragraph.join(" "))}</p>);
  }

  return blocks;
}

function parseBible(markdown: string) {
  const lines = markdown.split("\n");
  const intro: string[] = [];
  const sections: BibleSection[] = [];
  let current: { title: string; lines: string[] } | null = null;

  for (const line of lines) {
    const sectionHeading = line.match(/^##\s+(.+)$/);
    if (sectionHeading) {
      if (current) {
        const id = `bible-topic-${sections.length + 1}`;
        const subtopics = current.lines.filter((item) => /^###\s+/.test(item)).map((item, index) => ({ id: `${id}-sub-${index}`, title: item.replace(/^###\s+/, "") }));
        sections.push({ id, title: current.title, lines: current.lines, subtopics, searchText: `${current.title} ${current.lines.join(" ")}`.toLocaleLowerCase("th") });
      }
      current = { title: sectionHeading[1], lines: [] };
    } else if (current) {
      current.lines.push(line);
    } else {
      intro.push(line);
    }
  }

  if (current) {
    const id = `bible-topic-${sections.length + 1}`;
    const subtopics = current.lines.filter((item) => /^###\s+/.test(item)).map((item, index) => ({ id: `${id}-sub-${index}`, title: item.replace(/^###\s+/, "") }));
    sections.push({ id, title: current.title, lines: current.lines, subtopics, searchText: `${current.title} ${current.lines.join(" ")}`.toLocaleLowerCase("th") });
  }

  return { intro, sections };
}

export default function BibleReader({ hasActiveAttempt, onPractice }: BibleReaderProps) {
  const bible = useMemo(() => parseBible(bibleMarkdown), []);
  const [query, setQuery] = useState("");
  const [activeId, setActiveId] = useState(bible.sections[0]?.id ?? "");
  const [drawerOpen, setDrawerOpen] = useState(false);

  const filteredSections = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase("th");
    return normalized ? bible.sections.filter((section) => section.searchText.includes(normalized)) : bible.sections;
  }, [bible.sections, query]);

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((left, right) => left.boundingClientRect.top - right.boundingClientRect.top)[0];
      if (visible) setActiveId(visible.target.id);
    }, { rootMargin: "-15% 0px -72% 0px", threshold: 0 });
    bible.sections.forEach((section) => {
      const element = document.getElementById(section.id);
      if (element) observer.observe(element);
    });
    return () => observer.disconnect();
  }, [bible.sections]);

  function goTo(id: string) {
    setDrawerOpen(false);
    setActiveId(id.split("-sub-")[0]);
    window.setTimeout(() => document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" }), 0);
  }

  return (
    <main className="app-shell bible-shell" lang="th">
      <header className="site-header bible-header">
        <button className="brand button-text" onClick={onPractice}><span>◈</span> Architect Lab</button>
        <nav className="main-nav" aria-label="Main navigation">
          <button onClick={onPractice}>Practice{hasActiveAttempt && <i aria-label="saved attempt" />}</button>
          <button className="active" aria-current="page">คัมภีร์</button>
        </nav>
      </header>

      <section className="bible-hero">
        <div><span className="eyebrow">SAP-C02 Thai study bible</span><h1>คัมภีร์สถาปัตยกรรม<br />ที่ค้นหาได้ทันที</h1></div>
        <p>เนื้อหาเต็ม 4 Domains, 70 decision rules, ตารางเทียบ service, กับดัก และแผนเตรียมสอบ 21 วัน</p>
      </section>

      <div className="bible-mobile-tools">
        <button className="button secondary topic-toggle" onClick={() => setDrawerOpen(true)} aria-expanded={drawerOpen} aria-controls="bible-sidebar">☰ หัวข้อ</button>
        <label className="bible-search mobile"><span className="sr-only">ค้นหาในคัมภีร์</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ค้นหา service หรือหัวข้อ…" /></label>
      </div>

      <div className="bible-layout">
        {drawerOpen && <button className="drawer-backdrop" aria-label="Close topic menu" onClick={() => setDrawerOpen(false)} />}
        <aside id="bible-sidebar" className={`bible-sidebar ${drawerOpen ? "open" : ""}`} aria-label="หัวข้อคัมภีร์">
          <div className="sidebar-heading"><div><span className="eyebrow">สารบัญ</span><strong>เลือกหัวข้อ</strong></div><button onClick={() => setDrawerOpen(false)} aria-label="Close topic menu">×</button></div>
          <label className="bible-search desktop"><span className="sr-only">ค้นหาในคัมภีร์</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ค้นหา เช่น Transit Gateway" /></label>
          <div className="topic-count">{filteredSections.length} จาก {bible.sections.length} หัวข้อ</div>
          <nav className="topic-list">
            {filteredSections.map((section) => (
              <div key={section.id} className="topic-group">
                <button className={activeId === section.id ? "active" : ""} onClick={() => goTo(section.id)}>{section.title}</button>
                {activeId === section.id && section.subtopics.length > 0 && <div className="subtopic-list">{section.subtopics.map((subtopic) => <button key={subtopic.id} onClick={() => goTo(subtopic.id)}>{subtopic.title}</button>)}</div>}
              </div>
            ))}
            {filteredSections.length === 0 && <p className="topic-empty">ไม่พบหัวข้อ ลองค้นด้วยชื่อ service ภาษาอังกฤษ</p>}
          </nav>
        </aside>

        <article className="bible-article">
          <section className="bible-intro">{renderBlocks(bible.intro, "bible-intro")}</section>
          {bible.sections.map((section) => (
            <section id={section.id} className="bible-section" key={section.id}>
              <div className="section-anchor-label">Topic {String(bible.sections.indexOf(section) + 1).padStart(2, "0")}</div>
              <h2>{renderInline(section.title)}</h2>
              {renderBlocks(section.lines, section.id)}
            </section>
          ))}
          <footer className="bible-footer"><strong>พร้อมเปลี่ยนความรู้เป็นคะแนน?</strong><p>กลับไปทำ Study mode แล้วจด decision rule ทุกข้อที่พลาด</p><button className="button primary" onClick={onPractice}>ไปทำแบบฝึกหัด →</button></footer>
        </article>
      </div>
    </main>
  );
}
