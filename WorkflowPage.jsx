import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getProcesses,
  getWorkflowStates,
  createWorkflowState,
  getWorkflowTransitions,
  createWorkflowTransition,
} from "./workflowAdminApi.js";

import "../../../components/forms/forms.css";

function WorkflowPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");

  const [states, setStates] = useState([]);
  const [transitions, setTransitions] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [stateForm, setStateForm] = useState({
    code: "",
    name: "",
    display_order: 0,
    color: "",
    is_initial: false,
    is_final: false,
    is_active: true,
  });

  const [transitionForm, setTransitionForm] = useState({
    code: "",
    name: "",
    from_state_id: "",
    to_state_id: "",
    requires_comment: false,
    requires_checklist_completed: false,
    is_active: true,
  });

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
    }
  };

  const loadWorkflow = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const [statesResponse, transitionsResponse] = await Promise.all([
        getWorkflowStates(processId),
        getWorkflowTransitions(processId),
      ]);

      setStates(statesResponse.data);
      setTransitions(transitionsResponse.data);
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
    loadWorkflow(selectedProcessId);
  }, [selectedProcessId]);

  const handleStateChange = (event) => {
    const { name, value, type, checked } = event.target;

    setStateForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleTransitionChange = (event) => {
    const { name, value, type, checked } = event.target;

    setTransitionForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCreateState = async (event) => {
    event.preventDefault();

    await createWorkflowState({
      ...stateForm,
      process_id: Number(selectedProcessId),
      display_order: Number(stateForm.display_order || 0),
    });

    setStateForm({
      code: "",
      name: "",
      display_order: 0,
      color: "",
      is_initial: false,
      is_final: false,
      is_active: true,
    });

    loadWorkflow(selectedProcessId);
  };

  const handleCreateTransition = async (event) => {
    event.preventDefault();

    await createWorkflowTransition({
      ...transitionForm,
      process_id: Number(selectedProcessId),
      from_state_id: Number(transitionForm.from_state_id),
      to_state_id: Number(transitionForm.to_state_id),
    });

    setTransitionForm({
      code: "",
      name: "",
      from_state_id: "",
      to_state_id: "",
      requires_comment: false,
      requires_checklist_completed: false,
      is_active: true,
    });

    loadWorkflow(selectedProcessId);
  };

  const getStateName = (stateId) => {
    const state = states.find((item) => item.id === stateId);
    return state ? state.name : stateId;
  };

  const stateColumns = [
    { key: "display_order", label: "Orden" },
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    { key: "color", label: "Color" },
    {
      key: "is_initial",
      label: "Inicial",
      render: (row) => (row.is_initial ? "Sí" : "No"),
    },
    {
      key: "is_final",
      label: "Final",
      render: (row) => (row.is_final ? "Sí" : "No"),
    },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
  ];

  const transitionColumns = [
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    {
      key: "from_state_id",
      label: "Desde",
      render: (row) => getStateName(row.from_state_id),
    },
    {
      key: "to_state_id",
      label: "Hasta",
      render: (row) => getStateName(row.to_state_id),
    },
    {
      key: "requires_comment",
      label: "Comentario",
      render: (row) => (row.requires_comment ? "Sí" : "No"),
    },
    {
      key: "requires_checklist_completed",
      label: "Checklist",
      render: (row) => (row.requires_checklist_completed ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Workflow"
        description="Configuración de estados y transiciones del proceso."
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

      {loading && <LoadingState />}
      {error && <ErrorState message={error} />}

      <Card title="Nuevo estado">
        <form onSubmit={handleCreateState} className="simple-form">
          <label>
            Código
            <input
              name="code"
              value={stateForm.code}
              onChange={handleStateChange}
              placeholder="ej. received"
              required
            />
          </label>

          <label>
            Nombre
            <input
              name="name"
              value={stateForm.name}
              onChange={handleStateChange}
              placeholder="ej. Recibido"
              required
            />
          </label>

          <label>
            Orden
            <input
              type="number"
              name="display_order"
              value={stateForm.display_order}
              onChange={handleStateChange}
            />
          </label>

          <label>
            Color
            <input
              name="color"
              value={stateForm.color}
              onChange={handleStateChange}
              placeholder="#2563eb"
            />
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_initial"
              checked={stateForm.is_initial}
              onChange={handleStateChange}
            />
            Estado inicial
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_final"
              checked={stateForm.is_final}
              onChange={handleStateChange}
            />
            Estado final
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_active"
              checked={stateForm.is_active}
              onChange={handleStateChange}
            />
            Activo
          </label>

          <div className="form-actions">
            <Button type="submit">Crear estado</Button>
          </div>
        </form>
      </Card>

      <Card title="Estados configurados">
        <DataTable
          columns={stateColumns}
          data={states}
          emptyMessage="No hay estados configurados."
        />
      </Card>

      <Card title="Nueva transición">
        <form onSubmit={handleCreateTransition} className="simple-form">
          <label>
            Código
            <input
              name="code"
              value={transitionForm.code}
              onChange={handleTransitionChange}
              placeholder="ej. send_to_area"
              required
            />
          </label>

          <label>
            Nombre
            <input
              name="name"
              value={transitionForm.name}
              onChange={handleTransitionChange}
              placeholder="ej. Enviar al área"
              required
            />
          </label>

          <label>
            Desde
            <select
              name="from_state_id"
              value={transitionForm.from_state_id}
              onChange={handleTransitionChange}
              required
            >
              <option value="">Seleccione...</option>
              {states.map((state) => (
                <option key={state.id} value={state.id}>
                  {state.name}
                </option>
              ))}
            </select>
          </label>

          <label>
            Hasta
            <select
              name="to_state_id"
              value={transitionForm.to_state_id}
              onChange={handleTransitionChange}
              required
            >
              <option value="">Seleccione...</option>
              {states.map((state) => (
                <option key={state.id} value={state.id}>
                  {state.name}
                </option>
              ))}
            </select>
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="requires_comment"
              checked={transitionForm.requires_comment}
              onChange={handleTransitionChange}
            />
            Requiere comentario
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="requires_checklist_completed"
              checked={transitionForm.requires_checklist_completed}
              onChange={handleTransitionChange}
            />
            Requiere checklist completo
          </label>

          <div className="form-actions">
            <Button type="submit">Crear transición</Button>
          </div>
        </form>
      </Card>

      <Card title="Transiciones configuradas">
        <DataTable
          columns={transitionColumns}
          data={transitions}
          emptyMessage="No hay transiciones configuradas."
        />
      </Card>
    </>
  );
}

export default WorkflowPage;
