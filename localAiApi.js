import apiClient from "../../../api/client";

export function getLocalAIModels() {
  return apiClient.get("/local-ai/models");
}

export function createLocalAIModel(payload) {
  return apiClient.post("/local-ai/models", payload);
}

export function testLocalAI(payload) {
  return apiClient.post("/local-ai/test", payload);
}
