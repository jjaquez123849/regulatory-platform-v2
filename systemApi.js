import apiClient from "../../api/client";

export function getSystemDiagnostics() {
  return apiClient.get("/system/diagnostics");
}
