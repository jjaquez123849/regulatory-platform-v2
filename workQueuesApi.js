import apiClient from "../../api/client";

export function getWorkQueues() {
  return apiClient.get("/work-queues/");
}
