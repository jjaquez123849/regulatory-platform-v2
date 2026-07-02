import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getExtractionResults,
  updateExtractionResult,
  applyExtractionResults,
  createLearningExample,
} from "./extractionApi.js";

import "../../components/forms/forms.css";

function ExtractionResultsPage() {
  const { documentId } = useParams();

  const [results, setResults] = useState([]);
  const [editingResult, setEditingResult] = useState(null);
  const [normalizedValue, setNormalizedValue] = useState("");
  const [status, setStatus] = useState("proposed");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const loadResults = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getExtractionResults(documentId);
      setResults(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResults();
  }, [documentId]);

  const openEdit = (row) => {
    setEditingResult(row);
    setNormalizedValue(row.normalized_value || row.extracted_value || "");
    setStatus(row.status || "proposed");
  };

  const handleSave = async (event) => {
    event.preventDefault();

    await updateExtractionResult(editingResult.id, {
      normalized_value: normalizedValue,
      status,
      reviewed_by: "user",
    });

    setEditingResult(null);
    setNormalizedValue("");
    setStatus("proposed");
    loadResults();
  };

  const handleApply = async () => {
    await applyExtractionResults(documentId);
    loadResults();
  };

  const handleLearn = async (row) => {
    await createLearningExample(row.id);
    loadResults();
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "target_entity", label: "Entidad" },
    { key: "target_field", label: "Campo" },
    { key: "extracted_value", label: "Extraído" },
    { key: "normalized_value", label: "Corregido" },
    { key: "source_row", label: "Fila" },
    { key: "source_column", label: "Columna" },
    { key: "confidence_score", label: "Conf." },
    { key: "status", label: "Estado" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) => (
        <div className="row-actions">
          <Button variant="secondary" onClick={() => openEdit(row)}>
            Revisar
          </Button>
          <Button variant="secondary" onClick={() => handleLearn(row)}>
            Aprender
          </Button>
        </div>
      ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Resultados de extracción"
        description={`Documento #${documentId}. Revise, corrija, apruebe y aplique los datos extraídos.`}
        actions={
          <Button onClick={handleApply}>
            Aplicar al registro
          </Button>
        }
      />

      {editingResult && (
        <Card title={`Revisar resultado #${editingResult.id}`}>
          <form onSubmit={handleSave} className="simple-form">
            <label>
              Valor extraído
              <textarea value={editingResult.extracted_value || ""} disabled />
            </label>

            <label>
              Valor corregido/aprobado
              <textarea
                value={normalizedValue}
                onChange={(event) => setNormalizedValue(event.target.value)}
              />
            </label>

            <label>
              Estado
              <select
                value={status}
                onChange={(event) => setStatus(event.target.value)}
              >
                <option value="proposed">Propuesto</option>
                <option value="approved">Aprobado</option>
                <option value="corrected">Corregido</option>
                <option value="rejected">Rechazado</option>
                <option value="applied">Aplicado</option>
              </select>
            </label>

            <div className="form-actions">
              <Button type="submit">Guardar revisión</Button>
            </div>
          </form>
        </Card>
      )}

      <Card title="Datos extraídos">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={results}
            emptyMessage="No hay resultados de extracción para este documento."
          />
        )}
      </Card>
    </>
  );
}

export default ExtractionResultsPage;
