import { Link } from "react-router-dom";

import PageHeader from "../../components/ui/PageHeader.jsx";
import Card from "../../components/ui/Card.jsx";
import "./admin.css";

function AdminHomePage() {
  return (
    <>
      <PageHeader
        title="Administración"
        description="Configuración sin código de procesos, campos, documentos, workflow, automatizaciones, IA e IAM."
      />

      <div className="admin-grid">
        <Card title="Procesos">
          <p>Crear y administrar procesos configurables.</p>
          <Link to="/admin/processes">Abrir procesos</Link>
        </Card>

        <Card title="Campos">
          <p>Configurar campos dinámicos del log y formularios.</p>
          <Link to="/admin/fields">Abrir campos</Link>
        </Card>

        <Card title="Documentos">
          <p>Configurar tipos de documentos, extracción IA y mapeos Excel.</p>
          <Link to="/admin/documents">Abrir documentos</Link>
        </Card>

        <Card title="Workflow">
          <p>Configurar estados y transiciones del proceso.</p>
          <Link to="/admin/workflow">Abrir workflow</Link>
        </Card>

        <Card title="Automatizaciones">
          <p>Configurar reglas: evento, condiciones y acciones automáticas.</p>
          <Link to="/admin/automation">Abrir automatizaciones</Link>
        </Card>

        <Card title="IA">
          <p>Configurar instrucciones, extracción, clasificación, calidad y copiloto.</p>
          <Link to="/admin/ai">Abrir configuración IA</Link>
        </Card>

        <Card title="IA Local Offline">
          <p>Configurar modelos locales descargados previamente y probarlos sin internet.</p>
          <Link to="/admin/local-ai">Abrir IA local</Link>
        </Card>

        <Card title="IAM">
          <p>Administrar usuarios, roles, permisos, capacidades, áreas y equipos.</p>
          <Link to="/admin/iam">Abrir IAM</Link>
        </Card>
      </div>
    </>
  );
}

export default AdminHomePage;
