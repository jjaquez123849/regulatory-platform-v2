import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getRecords,
  getDocumentTypes,
  getDocuments,
  uploadDocument,
  processDocument,
} from "./documentsApi.js";

import "../../components/forms/forms.css";

function DocumentsPage() {
  const [records, setRecords] = useState([]);
  const [documentTypes, setDocumentTypes] = useState([]);
  const [documents, setDocuments] = useState([]);

  const [recordId, setRecordId] = useState("");
  const [documentTypeId, setDocumentTypeId] = useState("");
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [recordsResponse, typesResponse, documentsResponse] =
        await Promise.all([
          getRecords(),
          getDocumentTypes(),
          getDocuments(recordId),
        ]);

      setRecords(recordsResponse.data);
      setDocumentTypes(typesResponse.data);
      setDocuments(documentsResponse.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [recordId]);

  const handleUpload = async (event) => {
    event.preventDefault();

    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    if (recordId) {
      formData.append("record_id", recordId);
    }

    if (documentTypeId) {
      formData.append("document_type_id", documentTypeId);
    }

    formData.append("uploaded_by", "user");

    await uploadDocument(formData);

    setFile(null);
    loadData();
  };

  const handleProcess = async (documentId) => {
    await processDocument(documentId);
    loadData();
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "record_id", label: "Registro" },
    { key: "document_type_id", label: "Tipo" },
    { key: "original_filename", label: "Archivo" },
    { key: "file_extension", label: "Ext." },
    { key: "direction", label: "Dirección" },
    { key: "processing_status", label: "Estado" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) => (
        <Button variant="secondary" onClick={() => handleProcess(row.id)}>
          Procesar
        </Button>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Documentos"
        description="Carga, lectura y procesamiento documental."
      />

      <Card title="Cargar documento">
        <form onSubmit={handleUpload} className="simple-form">
          <label>
            Registro
            <select value={recordId} onChange={(event) => setRecordId(event.target.value)}>
              <option value="">Sin asociar</option>
              {records.map((record) => (
                <option key={record.id} value={record.id}>
                  #{record.id} - {record.title || "Sin título"}
                </option>
              ))}
            </select>
          </label>

          <label>
            Tipo de documento
            <select
              value={documentTypeId}
              onChange={(event) => setDocumentTypeId(event.target.value)}
            >
              <option value="">Seleccione...</option>
              {documentTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Archivo
            <input
              type="file"
              onChange={(event) => setFile(event.target.files[0])}
            />
          </label>

          <div className="form-actions">
            <Button type="submit">Cargar documento</Button>
          </div>
        </form>
      </Card>

      <Card title="Documentos cargados">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={documents}
            emptyMessage="No hay documentos cargados."
          />
        )}
      </Card>
    </>
  );
}

export default DocumentsPage;
