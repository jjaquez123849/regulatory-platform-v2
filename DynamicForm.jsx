import { useState } from "react";

import Button from "../ui/Button.jsx";
import FormField from "./FormField.jsx";
import "./forms.css";

function DynamicForm({ fields = [], initialValues = {}, onSubmit, submitLabel = "Guardar" }) {
  const [values, setValues] = useState(initialValues);

  const handleChange = (name, value) => {
    setValues((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="dynamic-form-grid">
        {fields
          .filter((field) => field.is_visible !== false)
          .map((field) => (
            <FormField
              key={field.id || field.name}
              field={field}
              value={values[field.name]}
              onChange={handleChange}
            />
          ))}
      </div>

      <div className="form-actions">
        <Button type="submit">{submitLabel}</Button>
      </div>
    </form>
  );
}

export default DynamicForm;
