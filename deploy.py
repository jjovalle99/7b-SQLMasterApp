import json
import os

import boto3
from dotenv import load_dotenv
from sagemaker.huggingface import (HuggingFaceModel,
                                   get_huggingface_llm_image_uri)

load_dotenv()


def main():
    iam = boto3.client("iam")
    role = iam.get_role(RoleName=os.getenv("ROLE"))["Role"]["Arn"]

    hub = {
        "HF_MODEL_ID": "jjovalle99/mistral7b-ft-lora-sql-v2",
        "SM_NUM_GPUS": json.dumps(1),
    }

    huggingface_model = HuggingFaceModel(
        image_uri=get_huggingface_llm_image_uri("huggingface", version="1.4.2"),
        env=hub,
        role=role,
    )

    huggingface_model.deploy(
        initial_instance_count=1,
        instance_type="ml.g5.2xlarge",
        container_startup_health_check_timeout=300,
    )


if __name__ == "__main__":
    main()
