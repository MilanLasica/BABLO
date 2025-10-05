export interface WorkflowResponse {
  success: boolean;
  data?: any;
  imageUrl?: string;
  message?: string;
  error?: string;
}

export interface WorkflowPayload {
  [key: string]: any;
}

/**
 * Triggers the Modal workflow endpoint
 * @param payload - Optional payload to send to the workflow
 * @returns Promise with the workflow response
 */
export const triggerWorkflow = async (
  payload?: WorkflowPayload
): Promise<WorkflowResponse> => {
  const workflowUrl = import.meta.env.VITE_WORKFLOW_URL;

  if (!workflowUrl) {
    throw new Error(
      "Workflow URL is not configured. Please set VITE_WORKFLOW_URL in your .env file"
    );
  }

  try {
    const response = await fetch(workflowUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload || {}),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message ||
        errorData.error ||
        `Workflow request failed with status: ${response.status}`
      );
    }

    const data = await response.json();
    return {
      success: data.success !== false,
      data,
      imageUrl: data.imageUrl || data.image_url || data.url,
      message: data.message,
      error: data.error,
    };
  } catch (error) {
    console.error("Error triggering workflow:", error);
    throw error;
  }
};

// Legacy export for backwards compatibility
export const triggerN8nWorkflow = triggerWorkflow;
