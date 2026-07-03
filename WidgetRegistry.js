const WidgetRegistry = {};

export function registerWidget(widgetCode, component) {
  WidgetRegistry[widgetCode] = component;
}

export function getWidget(widgetCode) {
  return WidgetRegistry[widgetCode] || null;
}

export default WidgetRegistry;
