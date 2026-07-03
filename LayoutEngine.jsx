import SectionEngine from "./SectionEngine.jsx";

function LayoutEngine({ layout = [] }) {
  if (!layout.length) {
    return (
      <p className="workspace-muted">
        No hay layout configurado para este Workspace.
      </p>
    );
  }

  return (
    <>
      {layout
        .filter((section) => section.visible !== false)
        .sort((a, b) => (a.order || 0) - (b.order || 0))
        .map((section, index) => (
          <SectionEngine
            key={section.id || section.code || index}
            section={section}
          />
        ))}
    </>
  );
}

export default LayoutEngine;
