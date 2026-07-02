import apiClient from "../../../api/client";

export function getProcesses() {
  return apiClient.get("/admin/processes");
}

export function getDocumentTypes(processId) {
  return apiClient.get(`/admin/document-types?process_id=${processId}`);
}

export function createDocumentType(payload) {
  return apiClient.post("/admin/document-types", payload);
}

export function getExtractionFields(documentTypeId) {
  return apiClient.get(`/admin/document-types/${documentTypeId}/extraction-fields`);
}

export function createExtractionField(payload) {
  return apiClient.post("/admin/extraction-fields", payload);
}

export function getExcelMappings(documentTypeId) {
  return apiClient.get(`/admin/document-types/${documentTypeId}/excel-mappings`);
}

export function createExcelMapping(payload) {
  return apiClient.post("/admin/excel-mappings", payload);
}
