import os
import sys
from apps.stable_diffusion.src import get_available_devices
import glob
from pathlib import Path
from apps.stable_diffusion.src import args
from dataclasses import dataclass
import apps.stable_diffusion.web.utils.global_obj as global_obj
from apps.stable_diffusion.src.pipelines.pipeline_shark_stable_diffusion_utils import (
    SD_STATE_CANCEL,
)


@dataclass
class Config:
    mode: str
    model_id: str
    ckpt_loc: str
    precision: str
    batch_size: int
    max_length: int
    height: int
    width: int
    device: str
    use_lora: str
    use_stencil: str


custom_model_filetypes = (
    "*.ckpt",
    "*.safetensors",
)  # the tuple of file types

scheduler_list = [
    "DDIM",
    "PNDM",
    "DPMSolverMultistep",
    "EulerAncestralDiscrete",
]
scheduler_list_txt2img = [
    "DDIM",
    "PNDM",
    "LMSDiscrete",
    "KDPM2Discrete",
    "DPMSolverMultistep",
    "EulerDiscrete",
    "EulerAncestralDiscrete",
    "SharkEulerDiscrete",
]

predefined_models = [
    "Linaqruf/anything-v3.0",
    "prompthero/openjourney",
    "wavymulder/Analog-Diffusion",
    "stabilityai/stable-diffusion-2-1",
    "stabilityai/stable-diffusion-2-1-base",
    "CompVis/stable-diffusion-v1-4",
]

predefined_paint_models = [
    "runwayml/stable-diffusion-inpainting",
    "stabilityai/stable-diffusion-2-inpainting",
]
predefined_upscaler_models = [
    "stabilityai/stable-diffusion-x4-upscaler",
]


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(
        sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__))
    )
    return os.path.join(base_path, relative_path)


def get_custom_model_path():
    return Path(args.ckpt_dir) if args.ckpt_dir else Path(Path.cwd(), "models")


def get_custom_model_pathfile(custom_model_name):
    return os.path.join(get_custom_model_path(), custom_model_name)


def get_custom_model_files():
    ckpt_files = []
    for extn in custom_model_filetypes:
        files = [
            os.path.basename(x)
            for x in glob.glob(os.path.join(get_custom_model_path(), extn))
        ]
        ckpt_files.extend(files)
    return sorted(ckpt_files, key=str.casefold)


def cancel_sd():
    # Try catch it, as gc can delete global_obj.sd_obj while switching model
    try:
        global_obj.set_sd_status(SD_STATE_CANCEL)
    except Exception:
        pass


nodlogo_loc = resource_path("logos/nod-logo.png")
available_devices = get_available_devices()
