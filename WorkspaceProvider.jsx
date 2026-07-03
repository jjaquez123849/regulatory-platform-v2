import { WorkspaceContext } from "./WorkspaceContext.jsx";

function WorkspaceProvider({
  value,
  children,
}) {
  return (
    <WorkspaceContext.Provider value={value}>
      {children}
    </WorkspaceContext.Provider>
  );
}

export default WorkspaceProvider;
