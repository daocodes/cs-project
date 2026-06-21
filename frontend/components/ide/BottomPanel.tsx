export default function BottomPanel() {
  return (
    <div
      className="h-full overflow-auto border-t p-3 text-xs"
      style={{
        background: "var(--vscode-panel-bg)",
        borderColor: "var(--vscode-panel-border)",
        color: "var(--vscode-foreground)",
      }}
    >
      <p className="opacity-70">Agent trace / logs will appear here.</p>
    </div>
  );
}
