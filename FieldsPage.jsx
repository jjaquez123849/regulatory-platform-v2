import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getProcesses,
  getProcessFields,
  createProcessField,
} from "./fieldsApi.js";

import "../../../components/forms/forms.css";

const FIELD_TYPES = [
  "text",
  "long_text",
  "number",
  "date",
  "datetime",
  "boolean",
  "select",
  "multi_select",
  "user",
  "email",
  "currency",
];

function FieldsPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");
  const [fields, setFields] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [creating, setCreating] = useState(false);
  const [form, setForm] = useState({
    name: "",
    label: "",
    field_type: "text",
    is_required: false,
    is_visible: true,
    is_editable: true,
    is_exportable: true,
    display_order: 0,
    help_text: "",
    default_value: "",
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

  const loadFields = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const response = await getProcessFields(processId);
      setFields(response.data);
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
    loadFields(selectedProcessId);
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

    await createProcessField({
      ...form,
      process_id: Number(selectedProcessId),
      display_order: Number(form.display_order || 0),
    });

    setForm({
      name: "",
      label: "",
      field_type: "text",
      is_required: false,
      is_visible: true,
      is_editable: true,
      is_exportable: true,
      display_order: 0,
      help_text: "",
      default_value: "",
    });

    setCreating(false);
    loadFields(selectedProcessId);
  };

  const columns = [
    { key: "display_order", label: "Orden" },
    { key: "name", label: "Nombre técnico" },
    { key: "label", label: "Etiqueta" },
    { key: "field_type", label: "Tipo" },
    {
      key: "is_required",
      label: "Obligatorio",
      render: (row) => (row.is_required ? "Sí" : "No"),
    },
    {
      key: "is_visible",
      label: "Visible",
      render: (row) => (row.is_visible ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Campos"
        description="Configuración de campos dinámicos para cada proceso."
        actions={
          <Button onClick={() => setCreating((value) => !value)}>
            Nuevo campo
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
        <Card title="Nuevo campo">
          <form onSubmit={handleCreate} className="simple-form">
            <label>
              Nombre técnico
              <input
                name="name"
                value={form.name}
                onChange={handleChange}
                placeholder="ej. request_number"
                required
              />
            </label>

            <label>
              Etiqueta
              <input
                name="label"
                value={form.label}
                onChange={handleChange}
                placeholder="ej. No. Requerimiento"
                required
              />
            </label>

            <label>
              Tipo
              <select
                name="field_type"
                value={form.field_type}
                onChange={handleChange}
              >
                {FIELD_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Orden
              <input
                type="number"
                name="display_order"
                value={form.display_order}
                onChange={handleChange}
              />
            </label>

            <label>
              Texto de ayuda
              <input
                name="help_text"
                value={form.help_text}
                onChange={handleChange}
              />
            </label>

            <label>
              Valor por defecto
              <input
                name="default_value"
                value={form.default_value}
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
                name="is_visible"
                checked={form.is_visible}
                onChange={handleChange}
              />
              Visible
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_editable"
                checked={form.is_editable}
                onChange={handleChange}
              />
              Editable
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_exportable"
                checked={form.is_exportable}
                onChange={handleChange}
              />
              Incluir en log
            </label>

            <div className="form-actions">
              <Button type="submit">Guardar campo</Button>
            </div>
          </form>
        </Card>
      )}

      <Card title="Campos configurados">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}
        {!loading && !error && (
          <DataTable
            columns={columns}
            data={fields}
            emptyMessage="No hay campos configurados para este proceso."
          />
        )}
      </Card>
    </>
  );
}

export default FieldsPage;
