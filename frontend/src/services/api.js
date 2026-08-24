import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export const predictSign = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
    "/predict",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get("/health");

  return response.data;
};

export const predictImageBlob = async (blob) => {
  const formData = new FormData();

  formData.append(
    "file",
    blob,
    "webcam-frame.jpg"
  );

  const response = await api.post(
    "/predict",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

export default api;