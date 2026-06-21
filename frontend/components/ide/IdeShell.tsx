import { useEffect, useState } from "react";
import { Allotment } from "allotment";
import ActivityBar, { type ActivityKey } from "./ActivityBar";
import MainPanel from "./MainPanel";
import BottomPanel from "./BottomPanel";

const LAYOUT_STORAGE_KEY = "internbase.ide.panelSizes";
const DEFAULT_SIZES = [70, 30];

function loadStoredSizes(): number[] {
  if (typeof window === "undefined") return DEFAULT_SIZES;
  try {
    const raw = window.localStorage.getItem(LAYOUT_STORAGE_KEY);
    if (!raw) return DEFAULT_SIZES;
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) && parsed.length === 2 ? parsed : DEFAULT_SIZES;
  } catch {
    return DEFAULT_SIZES;
  }
}

export default function IdeShell() {
  const [active, setActive] = useState<ActivityKey>("applications");
  const [panelSizes, setPanelSizes] = useState<number[]>(DEFAULT_SIZES);

  useEffect(() => {
    setPanelSizes(loadStoredSizes());
  }, []);

  const handleChange = (sizes: number[]) => {
    setPanelSizes(sizes);
    window.localStorage.setItem(LAYOUT_STORAGE_KEY, JSON.stringify(sizes));
  };

  return (
    <div className="flex h-screen w-screen">
      <ActivityBar active={active} onSelect={setActive} />
      <div className="flex-1">
        <Allotment vertical defaultSizes={panelSizes} onChange={handleChange}>
          <Allotment.Pane>
            <MainPanel active={active} />
          </Allotment.Pane>
          <Allotment.Pane preferredSize={200} minSize={80}>
            <BottomPanel />
          </Allotment.Pane>
        </Allotment>
      </div>
    </div>
  );
}
