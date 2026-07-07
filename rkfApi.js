import client from "../../api/client.js";

export function getRKFDocuments() {
  return client.get("/rkf/documents");
}

export function getRKFDocument(documentId) {
  return client.get(`/rkf/documents/${documentId}`);
}

export function getRKFRir(documentId) {
  return client.get(`/rkf/documents/${documentId}/rir`);
}

export function saveRKFRir(documentId, rir) {
  return client.post(`/rkf/documents/${documentId}/rir`, rir);
}

export function validateRKFRir(documentId) {
  return client.post(`/rkf/documents/${documentId}/validate`);
}
