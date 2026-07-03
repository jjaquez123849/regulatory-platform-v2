import LoadingState from "../../feedback/LoadingState.jsx";
import ErrorState from "../../feedback/ErrorState.jsx";
import WorkspaceEngine from "./WorkspaceEngine.jsx";

function WorkspaceLoader({
  workspace,
  loading,
  error,
}) {
  if (loading) {
    return <LoadingState message="Cargando Workspace..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return <WorkspaceEngine workspace={workspace} />;
}

export default WorkspaceLoader;
