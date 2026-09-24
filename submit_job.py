import urllib.request
import json
import time
import os

BASE_URL = "https://cab-county-deferred-optional.trycloudflare.com"

prompt_data = {
    # 1. UNET Loader (MiniMax-H3)
    "1": {
        "class_type": "UNETLoader",
        "inputs": {
            "unet_name": "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
            "weight_dtype": "default"
        }
    },
    # 2. CLIP Loader (Qwen3-VL 32B)
    "2": {
        "class_type": "CLIPLoader",
        "inputs": {
            "clip_name": "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
            "type": "minimax"
        }
    },
    # 3. Video VAE
    "3": {
        "class_type": "VAELoader",
        "inputs": {
            "vae_name": "minimax_h3_video_vae_fp16.safetensors"
        }
    },
    # 4. Audio VAE
    "4": {
        "class_type": "VAELoader",
        "inputs": {
            "vae_name": "minimax_h3_audio_vae_fp32.safetensors"
        }
    },
    # 5. Sigma Shift for MiniMax-H3
    "5": {
        "class_type": "MiniMaxH3SigmaShift",
        "inputs": {
            "model": ["1", 0],
            "shift_video": 12.0,
            "shift_audio": 3.0
        }
    },
    # 6. MiniMaxH3 Conditioning
    "6": {
        "class_type": "MiniMaxH3ImageToVideo",
        "inputs": {
            "clip": ["2", 0],
            "vae": ["3", 0],
            "prompt": "Kenmou-kun anime character crying comical tears of joy and shouting passionately: Google Colab can generate video on A100 GPU! Glowing laptop showing 100% GPU charts, dramatic camera zoom in, dynamic Japanese anime style, high production quality.",
            "width": 1344,
            "height": 768,
            "length": 124
        }
    },
    # 7. Negative Conditioning
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "blurry, low quality, distorted face, bad anatomy, static, watermark",
            "clip": ["2", 0]
        }
    },
    # 8. KSampler
    "8": {
        "class_type": "KSampler",
        "inputs": {
            "model": ["5", 0],
            "positive": ["6", 0],
            "negative": ["7", 0],
            "latent_image": ["6", 1],
            "seed": 42,
            "steps": 25,
            "cfg": 6.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0
        }
    },
    # 9. VAEDecode
    "9": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["8", 0],
            "vae": ["3", 0]
        }
    },
    # 10. SaveAnimatedWEBP
    "10": {
        "class_type": "SaveAnimatedWEBP",
        "inputs": {
            "images": ["9", 0],
            "filename_prefix": "kenmou_minimax_a100",
            "fps": 24.0,
            "lossless": False,
            "quality": 90,
            "method": "default"
        }
    }
}

data = json.dumps({"prompt": prompt_data, "client_id": "agent_kenmou"}).encode("utf-8")
req = urllib.request.Request(f"{BASE_URL}/prompt", data=data, headers={"Content-Type": "application/json"})

try:
    with urllib.request.urlopen(req, timeout=15) as res:
        res_json = json.loads(res.read().decode())
        prompt_id = res_json.get("prompt_id")
        print(f"[SUCCESS] Job successfully queued on Colab A100! Prompt ID: {prompt_id}")
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
except Exception as e:
    print("Error:", e)
