import apiClient from "../../api/client";

export function getExtractionResults(documentId) {
  return apiClient.get(`/extraction/documents/${documentId}/results`);
}

export function updateExtractionResult(resultId, payload) {
  return apiClient.put(`/extraction/results/${resultId}`, payload);
}

export function applyExtractionResults(documentId, performedBy = "user") {
  return apiClient.post(`/extraction/documents/${documentId}/apply?performed_by=${performedBy}`);
}

export function createLearningExample(resultId, createdBy = "user") {
  return apiClient.post(`/learning/from-result/${resultId}?created_by=${createdBy}`);
}
