import type { ActivityKey } from "./ActivityBar";

const PLACEHOLDER_COPY: Record<ActivityKey, string> = {
  applications: "Application kanban goes here.",
  discovery: "Internship discovery feed goes here.",
  roadmap: "Roadmap checklist goes here.",
  resume: "Resume matcher + tailoring diff goes here.",
  agent: "Agent chat goes here.",
};

type MainPanelProps = {
  active: ActivityKey;
};

export default function MainPanel({ active }: MainPanelProps) {
  return (
    <div
      className="h-full overflow-auto p-6"
      style={{ background: "var(--vscode-editor-bg)" }}
    >
      <p className="text-sm" style={{ color: "var(--vscode-foreground)" }}>
        {PLACEHOLDER_COPY[active]}
      </p>
    </div>
  );
}
