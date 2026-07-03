import Card from "../ui/Card.jsx";
import "../forms/forms.css";

function SelectProcessCard({
  processes = [],
  selectedProcessId = "",
  onChange,
  title = "Proceso",
}) {
  return (
    <Card title={title}>
      <div className="simple-form">
        <label>
          Proceso
          <select
            value={selectedProcessId}
            onChange={(event) => onChange(event.target.value)}
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
  );
}

export default SelectProcessCard;
