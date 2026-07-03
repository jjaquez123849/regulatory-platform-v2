import apiClient from "../../api/client";

export function getRecordWorkspace(recordId) {
  return apiClient.get(`/workspace/records/${recordId}`);
}
