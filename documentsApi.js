import apiClient from "../../api/client";

export function getRecords() {
  return apiClient.get("/records/");
}

export function getDocumentTypes() {
  return apiClient.get("/admin/document-types");
}

export function getDocuments(recordId = "") {
  const query = recordId ? `?record_id=${recordId}` : "";
  return apiClient.get(`/documents/${query}`);
}

export function uploadDocument(formData) {
  return apiClient.post("/documents/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
}

export function classifyDocument(documentId) {
  return apiClient.post(`/document-classification/${documentId}/classify`);
}

export function processDocument(documentId) {
  return apiClient.post(`/document-processing/${documentId}/process`);
}

export function understandDocument(documentId) {
  return apiClient.post(`/document-understanding/${documentId}/understand`);
}

export function getDocumentUnderstandingHistory(documentId) {
  return apiClient.get(`/document-understanding/${documentId}/history`);
}
