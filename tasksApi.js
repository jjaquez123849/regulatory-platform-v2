import apiClient from "../../api/client";

export function getRecords() {
  return apiClient.get("/records/");
}

export function getTasks() {
  return apiClient.get("/tasks/");
}

export function createTask(payload) {
  return apiClient.post("/tasks/", payload);
}

export function updateTask(taskId, payload) {
  return apiClient.put(`/tasks/${taskId}`, payload);
}
