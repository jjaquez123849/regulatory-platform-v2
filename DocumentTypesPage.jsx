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
  createDocumentType,
} from "./documentTypesApi.js";

import "../../../components/forms/forms.css";

function DocumentTypesPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");
  const [documentTypes, setDocumentTypes] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    code: "",
    name: "",
    description: "",
    direction: "input",
    allowed_extensions: "pdf,msg,eml,docx,xlsx,xls,csv",
    is_required: false,
    is_ai_enabled: true,
  });

  const loadProcesses = async () => {
    try {
      const response = await getProcesses();
      setProcesses(response.data);

      if (response.data.length && !selectedProcessId) {
        setSelectedProcessId(String(response.data[0].id));
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const loadDocumentTypes = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const response = await getDocumentTypes(processId);
      setDocumentTypes(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  useEffect(() => {
    loadDocumentTypes(selectedProcessId);
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

    await createDocumentType({
      ...form,
      process_id: Number(selectedProcessId),
    });

    setForm({
      code: "",
      name: "",
      description: "",
      direction: "input",
      allowed_extensions: "pdf,msg,eml,docx,xlsx,xls,csv",
      is_required: false,
      is_ai_enabled: true,
    });

    setCreating(false);
    loadDocumentTypes(selectedProcessId);
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    { key: "direction", label: "Dirección" },
    { key: "allowed_extensions", label: "Extensiones" },
    {
      key: "is_required",
      label: "Obligatorio",
      render: (row) => (row.is_required ? "Sí" : "No"),
    },
    {
      key: "is_ai_enabled",
      label: "IA",
      render: (row) => (row.is_ai_enabled ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Tipos de documentos"
        description="Configuración documental, lectura IA y archivos esperados."
        actions={
          <Button onClick={() => setCreating((value) => !value)}>
            Nuevo documento
          </Button>
        }
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

      {creating && (
        <Card title="Nuevo tipo de documento">
          <form onSubmit={handleCreate} className="simple-form">
            <label>
              Código
              <input
                name="code"
                value={form.code}
                onChange={handleChange}
                placeholder="ej. requirement_document"
                required
              />
            </label>

            <label>
              Nombre
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="ej. Requerimiento recibido"
                required
              />
            </label>

            <label>
              Dirección
              <select
                name="direction"
                value={form.direction}
                onChange={handleChange}
              >
                <option value="input">Entrada</option>
                <option value="response">Respuesta</option>
                <option value="support">Soporte</option>
              </select>
            </label>

            <label>
              Extensiones permitidas
              <input
                name="allowed_extensions"
                value={form.allowed_extensions}
                onChange={handleChange}
                placeholder="pdf,msg,eml,xlsx"
              />
            </label>

            <label>
              Descripción
              <textarea
                name="description"
                value={form.description}
                onChange={handleChange}
              />
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_required"
                checked={form.is_required}
                onChange={handleChange}
              />
              Obligatorio
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_ai_enabled"
                checked={form.is_ai_enabled}
                onChange={handleChange}
              />
              IA habilitada
            </label>

            <div className="form-actions">
              <Button type="submit">Guardar documento</Button>
            </div>
          </form>
        </Card>
      )}

      <Card title="Tipos de documentos configurados">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {!loading && !error && (
          <DataTable
            columns={columns}
            data={documentTypes}
            emptyMessage="No hay tipos de documentos configurados."
          />
        )}
      </Card>
    </>
  );
}

export default DocumentTypesPage;
