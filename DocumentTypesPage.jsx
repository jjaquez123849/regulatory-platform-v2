import PageHeader from "../../../components/ui/PageHeader.jsx";
import Card from "../../../components/ui/Card.jsx";

function DocumentTypesPage() {
  return (
    <>
      <PageHeader
        title="Tipos de documentos"
        description="Configuración documental, extracción IA y mapeos Excel."
      />

      <Card title="Documentos">
        <p>Pendiente conectar con /admin/document-types.</p>
      </Card>
    </>
  );
}

export default DocumentTypesPage;
