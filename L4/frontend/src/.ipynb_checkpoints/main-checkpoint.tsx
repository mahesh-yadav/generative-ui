
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { CopilotKitProvider } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import { demonstrationCatalog } from "./catalog/renderers";
import "./globals.css";
import App from "./App";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <main className="h-screen w-screen">
      <CopilotKitProvider
        runtimeUrl="/api/copilotkit"
        useSingleEndpoint={false}
        a2ui={{ catalog: demonstrationCatalog }}
      >
        <App />
      </CopilotKitProvider>
    </main>
  </StrictMode>,
);
