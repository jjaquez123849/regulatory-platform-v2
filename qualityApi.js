import apiClient from "../../api/client";

export function getRecords() {
  return apiClient.get("/records/");
}

export function runQualityReview(recordId) {
  return apiClient.post(`/quality/records/${recordId}/run?reviewed_by=user`);
}

export function getQualityReviews(recordId) {
  return apiClient.get(`/quality/records/${recordId}/reviews`);
}

export function getQualityIssues(recordId) {
  return apiClient.get(`/quality/records/${recordId}/issues`);
}

export function resolveQualityIssue(issueId, payload) {
  return apiClient.put(`/quality/issues/${issueId}/resolve`, payload);
}
