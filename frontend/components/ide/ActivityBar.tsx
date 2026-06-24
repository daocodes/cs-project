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
      className="flex w-24 flex-col items-center gap-2 py-3"
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
            className="group flex h-[68px] w-20 flex-col items-center justify-center gap-1.5 rounded-md border-l-2 px-1 transition-colors hover:bg-white/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
            style={{
              borderColor: isActive ? "var(--vscode-accent)" : "transparent",
              backgroundColor: isActive ? "rgba(255,255,255,0.08)" : "transparent",
              color: isActive
                ? "var(--vscode-activitybar-fg)"
                : "var(--vscode-activitybar-inactive-fg)",
            }}
          >
            <span className={`codicon ${activity.icon} text-2xl`} />
            <span className="text-center text-[11px] font-medium leading-tight">
              {activity.label}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
