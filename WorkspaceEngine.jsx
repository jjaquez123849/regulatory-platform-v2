import WorkspaceProvider from "./WorkspaceProvider.jsx";
import LayoutEngine from "./LayoutEngine.jsx";

function WorkspaceEngine({ workspace }) {
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
