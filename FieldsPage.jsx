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
  createFieldOption,
  getFieldOptions,
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

  const [selectedField, setSelectedField] = useState(null);
  const [fieldOptions, setFieldOptions] = useState([]);

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

  const [optionForm, setOptionForm] = useState({
    value: "",
    label: "",
    display_order: 0,
    is_active: true,
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

  const loadOptions = async (field) => {
    setSelectedField(field);

    if (!field) {
      setFieldOptions([]);
      return;
    }

    const response = await getFieldOptions(field.id);
    setFieldOptions(response.data);
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

  const handleOptionChange = (event) => {
    const { name, value, type, checked } = event.target;

    setOptionForm((current) => ({
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

  const handleCreateOption = async (event) => {
    event.preventDefault();

    if (!selectedField) return;

    await createFieldOption({
      field_id: selectedField.id,
      value: optionForm.value,
      label: optionForm.label,
      display_order: Number(optionForm.display_order || 0),
      is_active: optionForm.is_active,
    });

    setOptionForm({
      value: "",
      label: "",
      display_order: 0,
      is_active: true,
    });

    loadOptions(selectedField);
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
    {
      key: "actions",
      label: "Opciones",
      render: (row) =>
        ["select", "multi_select"].includes(row.field_type) ? (
          <Button variant="secondary" onClick={() => loadOptions(row)}>
            Opciones
          </Button>
        ) : (
          ""
        ),
    },
  ];

  const optionColumns = [
    { key: "display_order", label: "Orden" },
    { key: "value", label: "Valor" },
    { key: "label", label: "Etiqueta" },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
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

      {selectedField && (
        <Card title={`Opciones de ${selectedField.label}`}>
          <form onSubmit={handleCreateOption} className="simple-form">
            <label>
              Valor
              <input
                name="value"
                value={optionForm.value}
                onChange={handleOptionChange}
                required
              />
            </label>

            <label>
              Etiqueta
              <input
                name="label"
                value={optionForm.label}
                onChange={handleOptionChange}
                required
              />
            </label>

            <label>
              Orden
              <input
                type="number"
                name="display_order"
                value={optionForm.display_order}
                onChange={handleOptionChange}
              />
            </label>

            <label className="checkbox-row">
              <input
                type="checkbox"
                name="is_active"
                checked={optionForm.is_active}
                onChange={handleOptionChange}
              />
              Activo
            </label>

            <div className="form-actions">
              <Button type="submit">Agregar opción</Button>
            </div>
          </form>

          <br />

          <DataTable
            columns={optionColumns}
            data={fieldOptions}
            emptyMessage="Este campo aún no tiene opciones."
          />
        </Card>
      )}
    </>
  );
}

export default FieldsPage;
