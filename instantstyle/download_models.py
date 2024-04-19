import torch
from huggingface_hub import hf_hub_download
from diffusers import ControlNetModel, StableDiffusionXLControlNetPipeline


def fetch_pretrained_model(model_class, model_name, **kwargs):
    """
    Fetches a pretrained model from Hugging Face hub.
    """
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return model_class.from_pretrained(model_name, **kwargs)
        except OSError as err:
            if attempt < max_retries - 1:
                print(
                    f"Error encountered: {err}. Retrying attempt {attempt + 1} of {max_retries}...")
            else:
                raise


def download_controlnet_canny_model():
    print("Downloading SDXL ControlNet Canny model...")
    return fetch_pretrained_model(
        ControlNetModel,
        "diffusers/controlnet-canny-sdxl-1.0",
        **{
            "torch_dtype": torch.float16,
            "use_safetensors": False
        }
    )


def download_sdxl_base_model(controlnet):
    print("Downloading SDXL base model...")
    return fetch_pretrained_model(
        StableDiffusionXLControlNetPipeline,
        "stabilityai/stable-diffusion-xl-base-1.0",
        **{
            "torch_dtype": torch.float16,
            "controlnet": controlnet,
            "add_watermarker": False
        }
    )


def download_ip_adapter_models():
    hf_hub_download(
        repo_id="h94/IP-Adapter",
        filename="sdxl_models/image_encoder/config.json",
        local_dir_use_symlinks=False,
        local_dir="./"
    )
    # Probably only either safetensors or bin are required but not both
    hf_hub_download(
        repo_id="h94/IP-Adapter",
        filename="sdxl_models/image_encoder/model.safetensors",
        local_dir_use_symlinks=False,
        local_dir="./"
    )
    hf_hub_download(
        repo_id="h94/IP-Adapter",
        filename="sdxl_models/image_encoder/pytorch_model.bin",
        local_dir_use_symlinks=False,
        local_dir="./"
    )
    hf_hub_download(
        repo_id="h94/IP-Adapter",
        filename="sdxl_models/ip-adapter_sdxl.bin",
        local_dir_use_symlinks=False,
        local_dir="./"
    )


if __name__ == '__main__':
    controlnet = download_controlnet_canny_model()
    sdxl = download_sdxl_base_model(controlnet)
    download_ip_adapter_models()
