import apiClient from "./client";

export function createResourceApi(basePath) {
  return {
    list: (params = {}) => apiClient.get(basePath, { params }),

    get: (id) => apiClient.get(`${basePath}/${id}`),

    create: (payload) => apiClient.post(basePath, payload),

    update: (id, payload) => apiClient.put(`${basePath}/${id}`, payload),

    remove: (id) => apiClient.delete(`${basePath}/${id}`),
  };
}
