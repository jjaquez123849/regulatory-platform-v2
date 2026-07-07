import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getRKFDocuments,
  getRKFDocument,
  getRKFRir,
  saveRKFRir,
  validateRKFRir,
} from "./rkfApi.js";

import "./rkf.css";

function RIRReviewPage() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState("");
  const [documentText, setDocumentText] = useState("");
  const [rir, setRir] = useState(null);

  const [activeTab, setActiveTab] = useState("request");
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [validation, setValidation] = useState(null);

  const loadDocuments = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getRKFDocuments();
      setDocuments(response.data || []);

      if (response.data?.length && !selectedDocumentId) {
        setSelectedDocumentId(response.data[0].document_id);
      }
    } catch (err) {
      setError(err.message || "Error cargando documentos RKF.");
    } finally {
      setLoading(false);
    }
  };

  const loadSelectedDocument = async (documentId) => {
    if (!documentId) return;

    try {
      setLoading(true);
      setError("");
      setMessage("");
      setValidation(null);

      const [documentResponse, rirResponse] = await Promise.all([
        getRKFDocument(documentId),
        getRKFRir(documentId),
      ]);

      setDocumentText(documentResponse.data.text || "");
      setRir(rirResponse.data);
    } catch (err) {
      setError(err.message || "Error cargando documento.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
    if (selectedDocumentId) {
      loadSelectedDocument(selectedDocumentId);
    }
  }, [selectedDocumentId]);

  const updatePath = (path, value) => {
    setRir((current) => {
      const copy = structuredClone(current);
      let target = copy;

      for (let i = 0; i < path.length - 1; i += 1) {
        target = target[path[i]];
      }

      target[path[path.length - 1]] = value;
      return copy;
    });
  };

  const addAuthority = () => {
    setRir((current) => ({
      ...current,
      authorities: [
        ...(current.authorities || []),
        {
          id: `auth_${Date.now()}`,
          name: "",
          authority_type: "REGULATOR",
          jurisdiction: "",
          country: "República Dominicana",
          role_in_request: "ISSUER",
          evidence_ids: [],
        },
      ],
    }));
  };

  const addParty = () => {
    setRir((current) => ({
      ...current,
      parties: [
        ...(current.parties || []),
        {
          id: `party_${Date.now()}`,
          party_type: "PERSON",
          name: "",
          name_variants: [],
          identifications: [],
          role: "SUBJECT_OF_REQUEST",
          is_customer_claimed_by_document: null,
          source_structure: "PARAGRAPH",
          extraction_notes: "",
          evidence_ids: [],
          confidence: 1,
          needs_review: false,
        },
      ],
    }));
  };

  const addRequestedItem = () => {
    setRir((current) => ({
      ...current,
      requested_items: [
        ...(current.requested_items || []),
        {
          id: `req_item_${Date.now()}`,
          item_type: "DOCUMENT",
          category: "OTHER",
          description: "",
          period: {
            start_date: null,
            end_date: null,
            raw_text: "",
          },
          related_party_ids: [],
          mandatory: true,
          requires_attachment: true,
          status: "REQUESTED",
          evidence_ids: [],
          confidence: 1,
          needs_review: false,
        },
      ],
    }));
  };

  const addEvidence = () => {
    setRir((current) => ({
      ...current,
      evidence: [
        ...(current.evidence || []),
        {
          id: `ev_${Date.now()}`,
          source_document_id: current.document?.id || selectedDocumentId,
          page_number: null,
          section: "",
          paragraph_index: null,
          line_index: null,
          raw_text: "",
          normalized_text: "",
          confidence: 1,
          extraction_method: "HUMAN_REVIEW",
          coordinates: null,
        },
      ],
    }));
  };

  const removeArrayItem = (arrayName, index) => {
    setRir((current) => ({
      ...current,
      [arrayName]: current[arrayName].filter((_, itemIndex) => itemIndex !== index),
    }));
  };

  const saveRir = async () => {
    if (!selectedDocumentId || !rir) return;

    try {
      setSaving(true);
      setError("");
      setMessage("");

      const response = await saveRKFRir(selectedDocumentId, rir);

      setValidation(response.data.validation);
      setMessage("RIR guardado correctamente.");
      await loadDocuments();
    } catch (err) {
      setError(err.message || "Error guardando RIR.");
    } finally {
      setSaving(false);
    }
  };

  const validateRir = async () => {
    if (!selectedDocumentId) return;

    try {
      setError("");
      setMessage("");

      const response = await validateRKFRir(selectedDocumentId);
      setValidation(response.data);
      setMessage("Validación ejecutada.");
    } catch (err) {
      setError(err.message || "Error validando RIR.");
    }
  };

  return (
    <>
      <PageHeader
        title="RIR Review Studio"
        description="Formulario temporal para construir conocimiento regulatorio sin editar JSON manualmente."
      />

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      <Card title="Documento de entrenamiento">
        <div className="rkf-toolbar">
          <select
            value={selectedDocumentId}
            onChange={(event) => setSelectedDocumentId(event.target.value)}
          >
            <option value="">Seleccione documento</option>
            {documents.map((doc) => (
              <option key={doc.document_id} value={doc.document_id}>
                {doc.document_id} {doc.has_reviewed_rir ? "✓" : ""}
              </option>
            ))}
          </select>

          <Button onClick={() => loadSelectedDocument(selectedDocumentId)}>
            Cargar
          </Button>

          <Button onClick={saveRir} disabled={saving || !rir}>
            {saving ? "Guardando..." : "Guardar RIR"}
          </Button>

          <Button variant="secondary" onClick={validateRir} disabled={!rir}>
            Validar
          </Button>
        </div>

        {message && <div className="rkf-message">{message}</div>}

        {validation && (
          <div className={validation.is_valid ? "rkf-valid" : "rkf-invalid"}>
            {validation.is_valid ? "RIR válido" : "RIR con errores"}
            {validation.errors?.length > 0 && (
              <ul>
                {validation.errors.map((item, index) => (
                  <li key={index}>
                    {item.path}: {item.message}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </Card>

      {rir && (
        <div className="rkf-layout">
          <Card title="Texto extraído">
            <pre className="rkf-text">{documentText}</pre>
          </Card>

          <Card title="Formulario RIR">
            <div className="rkf-tabs">
              <button onClick={() => setActiveTab("request")}>Request</button>
              <button onClick={() => setActiveTab("authorities")}>
                Autoridades
              </button>
              <button onClick={() => setActiveTab("parties")}>Partes</button>
              <button onClick={() => setActiveTab("items")}>Solicitudes</button>
              <button onClick={() => setActiveTab("evidence")}>Evidencias</button>
            </div>

            {activeTab === "request" && (
              <div className="rkf-form">
                <label>Referencia</label>
                <input
                  value={rir.request?.reference || ""}
                  onChange={(event) =>
                    updatePath(["request", "reference"], event.target.value)
                  }
                />

                <label>Propósito</label>
                <input
                  value={rir.request?.purpose || ""}
                  onChange={(event) =>
                    updatePath(["request", "purpose"], event.target.value)
                  }
                />

                <label>Resumen</label>
                <textarea
                  value={rir.request?.summary || ""}
                  onChange={(event) =>
                    updatePath(["request", "summary"], event.target.value)
                  }
                />

                <label>Fecha límite</label>
                <input
                  type="date"
                  value={rir.request?.deadline?.date || ""}
                  onChange={(event) =>
                    updatePath(["request", "deadline", "date"], event.target.value)
                  }
                />

                <label>Texto original de fecha límite</label>
                <input
                  value={rir.request?.deadline?.raw_text || ""}
                  onChange={(event) =>
                    updatePath(
                      ["request", "deadline", "raw_text"],
                      event.target.value
                    )
                  }
                />
              </div>
            )}

            {activeTab === "authorities" && (
              <div>
                <Button onClick={addAuthority}>Agregar autoridad</Button>

                {(rir.authorities || []).map((authority, index) => (
                  <div className="rkf-repeat-card" key={authority.id}>
                    <label>Nombre</label>
                    <input
                      value={authority.name || ""}
                      onChange={(event) =>
                        updatePath(
                          ["authorities", index, "name"],
                          event.target.value
                        )
                      }
                    />

                    <label>Tipo</label>
                    <select
                      value={authority.authority_type || "REGULATOR"}
                      onChange={(event) =>
                        updatePath(
                          ["authorities", index, "authority_type"],
                          event.target.value
                        )
                      }
                    >
                      <option value="REGULATOR">Regulador</option>
                      <option value="COURT">Juzgado / Tribunal</option>
                      <option value="PROSECUTOR">Ministerio Público</option>
                      <option value="TAX_AUTHORITY">Autoridad fiscal</option>
                      <option value="OTHER">Otro</option>
                    </select>

                    <label>Rol</label>
                    <select
                      value={authority.role_in_request || "ISSUER"}
                      onChange={(event) =>
                        updatePath(
                          ["authorities", index, "role_in_request"],
                          event.target.value
                        )
                      }
                    >
                      <option value="ISSUER">Emisor</option>
                      <option value="ORIGINATING_AUTHORITY">
                        Autoridad originadora
                      </option>
                      <option value="ACTING_AUTHORITY">Actúa por otro</option>
                      <option value="LEGAL_AUTHORITY">Autoridad legal</option>
                      <option value="UNKNOWN">Desconocido</option>
                    </select>

                    <Button
                      variant="secondary"
                      onClick={() => removeArrayItem("authorities", index)}
                    >
                      Eliminar
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "parties" && (
              <div>
                <Button onClick={addParty}>Agregar parte/persona</Button>

                {(rir.parties || []).map((party, index) => (
                  <div className="rkf-repeat-card" key={party.id}>
                    <label>Nombre</label>
                    <input
                      value={party.name || ""}
                      onChange={(event) =>
                        updatePath(["parties", index, "name"], event.target.value)
                      }
                    />

                    <label>Tipo</label>
                    <select
                      value={party.party_type || "PERSON"}
                      onChange={(event) =>
                        updatePath(
                          ["parties", index, "party_type"],
                          event.target.value
                        )
                      }
                    >
                      <option value="PERSON">Persona física</option>
                      <option value="COMPANY">Persona jurídica</option>
                      <option value="GOVERNMENT_ENTITY">
                        Entidad gubernamental
                      </option>
                      <option value="UNKNOWN">Desconocido</option>
                    </select>

                    <label>Rol</label>
                    <select
                      value={party.role || "SUBJECT_OF_REQUEST"}
                      onChange={(event) =>
                        updatePath(["parties", index, "role"], event.target.value)
                      }
                    >
                      <option value="SUBJECT_OF_REQUEST">
                        Sujeto del requerimiento
                      </option>
                      <option value="CUSTOMER">Cliente</option>
                      <option value="INVESTIGATED_PERSON">Investigado</option>
                      <option value="LEGAL_REPRESENTATIVE">
                        Representante legal
                      </option>
                      <option value="BENEFICIAL_OWNER">Beneficiario final</option>
                      <option value="RELATED_PARTY">Relacionado</option>
                      <option value="UNKNOWN">Desconocido</option>
                    </select>

                    <Button
                      variant="secondary"
                      onClick={() => removeArrayItem("parties", index)}
                    >
                      Eliminar
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "items" && (
              <div>
                <Button onClick={addRequestedItem}>Agregar solicitud</Button>

                {(rir.requested_items || []).map((item, index) => (
                  <div className="rkf-repeat-card" key={item.id}>
                    <label>Descripción</label>
                    <textarea
                      value={item.description || ""}
                      onChange={(event) =>
                        updatePath(
                          ["requested_items", index, "description"],
                          event.target.value
                        )
                      }
                    />

                    <label>Tipo</label>
                    <select
                      value={item.item_type || "DOCUMENT"}
                      onChange={(event) =>
                        updatePath(
                          ["requested_items", index, "item_type"],
                          event.target.value
                        )
                      }
                    >
                      <option value="DOCUMENT">Documento</option>
                      <option value="INFORMATION">Información</option>
                      <option value="ACTION">Acción</option>
                      <option value="EXPLANATION">Explicación</option>
                      <option value="REPORT">Reporte</option>
                      <option value="OTHER">Otro</option>
                    </select>

                    <label>Categoría</label>
                    <select
                      value={item.category || "OTHER"}
                      onChange={(event) =>
                        updatePath(
                          ["requested_items", index, "category"],
                          event.target.value
                        )
                      }
                    >
                      <option value="BANK_STATEMENT">Estados de cuenta</option>
                      <option value="ACCOUNT_MOVEMENTS">Movimientos</option>
                      <option value="CONTRACT">Contrato</option>
                      <option value="CUSTOMER_FILE">Expediente cliente</option>
                      <option value="BENEFICIAL_OWNER">Beneficiario final</option>
                      <option value="PRODUCT_LIST">Productos</option>
                      <option value="OTHER">Otro</option>
                    </select>

                    <Button
                      variant="secondary"
                      onClick={() => removeArrayItem("requested_items", index)}
                    >
                      Eliminar
                    </Button>
                  </div>
                ))}
              </div>
            )}

            {activeTab === "evidence" && (
              <div>
                <Button onClick={addEvidence}>Agregar evidencia</Button>

                {(rir.evidence || []).map((evidence, index) => (
                  <div className="rkf-repeat-card" key={evidence.id}>
                    <label>Texto evidencia</label>
                    <textarea
                      value={evidence.raw_text || ""}
                      onChange={(event) =>
                        updatePath(
                          ["evidence", index, "raw_text"],
                          event.target.value
                        )
                      }
                    />

                    <label>Página</label>
                    <input
                      type="number"
                      value={evidence.page_number || ""}
                      onChange={(event) =>
                        updatePath(
                          ["evidence", index, "page_number"],
                          event.target.value
                            ? Number(event.target.value)
                            : null
                        )
                      }
                    />

                    <Button
                      variant="secondary"
                      onClick={() => removeArrayItem("evidence", index)}
                    >
                      Eliminar
                    </Button>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      )}
    </>
  );
}

export default RIRReviewPage;
