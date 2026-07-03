const WidgetManifestRegistry = {};

export function registerWidgetManifest(widgetCode, manifest) {
  WidgetManifestRegistry[widgetCode] = manifest;
}

export function getWidgetManifest(widgetCode) {
  return WidgetManifestRegistry[widgetCode] || null;
}

export function getAllWidgetManifests() {
  return WidgetManifestRegistry;
}

export default WidgetManifestRegistry;
