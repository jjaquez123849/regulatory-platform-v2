import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";

function RecordsPage() {
  return (
    <>
      <PageHeader
        title="Registros"
        description="Requerimientos/casos operativos generados por el workflow."
      />

      <Card title="Registros">
        <p>Módulo de registros pendiente de conectar.</p>
      </Card>
    </>
  );
}

export default RecordsPage;
