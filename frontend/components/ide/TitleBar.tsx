export default function TitleBar() {
  return (
    <header
      className="flex h-11 shrink-0 items-center justify-between border-b px-4"
      style={{
        background: "var(--vscode-activitybar-bg)",
        borderColor: "var(--vscode-panel-border)",
      }}
    >
      <div className="w-20" />

      <button
        className="flex w-72 items-center gap-2 rounded-md border px-3 py-1.5 text-xs transition-colors hover:bg-white/5"
        style={{ borderColor: "var(--vscode-panel-border)", color: "var(--vscode-foreground)" }}
      >
        <span className="codicon codicon-search text-sm opacity-70" />
        <span className="opacity-70">Search or jump to&hellip;</span>
        <kbd className="ml-auto rounded border px-1.5 py-0.5 text-[10px] opacity-60" style={{ borderColor: "var(--vscode-panel-border)" }}>
          ⌘K
        </kbd>
      </button>

      <div
        className="flex h-7 w-7 items-center justify-center rounded-full text-xs font-semibold"
        style={{ background: "var(--vscode-accent)", color: "white" }}
      >
        U
      </div>
    </header>
  );
}
