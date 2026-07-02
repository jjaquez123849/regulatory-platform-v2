import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";

function DashboardPage() {
  return (
    <>
      <PageHeader
        title="Dashboard"
        description="Centro operativo de requerimientos, tareas, documentos y calidad."
      />

      <Card title="Resumen">
        <p>Dashboard operativo pendiente de conectar al backend.</p>
      </Card>
    </>
  );
}

export default DashboardPage;
