import { useEffect, useState } from "react";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import Button from "../../components/ui/Button.jsx";
import DataTable from "../../components/table/DataTable.jsx";
import LoadingState from "../../components/feedback/LoadingState.jsx";
import ErrorState from "../../components/feedback/ErrorState.jsx";

import {
  getRecords,
  getTasks,
  createTask,
  updateTask,
} from "./tasksApi.js";

import "../../components/forms/forms.css";

function TasksPage() {
  const [records, setRecords] = useState([]);
  const [tasks, setTasks] = useState([]);

  const [creating, setCreating] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [form, setForm] = useState({
    record_id: "",
    title: "",
    description: "",
    assigned_to: "",
    assigned_area: "",
    priority: "medium",
    due_date: "",
    created_by: "user",
  });

  const loadData = async () => {
    try {
      setLoading(true);
      setError("");

      const [recordsResponse, tasksResponse] = await Promise.all([
        getRecords(),
        getTasks(),
      ]);

      setRecords(recordsResponse.data);
      setTasks(tasksResponse.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleCreate = async (event) => {
    event.preventDefault();

    await createTask({
      ...form,
      record_id: Number(form.record_id),
      due_date: form.due_date || null,
    });

    setForm({
      record_id: "",
      title: "",
      description: "",
      assigned_to: "",
      assigned_area: "",
      priority: "medium",
      due_date: "",
      created_by: "user",
    });

    setCreating(false);
    loadData();
  };

  const completeTask = async (taskId) => {
    await updateTask(taskId, {
      status: "completed",
      completed_by: "user",
    });

    loadData();
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "record_id", label: "Registro" },
    { key: "title", label: "Título" },
    { key: "assigned_area", label: "Área" },
    { key: "assigned_to", label: "Asignado" },
    { key: "status", label: "Estado" },
    { key: "priority", label: "Prioridad" },
    { key: "due_date", label: "Vence" },
    {
      key: "actions",
      label: "Acciones",
      render: (row) =>
        row.status !== "completed" ? (
          <Button variant="secondary" onClick={() => completeTask(row.id)}>
            Completar
          </Button>
        ) : (
          "Completada"
        ),
    },
  ];

  return (
    <>
      <PageHeader
        title="Tareas"
        description="Seguimiento de tareas asignadas, vencidas y completadas."
        actions={
          <Button onClick={() => setCreating((value) => !value)}>
            Nueva tarea
          </Button>
        }
      />

      {creating && (
        <Card title="Nueva tarea">
          <form onSubmit={handleCreate} className="simple-form">
            <label>
              Registro
              <select
                name="record_id"
                value={form.record_id}
                onChange={handleChange}
                required
              >
                <option value="">Seleccione...</option>
                {records.map((record) => (
                  <option key={record.id} value={record.id}>
                    #{record.id} - {record.title || "Sin título"}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Título
              <input
                name="title"
                value={form.title}
                onChange={handleChange}
                required
              />
            </label>

            <label>
              Área asignada
              <input
                name="assigned_area"
                value={form.assigned_area}
                onChange={handleChange}
              />
            </label>

            <label>
              Usuario asignado
              <input
                name="assigned_to"
                value={form.assigned_to}
                onChange={handleChange}
              />
            </label>

            <label>
              Prioridad
              <select
                name="priority"
                value={form.priority}
                onChange={handleChange}
              >
                <option value="low">Baja</option>
                <option value="medium">Media</option>
                <option value="high">Alta</option>
              </select>
            </label>

            <label>
              Fecha límite
              <input
                type="datetime-local"
                name="due_date"
                value={form.due_date}
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

            <div className="form-actions">
              <Button type="submit">Guardar tarea</Button>
            </div>
          </form>
        </Card>
      )}

      <Card title="Tareas">
        {loading && <LoadingState />}
        {error && <ErrorState message={error} />}

        {!loading && !error && (
          <DataTable
            columns={columns}
            data={tasks}
            emptyMessage="No hay tareas creadas."
          />
        )}
      </Card>
    </>
  );
}

export default TasksPage;
