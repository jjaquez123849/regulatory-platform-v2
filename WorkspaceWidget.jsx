import { getWidget } from "./WidgetRegistry.js";

function WorkspaceWidget({ widgetConfig }) {
  const WidgetComponent = getWidget(widgetConfig.widget);

  if (!WidgetComponent) {
    return (
      <div className="workspace-widget-missing">
        Widget no registrado: {widgetConfig.widget}
      </div>
    );
  }

  return <WidgetComponent config={widgetConfig} />;
}

export default WorkspaceWidget;
