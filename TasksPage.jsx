import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";

function TasksPage() {
  return (
    <>
      <PageHeader
        title="Tareas"
        description="Seguimiento de tareas asignadas, vencidas y completadas."
      />

      <Card title="Tareas">
        <p>Módulo de tareas pendiente de conectar.</p>
      </Card>
    </>
  );
}

export default TasksPage;
