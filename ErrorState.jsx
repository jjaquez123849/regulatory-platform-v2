function ErrorState({ message = "Ocurrió un error." }) {
  return <div className="feedback-state error">{message}</div>;
}

export default ErrorState;
