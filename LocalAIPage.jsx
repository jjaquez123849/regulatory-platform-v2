import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import StatusBadge from "../../../components/ui/StatusBadge.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getLocalAIModels,
  createLocalAIModel,
  testLocalAI,
} from "./localAiApi.js";

import "../../../components/forms/forms.css";

function LocalAIPage() {
  const [models, setModels] = useState([]);
  const [selectedModelId, setSelectedModelId] = useState("");
  const [testPrompt, setTestPrompt] = useState("");
  const [testResult, setTestResult] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    name: "",
    engine_type: "rule_based",
    model_path: "",
    model_name: "",
    context_size: 4096,
    temperature: "0.2",
    is_default: true,
    is_active: true,
    notes: "",
  });

  const loadModels = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getLocalAIModels();
      setModels(response.data);

      const defaultModel = response.data.find((item) => item.is_default);
      if (defaultModel) {
        setSelectedModelId(String(defaultModel.id));
      }
    } catch (err) {
      setError(err.message || "Error cargando IA local");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadModels();
  }, []);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCreate = async (event) => {
    event.preventDefault();

    await createLocalAIModel({
      ...form,
      context_size: Number(form.context_size || 4096),
      model_path: form.model_path || null,
      model_name: form.model_name || null,
      notes: form.notes || null,
    });

    setForm({
      name: "",
      engine_type: "rule_based",
      model_path: "",
      model_name: "",
      context_size: 4096,
      temperature: "0.2",
      is_default: true,
      is_active: true,
      notes: "",
    });

    loadModels();
  };

  const handleTest = async (event) => {
    event.preventDefault();

    const response = await testLocalAI({
      prompt: testPrompt,
      model_id: selectedModelId ? Number(selectedModelId) : null,
    });

    setTestResult(response.data);
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "name", label: "Nombre" },
    { key: "engine_type", label: "Motor" },
    { key: "model_name", label: "Modelo" },
    { key: "model_path", label: "Ruta" },
    {
      key: "is_default",
      label: "Default",
      render: (row) => (row.is_default ? "Sí" : "No"),
    },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => <StatusBadge value={row.is_active ? "enabled" : "disabled"} />,
    },
  ];

  return (
    <>
      <PageHeader
        title="IA Local Offline"
        description="Configurar modelos locales descargados previamente. No requiere conexión a IA externa."
      />

      <Card title="Nuevo modelo local">
        <form onSubmit={handleCreate} className="simple-form">
          <label>
            Nombre
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Ej. Rule Based V1 / Mistral Local GGUF"
              required
            />
          </label>

          <label>
            Tipo de motor
            <select
              name="engine_type"
              value={form.engine_type}
              onChange={handleChange}
            >
              <option value="rule_based">rule_based</option>
              <option value="llama_cpp">llama_cpp / GGUF</option>
              <option value="ollama_local">ollama_local</option>
              <option value="transformers_local">transformers_local</option>
            </select>
          </label>

          <label>
            Ruta local del modelo
            <input
              name="model_path"
              value={form.model_path}
              onChange={handleChange}
              placeholder="C:\modelos\mistral.gguf"
            />
          </label>

          <label>
            Nombre del modelo
            <input
              name="model_name"
              value={form.model_name}
              onChange={handleChange}
              placeholder="mistral-7b-instruct / llama3 / etc."
            />
          </label>

          <label>
            Context size
            <input
              type="number"
              name="context_size"
              value={form.context_size}
              onChange={handleChange}
            />
          </label>

          <label>
            Temperatura
            <input
              name="temperature"
              value={form.temperature}
              onChange={handleChange}
            />
          </label>

          <label>
            Notas
            <textarea
              name="notes"
              value={form.notes}
              onChange={handleChange}
              placeholder="Detalles de instalación, modelo descargado, fecha, etc."
            />
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_default"
              checked={form.is_default}
              onChange={handleChange}
            />
            Modelo default
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_active"
              checked={form.is_active}
              onChange={handleChange}
            />
            Activo
          </label>

          <div className="form-actions">
            <Button type="submit">Guardar modelo local</Button>
          </div>
        </form>
      </Card>

      <Card title="Modelos configurados">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={models}
            emptyMessage="No hay modelos locales configurados."
          />
        )}
      </Card>

      <Card title="Probar IA local">
        <form onSubmit={handleTest} className="simple-form">
          <label>
            Modelo
            <select
              value={selectedModelId}
              onChange={(event) => setSelectedModelId(event.target.value)}
            >
              <option value="">Default</option>
              {models.map((model) => (
                <option key={model.id} value={model.id}>
                  {model.name} ({model.engine_type})
                </option>
              ))}
            </select>
          </label>

          <label>
            Prompt de prueba
            <textarea
              value={testPrompt}
              onChange={(event) => setTestPrompt(event.target.value)}
              placeholder="Resume este texto..."
              required
            />
          </label>

          <div className="form-actions">
            <Button type="submit">Probar</Button>
          </div>
        </form>

        {testResult && (
          <div className="workspace-summary-panel">
            <p>
              <strong>Motor:</strong> {testResult.engine_type}
            </p>
            <p>
              <strong>Disponible:</strong>{" "}
              {testResult.available ? "Sí" : "No"}
            </p>
            <p>
              <strong>Respuesta:</strong>
            </p>
            <p>{testResult.response}</p>
          </div>
        )}
      </Card>
    </>
  );
}

export default LocalAIPage;
