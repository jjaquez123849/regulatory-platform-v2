import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar.jsx";
import Topbar from "./Topbar.jsx";
import "./layout.css";

function AppShell() {
  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <Topbar />
        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default AppShell;
