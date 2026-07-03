import { useEffect } from "react";

import WorkspaceProvider from "./WorkspaceProvider.jsx";
import LayoutEngine from "./LayoutEngine.jsx";
import { registerDefaultWidgets } from "./registerDefaultWidgets.js";
import { registerDefaultWidgetManifests } from "./registerDefaultWidgetManifests.js";

function WorkspaceEngine({ workspace }) {
  useEffect(() => {
    registerDefaultWidgets();
    registerDefaultWidgetManifests();
  }, []);

  if (!workspace) {
    return null;
  }

  return (
    <WorkspaceProvider value={workspace}>
      <LayoutEngine layout={workspace.layout || []} />
    </WorkspaceProvider>
  );
}

export default WorkspaceEngine;
