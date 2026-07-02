import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  ClipboardList,
  FileText,
  FolderOpen,
  CheckSquare,
  Settings
} from "lucide-react";

const navItems = [
  {
    label: "Dashboard",
    path: "/",
    icon: LayoutDashboard
  },
  {
    label: "Log",
    path: "/log",
    icon: ClipboardList
  },
  {
    label: "Registros",
    path: "/records",
    icon: FolderOpen
  },
  {
    label: "Documentos",
    path: "/documents",
    icon: FileText
  },
  {
    label: "Tareas",
    path: "/tasks",
    icon: CheckSquare
  },
  {
    label: "Administración",
    path: "/admin",
    icon: Settings
  }
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-mark">RP</div>
        <div>
          <strong>Regulatory</strong>
          <span>Platform V2</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                isActive ? "sidebar-link active" : "sidebar-link"
              }
            >
              <Icon size={18} />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}

export default Sidebar;
