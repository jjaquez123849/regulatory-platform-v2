import apiClient from "../../api/client";

export function getRecordWorkspace(recordId) {
  return apiClient.get(`/workspace/records/${recordId}`);
}

export function updateRecordLogValues(recordId, payload) {
  return apiClient.put(`/log-edit/records/${recordId}/values`, payload);
}

export function getLogCompletion(recordId) {
  return apiClient.get(`/log-intelligence/records/${recordId}/completion`);
}
