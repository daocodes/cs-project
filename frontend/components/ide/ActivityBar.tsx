export type ActivityKey =
  | "applications"
  | "discovery"
  | "roadmap"
  | "resume"
  | "agent";

const ACTIVITIES: { key: ActivityKey; label: string; icon: string }[] = [
  { key: "applications", label: "Applications", icon: "codicon-checklist" },
  { key: "discovery", label: "Discovery", icon: "codicon-search" },
  { key: "roadmap", label: "Roadmap", icon: "codicon-graph-line" },
  { key: "resume", label: "Resume", icon: "codicon-file" },
  { key: "agent", label: "Agent", icon: "codicon-comment-discussion" },
];

type ActivityBarProps = {
  active: ActivityKey;
  onSelect: (key: ActivityKey) => void;
};

export default function ActivityBar({ active, onSelect }: ActivityBarProps) {
  return (
    <nav
      className="flex w-12 flex-col items-center gap-1 py-2"
      style={{ background: "var(--vscode-activitybar-bg)" }}
      aria-label="Activity Bar"
    >
      {ACTIVITIES.map((activity) => {
        const isActive = activity.key === active;
        return (
          <button
            key={activity.key}
            title={activity.label}
            aria-label={activity.label}
            aria-pressed={isActive}
            onClick={() => onSelect(activity.key)}
            className="flex h-12 w-12 items-center justify-center border-l-2"
            style={{
              borderColor: isActive ? "var(--vscode-accent)" : "transparent",
              color: isActive
                ? "var(--vscode-activitybar-fg)"
                : "var(--vscode-activitybar-inactive-fg)",
            }}
          >
            <span className={`codicon ${activity.icon} text-xl`} />
          </button>
        );
      })}
    </nav>
  );
}
