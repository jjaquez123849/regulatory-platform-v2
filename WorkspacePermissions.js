export function hasWorkspacePermission(workspace, permission) {
  if (!permission) return true;

  const permissions = workspace?.permissions || [];

  return permissions.includes("*") || permissions.includes(permission);
}

export function hasWorkspaceAction(workspace, action) {
  if (!action) return true;

  const allowedActions = workspace?.allowed_actions || [];

  return allowedActions.includes(action);
}

export function canRenderWidget(workspace, manifest) {
  if (!manifest) return true;

  const permissions = manifest.permissions || [];

  if (!permissions.length) return true;

  return permissions.some((permission) =>
    hasWorkspacePermission(workspace, permission)
  );
}
