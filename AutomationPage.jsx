import { useEffect, useState } from "react";

import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";
import Button from "../../../components/ui/Button.jsx";
import DataTable from "../../../components/table/DataTable.jsx";
import LoadingState from "../../../components/feedback/LoadingState.jsx";
import ErrorState from "../../../components/feedback/ErrorState.jsx";

import {
  getProcesses,
  getAutomationRules,
  createAutomationRule,
  getAutomationConditions,
  createAutomationCondition,
  getAutomationActions,
  createAutomationAction,
} from "./automationAdminApi.js";

import "../../../components/forms/forms.css";

const TRIGGERS = [
  "document_uploaded",
  "document_processed",
  "extraction_completed",
  "workflow_changed",
  "quality_completed",
  "quality_failed",
  "record_created",
  "record_updated",
  "button_executed",
];

const OPERATORS = [
  "equals",
  "not_equals",
  "contains",
  "not_contains",
  "is_empty",
  "is_not_empty",
  "starts_with",
  "ends_with",
  "in_list",
  "not_in_list",
];

const ACTION_TYPES = [
  "create_task",
  "execute_extraction",
  "apply_extraction",
  "execute_quality",
  "change_state",
  "send_notification",
];

function AutomationPage() {
  const [processes, setProcesses] = useState([]);
  const [selectedProcessId, setSelectedProcessId] = useState("");

  const [rules, setRules] = useState([]);
  const [selectedRule, setSelectedRule] = useState(null);
  const [conditions, setConditions] = useState([]);
  const [actions, setActions] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [ruleForm, setRuleForm] = useState({
    code: "",
    name: "",
    description: "",
    trigger_event: "document_uploaded",
    is_active: true,
  });

  const [conditionForm, setConditionForm] = useState({
    left_value: "",
    operator: "equals",
    right_value: "",
    display_order: 0,
    is_active: true,
  });

  const [actionForm, setActionForm] = useState({
    action_type: "create_task",
    action_payload: "",
    display_order: 0,
    is_active: true,
  });

  const loadProcesses = async () => {
    const response = await getProcesses();
    setProcesses(response.data);

    if (response.data.length && !selectedProcessId) {
      setSelectedProcessId(String(response.data[0].id));
    }
  };

  const loadRules = async (processId) => {
    if (!processId) return;

    try {
      setLoading(true);
      setError("");

      const response = await getAutomationRules(processId);
      setRules(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadRuleConfig = async (rule) => {
    setSelectedRule(rule);

    const [conditionsResponse, actionsResponse] = await Promise.all([
      getAutomationConditions(rule.id),
      getAutomationActions(rule.id),
    ]);

    setConditions(conditionsResponse.data);
    setActions(actionsResponse.data);
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  useEffect(() => {
    loadRules(selectedProcessId);
  }, [selectedProcessId]);

  const handleRuleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setRuleForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleConditionChange = (event) => {
    const { name, value, type, checked } = event.target;

    setConditionForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleActionChange = (event) => {
    const { name, value, type, checked } = event.target;

    setActionForm((current) => ({
      ...current,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCreateRule = async (event) => {
    event.preventDefault();

    await createAutomationRule({
      ...ruleForm,
      process_id: Number(selectedProcessId),
    });

    setRuleForm({
      code: "",
      name: "",
      description: "",
      trigger_event: "document_uploaded",
      is_active: true,
    });

    loadRules(selectedProcessId);
  };

  const handleCreateCondition = async (event) => {
    event.preventDefault();
    if (!selectedRule) return;

    await createAutomationCondition({
      ...conditionForm,
      rule_id: selectedRule.id,
      display_order: Number(conditionForm.display_order || 0),
    });

    setConditionForm({
      left_value: "",
      operator: "equals",
      right_value: "",
      display_order: 0,
      is_active: true,
    });

    loadRuleConfig(selectedRule);
  };

  const handleCreateAction = async (event) => {
    event.preventDefault();
    if (!selectedRule) return;

    await createAutomationAction({
      ...actionForm,
      rule_id: selectedRule.id,
      display_order: Number(actionForm.display_order || 0),
    });

    setActionForm({
      action_type: "create_task",
      action_payload: "",
      display_order: 0,
      is_active: true,
    });

    loadRuleConfig(selectedRule);
  };

  const ruleColumns = [
    { key: "id", label: "ID" },
    { key: "code", label: "Código" },
    { key: "name", label: "Nombre" },
    { key: "trigger_event", label: "Evento" },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
    {
      key: "actions",
      label: "Configurar",
      render: (row) => (
        <Button variant="secondary" onClick={() => loadRuleConfig(row)}>
          Configurar
        </Button>
      ),
    },
  ];

  const conditionColumns = [
    { key: "display_order", label: "Orden" },
    { key: "left_value", label: "Valor izquierdo" },
    { key: "operator", label: "Operador" },
    { key: "right_value", label: "Valor derecho" },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
  ];

  const actionColumns = [
    { key: "display_order", label: "Orden" },
    { key: "action_type", label: "Acción" },
    { key: "action_payload", label: "Payload" },
    {
      key: "is_active",
      label: "Activo",
      render: (row) => (row.is_active ? "Sí" : "No"),
    },
  ];

  return (
    <>
      <PageHeader
        title="Automatizaciones"
        description="Configure reglas del tipo: cuando ocurra un evento, si se cumplen condiciones, ejecutar acciones."
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

      <Card title="Nueva automatización">
        <form onSubmit={handleCreateRule} className="simple-form">
          <label>
            Código
            <input
              name="code"
              value={ruleForm.code}
              onChange={handleRuleChange}
              placeholder="ej. process_uploaded_document"
              required
            />
          </label>

          <label>
            Nombre
            <input
              name="name"
              value={ruleForm.name}
              onChange={handleRuleChange}
              placeholder="ej. Procesar documento cargado"
              required
            />
          </label>

          <label>
            Evento disparador
            <select
              name="trigger_event"
              value={ruleForm.trigger_event}
              onChange={handleRuleChange}
            >
              {TRIGGERS.map((trigger) => (
                <option key={trigger} value={trigger}>
                  {trigger}
                </option>
              ))}
            </select>
          </label>

          <label>
            Descripción
            <textarea
              name="description"
              value={ruleForm.description}
              onChange={handleRuleChange}
            />
          </label>

          <label className="checkbox-row">
            <input
              type="checkbox"
              name="is_active"
              checked={ruleForm.is_active}
              onChange={handleRuleChange}
            />
            Activa
          </label>

          <div className="form-actions">
            <Button type="submit">Crear automatización</Button>
          </div>
        </form>
      </Card>

      <Card title="Automatizaciones configuradas">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={ruleColumns}
            data={rules}
            emptyMessage="No hay automatizaciones configuradas."
          />
        )}
      </Card>

      {selectedRule && (
        <>
          <Card title={`Condiciones: ${selectedRule.name}`}>
            <form onSubmit={handleCreateCondition} className="simple-form">
              <label>
                Valor izquierdo
                <input
                  name="left_value"
                  value={conditionForm.left_value}
                  onChange={handleConditionChange}
                  placeholder="ej. document.file_extension"
                  required
                />
              </label>

              <label>
                Operador
                <select
                  name="operator"
                  value={conditionForm.operator}
                  onChange={handleConditionChange}
                >
                  {OPERATORS.map((operator) => (
                    <option key={operator} value={operator}>
                      {operator}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Valor derecho
                <input
                  name="right_value"
                  value={conditionForm.right_value}
                  onChange={handleConditionChange}
                  placeholder="ej. pdf"
                />
              </label>

              <label>
                Orden
                <input
                  type="number"
                  name="display_order"
                  value={conditionForm.display_order}
                  onChange={handleConditionChange}
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={conditionForm.is_active}
                  onChange={handleConditionChange}
                />
                Activa
              </label>

              <div className="form-actions">
                <Button type="submit">Agregar condición</Button>
              </div>
            </form>

            <br />

            <DataTable
              columns={conditionColumns}
              data={conditions}
              emptyMessage="Esta automatización no tiene condiciones."
            />
          </Card>

          <Card title={`Acciones: ${selectedRule.name}`}>
            <form onSubmit={handleCreateAction} className="simple-form">
              <label>
                Acción
                <select
                  name="action_type"
                  value={actionForm.action_type}
                  onChange={handleActionChange}
                >
                  {ACTION_TYPES.map((action) => (
                    <option key={action} value={action}>
                      {action}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Payload JSON
                <textarea
                  name="action_payload"
                  value={actionForm.action_payload}
                  onChange={handleActionChange}
                  placeholder='{"title":"Dar seguimiento","assigned_area":"CRIC","priority":"high"}'
                />
              </label>

              <label>
                Orden
                <input
                  type="number"
                  name="display_order"
                  value={actionForm.display_order}
                  onChange={handleActionChange}
                />
              </label>

              <label className="checkbox-row">
                <input
                  type="checkbox"
                  name="is_active"
                  checked={actionForm.is_active}
                  onChange={handleActionChange}
                />
                Activa
              </label>

              <div className="form-actions">
                <Button type="submit">Agregar acción</Button>
              </div>
            </form>

            <br />

            <DataTable
              columns={actionColumns}
              data={actions}
              emptyMessage="Esta automatización no tiene acciones."
            />
          </Card>
        </>
      )}
    </>
  );
}

export default AutomationPage;
