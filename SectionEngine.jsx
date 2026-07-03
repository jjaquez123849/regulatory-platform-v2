import SectionCard from "../SectionCard.jsx";
import WorkspaceWidget from "./WorkspaceWidget.jsx";

function SectionEngine({ section }) {
  if (section.visible === false) {
    return null;
  }

  return (
    <SectionCard
      title={section.title}
      description={section.description}
    >
      {(section.widgets || []).map((widgetConfig, index) => (
        <WorkspaceWidget
          key={widgetConfig.id || widgetConfig.widget || index}
          widgetConfig={widgetConfig}
        />
      ))}
    </SectionCard>
  );
}

export default SectionEngine;
