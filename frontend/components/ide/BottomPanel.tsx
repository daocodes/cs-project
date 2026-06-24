export default function BottomPanel() {
  return (
    <div
      className="flex h-full flex-col border-t"
      style={{
        background: "var(--vscode-panel-bg)",
        borderColor: "var(--vscode-panel-border)",
      }}
    >
      <div
        className="flex h-9 shrink-0 items-center gap-4 border-b px-4 text-xs font-semibold uppercase tracking-wide"
        style={{ borderColor: "var(--vscode-panel-border)" }}
      >
        <span style={{ color: "var(--vscode-activitybar-fg)" }}>Agent Trace</span>
        <span className="opacity-50">Logs</span>
      </div>
      <div className="flex flex-1 items-center gap-2 overflow-auto p-4 text-xs opacity-60" style={{ color: "var(--vscode-foreground)" }}>
        <span className="codicon codicon-circle-large-outline" />
        Plan → retrieve → tool call → result will stream here once the agent is wired up.
      </div>
    </div>
  );
}
