"""
ComfyUI Client & Agent Bridge for Google Colab + MiniMax-H3
Allows AI agents (or CLI scripts) to trigger video generation via Cloudflare Tunnel URL.
"""

import json
import time
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any


class ComfyUIColabClient:
    def __init__(self, base_url: str):
        """
        :param base_url: e.g. "https://xxxx.trycloudflare.com"
        """
        self.base_url = base_url.rstrip("/")

    def check_health(self) -> bool:
        """Checks if the ComfyUI endpoint is alive and responsive."""
        try:
            req = urllib.request.Request(f"{self.base_url}/system_stats")
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.status == 200
        except Exception as e:
            print(f"[Error] Failed to connect to {self.base_url}: {e}")
            return False

    def queue_prompt(self, workflow_prompt: Dict[str, Any], client_id: str = "agent-runner") -> Optional[str]:
        """
        Queues a ComfyUI prompt dictionary.
        Returns the prompt_id if successful.
        """
        data = json.dumps({"prompt": workflow_prompt, "client_id": client_id}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/prompt",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                result = json.loads(res.read().decode("utf-8"))
                return result.get("prompt_id")
        except Exception as e:
            print(f"[Error] Failed to queue prompt: {e}")
            return None

    def get_history(self, prompt_id: str) -> Optional[Dict[str, Any]]:
        """Fetches history for a given prompt_id."""
        url = f"{self.base_url}/history/{prompt_id}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as res:
                data = json.loads(res.read().decode("utf-8"))
                return data.get(prompt_id)
        except Exception:
            return None

    def wait_for_completion(self, prompt_id: str, poll_interval: int = 5, timeout: int = 600) -> Optional[Dict[str, Any]]:
        """Polls until the video generation is completed and returns outputs."""
        print(f"⏳ Waiting for generation job {prompt_id} to finish...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            if history and "outputs" in history:
                print("🎉 Generation completed successfully!")
                return history["outputs"]
            time.sleep(poll_interval)
        print("❌ Generation timed out.")
        return None

    def get_output_file_url(self, filename: str, subfolder: str = "", folder_type: str = "output") -> str:
        """Returns the public download URL for a generated video file."""
        query = urllib.parse.urlencode({
            "filename": filename,
            "subfolder": subfolder,
            "type": folder_type
        })
        return f"{self.base_url}/view?{query}"


def create_minimax_t2v_prompt(
    positive_prompt: str,
    negative_prompt: str = "distorted, low quality, watermark, glitch",
    width: int = 1280,
    height: int = 720,
    frames: int = 121,
    steps: int = 25,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Constructs an API-compatible prompt structure for MiniMax-H3 Text-to-Video.
    """
    return {
        "1": {
            "class_type": "UNETLoader",
            "inputs": {
                "unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
                "weight_dtype": "default"
            }
        },
        "2": {
            "class_type": "CLIPLoader",
            "inputs": {
                "clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
                "type": "minimax"
            }
        },
        "3": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "minimax_h3_video_vae_fp16.safetensors"
            }
        },
        "4": {
            "class_type": "VAELoader",
            "inputs": {
                "vae_name": "minimax_h3_audio_vae_fp32.safetensors"
            }
        },
        "5": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": positive_prompt,
                "clip": ["2", 0]
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": negative_prompt,
                "clip": ["2", 0]
            }
        },
        "7": {
            "class_type": "EmptyLatentVideo",
            "inputs": {
                "width": width,
                "height": height,
                "length": frames,
                "batch_size": 1
            }
        },
        "8": {
            "class_type": "KSampler",
            "inputs": {
                "model": ["1", 0],
                "positive": ["5", 0],
                "negative": ["6", 0],
                "latent_image": ["7", 0],
                "seed": seed,
                "steps": steps,
                "cfg": 6.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0
            }
        },
        "9": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["8", 0],
                "vae": ["3", 0]
            }
        },
        "10": {
            "class_type": "SaveVideo",
            "inputs": {
                "images": ["9", 0],
                "filename_prefix": "minimax_output"
            }
        }
    }
