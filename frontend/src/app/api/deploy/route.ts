import { NextRequest } from "next/server";
import { firestore } from "@/lib/firebase";
import { doc, getDoc } from "firebase/firestore";

export async function POST(req: NextRequest) {
  try {
    console.log("Deploy API - Starting workflow execution...");
    const body = await req.json();
    const { query, userId, projectId } = body || {};

    console.log("Deploy API - Request params:", { query, userId, projectId });

    if (!query || typeof query !== "string") {
      console.error("Deploy API - Missing query");
      return new Response(JSON.stringify({ error: "query is required" }), {
        status: 400,
      });
    }

    if (!userId || typeof userId !== "string") {
      console.error("Deploy API - Missing userId");
      return new Response(JSON.stringify({ error: "userId is required" }), {
        status: 400,
      });
    }

    if (!projectId || typeof projectId !== "string") {
      console.error("Deploy API - Missing projectId");
      return new Response(JSON.stringify({ error: "projectId is required" }), {
        status: 400,
      });
    }

    // Get the builtWorkflow from Firebase
    console.log("Deploy API - Fetching builtWorkflow from Firebase...");
    let builtWorkflow: any;
    try {
      const projectRef = doc(firestore, "users", userId, "projects", projectId);
      const projectSnap = await getDoc(projectRef);

      if (!projectSnap.exists()) {
        console.error("Deploy API - Project not found");
        return new Response(JSON.stringify({ error: "Project not found" }), {
          status: 404,
        });
      }

      builtWorkflow = projectSnap.data()?.builtWorkflow;

      if (!builtWorkflow) {
        console.error("Deploy API - Workflow not built yet");
        return new Response(
          JSON.stringify({
            error: "Workflow not built yet. Please click 'Build' first.",
          }),
          { status: 400 },
        );
      }
      
      console.log("Deploy API - Built workflow retrieved from Firebase");
    } catch (firebaseErr: any) {
      console.error("Deploy API - Firebase error:", firebaseErr);
      return new Response(
        JSON.stringify({
          error: "Failed to fetch workflow from Firebase",
          message: firebaseErr?.message || String(firebaseErr),
        }),
        { status: 500 },
      );
    }

    const FACTORY_URL =
      process.env.FACTORY_URL ||
      "https://coral-factory-540229907345.europe-west1.run.app";
    const FACTORY_TOKEN = process.env.FACTORY_TOKEN || "bearer-token-2024";

    // Payload for factory /run/workflow/local endpoint
    const payload = {
      workflow_config: builtWorkflow,
      user_id: userId,
      user_task: query,
    };

    console.log("Deploy API - Calling factory run endpoint:", FACTORY_URL);
    console.log("Deploy API - Payload:", JSON.stringify(payload, null, 2));

    const res = await fetch(`${FACTORY_URL}/run/workflow/local`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${FACTORY_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    console.log("Deploy API - Factory response status:", res.status);

    const text = await res.text();
    console.log("Deploy API - Factory response text:", text);
    
    let data: any = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = { raw: text };
    }

    if (!res.ok) {
      console.error("Deploy API - Factory run failed:", { status: res.status, data });
      return new Response(
        JSON.stringify({
          error: "Factory run failed",
          status: res.status,
          data,
        }),
        { status: 502 },
      );
    }

    console.log("Deploy API - Workflow started successfully! trace_id:", data?.trace_id);
    
    // Poll for the result
    const traceId = data?.trace_id;
    if (traceId) {
      console.log("Deploy API - Polling for result...");
      let pollCount = 0;
      const maxPolls = 60; // 60 seconds max (increased for multi-agent workflows)
      
      while (pollCount < maxPolls) {
        await new Promise((resolve) => setTimeout(resolve, 1000)); // Wait 1 second
        
        try {
          const statusRes = await fetch(`${FACTORY_URL}/workflow/result/${traceId}`, {
            headers: {
              Authorization: `Bearer ${FACTORY_TOKEN}`,
            },
          });
          
          if (statusRes.ok) {
            const statusData = await statusRes.json();
            console.log("Deploy API - Poll response:", statusData);
            
            if (statusData.status === "not_completed" || statusData.status === "not_found") {
              pollCount++;
              continue;
            }
            
            if (statusData.result) {
              console.log("Deploy API - Got result:", statusData.result);
              return new Response(JSON.stringify({ 
                success: true, 
                data: { 
                  trace_id: traceId,
                  result: statusData.result 
                } 
              }), {
                status: 200,
              });
            }
          }
        } catch (pollErr) {
          console.error("Deploy API - Poll error:", pollErr);
        }
        
        pollCount++;
      }
      
      console.log("Deploy API - Timeout waiting for result");
      return new Response(JSON.stringify({ 
        success: true, 
        data: { 
          trace_id: traceId,
          result: "Workflow started but result not ready yet. Check traces panel."
        } 
      }), {
        status: 200,
      });
    }
    
    return new Response(JSON.stringify({ success: true, data }), {
      status: 200,
    });
  } catch (err: any) {
    console.error("Deploy API - Internal error:", err);
    return new Response(
      JSON.stringify({
        error: "Internal error",
        message: err?.message || String(err),
      }),
      { status: 500 },
    );
  }
}
