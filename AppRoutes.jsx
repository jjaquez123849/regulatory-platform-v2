import { Routes, Route, Navigate } from "react-router-dom";

import AppShell from "../layout/AppShell.jsx";
import ProtectedRoute from "../../features/security/ProtectedRoute.jsx";
import LoginPage from "../../features/security/LoginPage.jsx";

import DashboardPage from "../../features/dashboard/DashboardPage.jsx";
import LogPage from "../../features/log/LogPage.jsx";
import RecordsPage from "../../features/records/RecordsPage.jsx";
import WorkspacePage from "../../features/workspace/WorkspacePage.jsx";
import DocumentsPage from "../../features/documents/DocumentsPage.jsx";
import DocumentUnderstandingPage from "../../features/documents/DocumentUnderstandingPage.jsx";
import ExtractionResultsPage from "../../features/extraction/ExtractionResultsPage.jsx";
import TasksPage from "../../features/tasks/TasksPage.jsx";
import QualityPage from "../../features/quality/QualityPage.jsx";
import NotificationsPage from "../../features/notifications/NotificationsPage.jsx";
import SystemDiagnosticsPage from "../../features/system/SystemDiagnosticsPage.jsx";

import AdminHomePage from "../../features/admin/AdminHomePage.jsx";
import ProcessesPage from "../../features/admin/processes/ProcessesPage.jsx";
import FieldsPage from "../../features/admin/fields/FieldsPage.jsx";
import DocumentTypesPage from "../../features/admin/documents/DocumentTypesPage.jsx";
import WorkflowPage from "../../features/admin/workflow/WorkflowPage.jsx";
import AutomationPage from "../../features/admin/automation/AutomationPage.jsx";
import AIConfigPage from "../../features/admin/ai/AIConfigPage.jsx";
import IAMPage from "../../features/admin/iam/IAMPage.jsx";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      <Route
        element={
          <ProtectedRoute>
            <AppShell />
          </ProtectedRoute>
        }
      >
        <Route path="/" element={<DashboardPage />} />
        <Route path="/log" element={<LogPage />} />
        <Route path="/records" element={<RecordsPage />} />
        <Route path="/records/:recordId/workspace" element={<WorkspacePage />} />

        <Route path="/documents" element={<DocumentsPage />} />
        <Route
          path="/documents/:documentId/understanding"
          element={<DocumentUnderstandingPage />}
        />
        <Route
          path="/documents/:documentId/extraction"
          element={<ExtractionResultsPage />}
        />

        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/quality" element={<QualityPage />} />
        <Route path="/notifications" element={<NotificationsPage />} />
        <Route path="/system" element={<SystemDiagnosticsPage />} />

        <Route path="/admin" element={<AdminHomePage />} />
        <Route path="/admin/processes" element={<ProcessesPage />} />
        <Route path="/admin/fields" element={<FieldsPage />} />
        <Route path="/admin/documents" element={<DocumentTypesPage />} />
        <Route path="/admin/workflow" element={<WorkflowPage />} />
        <Route path="/admin/automation" element={<AutomationPage />} />
        <Route path="/admin/ai" element={<AIConfigPage />} />
        <Route path="/admin/iam" element={<IAMPage />} />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default AppRoutes;
