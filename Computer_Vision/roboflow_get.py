# 1. Import the library
from inference_sdk import InferenceHTTPClient

def roboflow_get(image_path,workflow):

    # 2. Connect to your workflow
    client = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="KQ2xn7sM4PtEodwyhs3J"
    )

    # 3. Run your workflow on an image
    result = client.run_workflow(
        workspace_name="sortware-solutions",
        workflow_id=workflow,
        images={
            "image": image_path # Path to your image file
        },
        use_cache=True # Speeds up repeated requests
    )

    # 4. Get your results
    return result
