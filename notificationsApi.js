import apiClient from "../../api/client";

export function getNotifications(params = {}) {
  return apiClient.get("/notifications/", { params });
}

export function markNotificationRead(notificationId) {
  return apiClient.put(`/notifications/${notificationId}/read`);
}
