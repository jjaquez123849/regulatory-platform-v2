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
  getExtractionFields,
  createExtractionField,
  getExcelMappings,
  createExcelMapping,
} from "./documentTypesApi.js";

import "../../../components/forms/forms.css";

function DocumentTypesPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");
  const [documentTypes, setDocumentTypes] = useState([]);
  const [selectedDocumentType, setSelectedDocumentType] = useState(null);

  const [extractionFields, setExtractionFields] = useState([]);
  const [excelMappings, setExcelMappings] = useState([]);

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

  const [extractionForm, setExtractionForm] = useState({
    source_name: "",
    target_entity: "record",
    target_field: "",
    extraction_type: "ai",
    is_required: false,
    instructions: "",
  });

  const [excelForm, setExcelForm] = useState({
    sheet_name: "",
    header_row: 1,
    column_name: "",
    target_entity: "record",
    target_field: "",
    is_required: false,
  });

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
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

  const loadDocumentConfig = async (documentType) => {
    setSelectedDocumentType(documentType);

    const [extractionResponse, excelResponse] = await Promise.all([
      getExtractionFields(documentType.id),
      getExcelMappings(documentType.id),
    ]);

    setExtractionFields(extractionResponse.data);
    setExcelMappings(excelResponse.data);
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

  const handleExtractionChange = (event) => {
    const { name, value, type, checked } = event.target;
    setExtractionForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleExcelChange = (event) => {
    const { name, value, type, checked } = event.target;
    setExcelForm((current) => ({
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

  const handleCreateExtraction = async (event) => {
    event.preventDefault();

    await createExtractionField({
      ...extractionForm,
      document_type_id: selectedDocumentType.id,
    });

    setExtractionForm({
      source_name: "",
      target_entity: "record",
      target_field: "",
      extraction_type: "ai",
      is_required: false,
      instructions: "",
    });

    loadDocumentConfig(selectedDocumentType);
  };

  const handleCreateExcelMapping = async (event) => {
    event.preventDefault();

    await createExcelMapping({
      ...excelForm,
      document_type_id: selectedDocumentType.id,
      sheet_name: excelForm.sheet_name || null,
      header_row: Number(excelForm.header_row || 1),
    });

    setExcelForm({
      sheet_name: "",
      header_row: 1,
      column_name: "",
      target_entity: "record",
      target_field: "",
      is_required: false,
    });

    loadDocumentConfig(selectedDocumentType);
  };

  const documentColumns = [
    { key: "id", label: "ID" },
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    { key: "direction", label: "Dirección" },
    { key: "allowed_extensions", label: "Extensiones" },
    {
      key: "is_ai_enabled",
      label: "IA",
      render: (row) => (row.is_ai_enabled ? "Sí" : "No"),
    },
    {
      key: "actions",
      label: "Configurar",
      render: (row) => (
        <Button variant="secondary" onClick={() => loadDocumentConfig(row)}>
          Configurar
        </Button>
      ),
    },
  ];

  const extractionColumns = [
    { key: "source_name", label: "Fuente" },
    { key: "target_entity", label: "Entidad" },
    { key: "target_field", label: "Campo destino" },
    { key: "extraction_type", label: "Tipo" },
    {
      key: "is_required",
      label: "Obligatorio",
      render: (row) => (row.is_required ? "Sí" : "No"),
    },
  ];

  const excelColumns = [
    { key: "sheet_name", label: "Hoja" },
    { key: "header_row", label: "Fila encabezado" },
    { key: "column_name", label: "Columna Excel" },
    { key: "target_entity", label: "Entidad" },
    { key: "target_field", label: "Campo destino" },
    {
      key: "is_required",
      label: "Obligatorio",
      render: (row) => (row.is_required ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Tipos de documentos"
        description="Configuración documental, extracción IA y mapeos Excel."
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
              <input name="code" value={form.code} onChange={handleChange} required />
            </label>

            <label>
              Nombre
              <input name="name" value={form.name} onChange={handleChange} required />
            </label>

            <label>
              Dirección
              <select name="direction" value={form.direction} onChange={handleChange}>
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
            columns={documentColumns}
            data={documentTypes}
            emptyMessage="No hay tipos de documentos configurados."
          />
        )}
      </Card>

      {selectedDocumentType && (
        <>
          <Card title={`Campos de extracción: ${selectedDocumentType.name}`}>
            <form onSubmit={handleCreateExtraction} className="simple-form">
              <label>
                Nombre fuente
                <input
                  name="source_name"
                  value={extractionForm.source_name}
                  onChange={handleExtractionChange}
                  placeholder="ej. numero_requerimiento"
                  required
                />
              </label>

              <label>
                Entidad destino
                <select
                  name="target_entity"
                  value={extractionForm.target_entity}
                  onChange={handleExtractionChange}
                >
                  <option value="record">Record</option>
                  <option value="person">Persona</option>
                  <option value="request_item">Solicitud</option>
                </select>
              </label>

              <label>
                Campo destino
                <input
                  name="target_field"
                  value={extractionForm.target_field}
                  onChange={handleExtractionChange}
                  required
                />
              </label>

              <label>
                Tipo extracción
                <select
                  name="extraction_type"
                  value={extractionForm.extraction_type}
                  onChange={handleExtractionChange}
                >
                  <option value="ai">IA</option>
                  <option value="rule">Regla</option>
                  <option value="regex">Regex</option>
                </select>
              </label>

              <label>
                Instrucciones
                <textarea
                  name="instructions"
                  value={extractionForm.instructions}
                  onChange={handleExtractionChange}
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  name="is_required"
                  checked={extractionForm.is_required}
                  onChange={handleExtractionChange}
                />
                Obligatorio
              </label>

              <div className="form-actions">
                <Button type="submit">Agregar extracción</Button>
              </div>
            </form>

            <br />

            <DataTable
              columns={extractionColumns}
              data={extractionFields}
              emptyMessage="No hay campos de extracción configurados."
            />
          </Card>

          <Card title={`Mapeos Excel: ${selectedDocumentType.name}`}>
            <form onSubmit={handleCreateExcelMapping} className="simple-form">
              <label>
                Hoja
                <input
                  name="sheet_name"
                  value={excelForm.sheet_name}
                  onChange={handleExcelChange}
                  placeholder="Opcional"
                />
              </label>

              <label>
                Fila encabezado
                <input
                  type="number"
                  name="header_row"
                  value={excelForm.header_row}
                  onChange={handleExcelChange}
                />
              </label>

              <label>
                Columna Excel
                <input
                  name="column_name"
                  value={excelForm.column_name}
                  onChange={handleExcelChange}
                  required
                />
              </label>

              <label>
                Entidad destino
                <select
                  name="target_entity"
                  value={excelForm.target_entity}
                  onChange={handleExcelChange}
                >
                  <option value="record">Record</option>
                  <option value="person">Persona</option>
                  <option value="request_item">Solicitud</option>
                </select>
              </label>

              <label>
                Campo destino
                <input
                  name="target_field"
                  value={excelForm.target_field}
                  onChange={handleExcelChange}
                  required
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  name="is_required"
                  checked={excelForm.is_required}
                  onChange={handleExcelChange}
                />
                Obligatorio
              </label>

              <div className="form-actions">
                <Button type="submit">Agregar mapeo</Button>
              </div>
            </form>

            <br />

            <DataTable
              columns={excelColumns}
              data={excelMappings}
              emptyMessage="No hay mapeos Excel configurados."
            />
          </Card>
        </>
      )}
    </>
  );
}

export default DocumentTypesPage;
