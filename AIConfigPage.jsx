import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getProcesses,
  getDocumentTypes,
  getAIConfigurations,
  createAIConfiguration,
} from "./aiAdminApi.js";

import "../../../components/forms/forms.css";

const PURPOSES = [
  "extraction",
  "classification",
  "quality_review",
  "summary",
  "copilot",
];

function AIConfigPage() {
  const [processes, setProcesses] = useState([]);
  const [documentTypes, setDocumentTypes] = useState([]);
  const [configs, setConfigs] = useState([]);

  const [selectedProcessId, setSelectedProcessId] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    document_type_id: "",
    name: "",
    purpose: "extraction",
    instructions: "",
    expected_output: "",
    is_active: true,
  });

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
    }
  };

  const loadData = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const [typesResponse, configsResponse] = await Promise.all([
        getDocumentTypes(processId),
        getAIConfigurations({ process_id: processId }),
      ]);

      setDocumentTypes(typesResponse.data);
      setConfigs(configsResponse.data);
    } catch (err) {
      setError(err.message || "Error cargando configuración IA");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  useEffect(() => {
    loadData(selectedProcessId);
  }, [selectedProcessId]);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCreate = async (event) => {
    event.preventDefault();

    await createAIConfiguration({
      ...form,
      process_id: Number(selectedProcessId),
      document_type_id: form.document_type_id
        ? Number(form.document_type_id)
        : null,
    });

    setForm({
      document_type_id: "",
      name: "",
      purpose: "extraction",
      instructions: "",
      expected_output: "",
      is_active: true,
    });

    loadData(selectedProcessId);
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "name", label: "Nombre" },
    { key: "purpose", label: "Propósito" },
    { key: "document_type_id", label: "Tipo documento" },
    {
      key: "is_active",
      label: "Activa",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Configuración IA"
        description="Instrucciones, propósitos y salidas esperadas para extracción, clasificación, calidad y copiloto."
      />

      <Card title="Proceso">
        <div className="simple-form">
          <label>
            Proceso
            <select
              value={selectedProcessId}
              onChange={(event) => setSelectedProcessId(event.target.value)}
            >
              <option value="">Seleccione...</option>
              {processes.map((process) => (
                <option key={process.id} value={process.id}>
                  {process.name}
                </option>
              ))}
            </select>
          </label>
        </div>
      </Card>

      <Card title="Nueva configuración IA">
        <form onSubmit={handleCreate} className="simple-form">
          <label>
            Nombre
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Ej. Extracción de requerimiento recibido"
              required
            />
          </label>

          <label>
            Propósito
            <select
              name="purpose"
              value={form.purpose}
              onChange={handleChange}
            >
              {PURPOSES.map((purpose) => (
                <option key={purpose} value={purpose}>
                  {purpose}
                </option>
              ))}
            </select>
          </label>

          <label>
            Tipo de documento
            <select
              name="document_type_id"
              value={form.document_type_id}
              onChange={handleChange}
            >
              <option value="">General del proceso</option>
              {documentTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Instrucciones
            <textarea
              name="instructions"
              value={form.instructions}
              onChange={handleChange}
              placeholder="Explique cómo debe interpretar la IA este documento."
            />
          </label>

          <label>
            Salida esperada
            <textarea
              name="expected_output"
              value={form.expected_output}
              onChange={handleChange}
              placeholder='Ej. {"request_number":"","people":[],"request_items":[]}'
            />
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_active"
              checked={form.is_active}
              onChange={handleChange}
            />
            Activa
          </label>

          <div className="form-actions">
            <Button type="submit">Guardar configuración IA</Button>
          </div>
        </form>
      </Card>

      <Card title="Configuraciones IA">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={configs}
            emptyMessage="No hay configuraciones IA."
          />
        )}
      </Card>
    </>
  );
}

export default AIConfigPage;
