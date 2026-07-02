import "./ui.css";

function Card({ title, children, actions }) {
  return (
    <section className="card">
      {(title || actions) && (
        <div className="card-header">
          {title && <h2>{title}</h2>}
          {actions && <div>{actions}</div>}
        </div>
      )}

      <div className="card-body">{children}</div>
    </section>
  );
}

export default Card;
