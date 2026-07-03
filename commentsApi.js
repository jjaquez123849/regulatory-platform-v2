import apiClient from "../../api/client";

export function createComment(payload) {
  return apiClient.post("/comments/", payload);
}

export function getRecordComments(recordId) {
  return apiClient.get(`/comments/records/${recordId}`);
}
