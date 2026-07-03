import { useWorkspace } from "../engine/WorkspaceContext.jsx";
import TimelinePanel from "../TimelinePanel.jsx";

function TimelineWidget() {
  const workspace = useWorkspace();

  return (
    <TimelinePanel
      items={workspace.timeline || []}
    />
  );
}

export default TimelineWidget;
