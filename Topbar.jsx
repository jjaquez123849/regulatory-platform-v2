import { useNavigate } from "react-router-dom";

import Button from "../../components/ui/Button.jsx";
import { useAuth } from "../../features/security/AuthContext.jsx";

function Topbar() {
  const navigate = useNavigate();
  const { currentUser, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="topbar">
      <div>
        <strong>Centro de Operaciones</strong>
        <span> Plataforma configurable BPM + IA documental</span>
      </div>

      <div className="topbar-user">
        {currentUser && (
          <>
            <span>
              {currentUser.full_name || currentUser.username} · {currentUser.role}
            </span>

            <Button variant="secondary" onClick={handleLogout}>
              Salir
            </Button>
          </>
        )}
      </div>
    </header>
  );
}

export default Topbar;
