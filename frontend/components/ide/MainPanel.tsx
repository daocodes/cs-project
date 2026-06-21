import type { ActivityKey } from "./ActivityBar";

const SECTION_CONTENT: Record<
  ActivityKey,
  { icon: string; title: string; description: string }
> = {
  applications: {
    icon: "codicon-checklist",
    title: "Application Tracker",
    description:
      "Kanban board for tracked internship applications will live here — status pipeline, dates, notes, and resume version.",
  },
  discovery: {
    icon: "codicon-search",
    title: "Discovery Feed",
    description:
      "Personalized internship postings pulled from scrapers will be ranked and surfaced here.",
  },
  roadmap: {
    icon: "codicon-graph-line",
    title: "Roadmap",
    description:
      "Skill-gap checklist synced from the resume matcher — LeetCode, courses, and projects per target role.",
  },
  resume: {
    icon: "codicon-file",
    title: "Resume Matcher",
    description:
      "Resume vs. job description scoring, missing skills, and Bedrock-assisted tailoring diff will live here.",
  },
  agent: {
    icon: "codicon-comment-discussion",
    title: "Agent Chat",
    description:
      "Chat with the InternBase agent — it can update applications, search internships, and tailor your resume.",
  },
};

type MainPanelProps = {
  active: ActivityKey;
};

export default function MainPanel({ active }: MainPanelProps) {
  const section = SECTION_CONTENT[active];

  return (
    <div
      className="flex h-full flex-col"
      style={{ background: "var(--vscode-editor-bg)" }}
    >
      <div
        className="flex h-10 shrink-0 items-center gap-2 border-b px-4 text-sm font-medium"
        style={{ borderColor: "var(--vscode-panel-border)", color: "var(--vscode-foreground)" }}
      >
        <span className={`codicon ${section.icon} text-base`} />
        {section.title}
      </div>

      <div className="flex flex-1 flex-col items-center justify-center gap-3 p-8 text-center">
        <span
          className={`codicon ${section.icon} text-5xl opacity-30`}
          style={{ color: "var(--vscode-foreground)" }}
        />
        <p
          className="max-w-md text-sm opacity-70"
          style={{ color: "var(--vscode-foreground)" }}
        >
          {section.description}
        </p>
      </div>
    </div>
  );
}
