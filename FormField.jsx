import "./forms.css";

function FormField({ field, value, onChange }) {
  const {
    name,
    label,
    field_type,
    is_required,
    help_text,
    options = [],
  } = field;

  const handleChange = (event) => {
    const rawValue =
      field_type === "boolean" ? event.target.checked : event.target.value;

    onChange(name, rawValue);
  };

  return (
    <div className="form-field">
      <label>
        {label}
        {is_required && <span className="required">*</span>}
      </label>

      {field_type === "long_text" ? (
        <textarea value={value || ""} onChange={handleChange} />
      ) : field_type === "select" ? (
        <select value={value || ""} onChange={handleChange}>
          <option value="">Seleccione...</option>
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      ) : field_type === "boolean" ? (
        <input type="checkbox" checked={Boolean(value)} onChange={handleChange} />
      ) : (
        <input
          type={field_type === "date" ? "date" : "text"}
          value={value || ""}
          onChange={handleChange}
        />
      )}

      {help_text && <small>{help_text}</small>}
    </div>
  );
}

export default FormField;
