import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";

function WorkflowPage() {
  return (
    <>
      <PageHeader
        title="Workflow"
        description="Configuración de estados y transiciones del proceso."
      />

      <Card title="Workflow">
        <p>Pendiente conectar con /admin/workflow-states y /admin/workflow-transitions.</p>
      </Card>
    </>
  );
}

export default WorkflowPage;
