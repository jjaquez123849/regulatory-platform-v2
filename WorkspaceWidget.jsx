import { getWidget } from "./WidgetRegistry.js";
import { getWidgetManifest } from "./WidgetManifestRegistry.js";
import { canRenderWidget } from "./WorkspacePermissions.js";
import { useWorkspace } from "./WorkspaceContext.jsx";

function WorkspaceWidget({ widgetConfig }) {
  const workspace = useWorkspace();

  const WidgetComponent = getWidget(widgetConfig.widget);
  const manifest = getWidgetManifest(widgetConfig.widget);

  if (!canRenderWidget(workspace, manifest)) {
    return null;
  }

  if (!WidgetComponent) {
    return (
      <div className="workspace-widget-missing">
        Widget no registrado: {widgetConfig.widget}
      </div>
    );
  }

  return (
    <WidgetComponent
      config={widgetConfig}
      manifest={manifest}
    />
  );
}

export default WorkspaceWidget;
