import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";

function LogPage() {
  return (
    <>
      <PageHeader
        title="Log"
        description="Vista oficial de la base histórica. La base de datos es la única verdad."
      />

      <Card title="Log dinámico">
        <p>Vista del log pendiente de conectar a /log/process/&#123;process_id&#125;.</p>
      </Card>
    </>
  );
}

export default LogPage;
