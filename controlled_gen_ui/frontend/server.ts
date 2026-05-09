import { serve } from "@hono/node-server";
import {
  CopilotRuntime,
  createCopilotHonoHandler,
} from "@copilotkit/runtime/v2";
import { LangGraphHttpAgent } from "@ag-ui/langgraph";
// import { HttpAgent } from "@ag-ui/client";

const langGraphAgent = new LangGraphHttpAgent({
  url: process.env.LANGGRAPH_DEPLOYMENT_URL || "http://localhost:8000",
});

// const adkAgent = new HttpAgent({
//   url: process.env.ADK_DEPLOYMENT_URL || "http://localhost:8001",
// });

const runtime = new CopilotRuntime({
  agents: {
    default: langGraphAgent,
    // gemini: adkAgent,
  },
});

const app = createCopilotHonoHandler({
  runtime,
  basePath: "/api/copilotkit",
});

const server = serve(
  {
    fetch: app.fetch,
    port: 4002,
  },
  () => {
    console.log("CopilotKit API server running at http://localhost:4002");
  }
);

const shutdown = async (signal: string) => {
  console.log(`\nReceived ${signal}. Shutting down gracefully...`);

  try {
    // stop accepting new connections
    server.close(() => {
      console.log("HTTP server closed");
      process.exit(0);
    });

    // force exit if shutdown hangs
    setTimeout(() => {
      console.error("Forced shutdown");
      process.exit(1);
    }, 10000).unref();
  } catch (error) {
    console.error("Error during shutdown:", error);
    process.exit(1);
  }
};

process.on("SIGINT", () => shutdown("SIGINT"));
process.on("SIGTERM", () => shutdown("SIGTERM"));