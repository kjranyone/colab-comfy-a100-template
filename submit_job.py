import urllib.request
import json

BASE_URL = "https://cab-county-deferred-optional.trycloudflare.com"

# 正真正銘の嫌儲板原住民・けんもうくん （ヽ´ん`） プロンプト
KENMOU_PROMPT = (
    "A melancholic, pale, round-headed minimalist 2ch AA character Kenmou-kun `( ´ん\\` )`, "
    "having faint dark stubble, droopy resigned eyes, slouching in a dimly lit messy Japanese 4.5-tatami room. "
    "Suddenly glowing light from his old monitor displays 'Google Colab A100 GPU Video Generation Successful!'. "
    "His tired eyes tear up in deep, overwhelming emotion, muttering softly with trembling lips. "
    "Poignant cinematic anime lighting, rain hitting the window outside, 24fps atmospheric masterpiece animation."
)

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
            "prompt": KENMOU_PROMPT,
            "width": 1344,
            "height": 768,
            "length": 124
        }
    },
    # 7. Negative Conditioning
    "7": {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "handsome bishonen, western cartoon, high saturation glossy modern anime, 3d cgi render, blurry, distorted face, watermark",
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
            "seed": 20260924,
            "steps": 25,
            "cfg": 6.0,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1.0
        }
    },
    # 9. VAEDecode (Latent -> Frames)
    "9": {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["8", 0],
            "vae": ["3", 0]
        }
    },
    # 10. CreateVideo (Images -> Video Stream at 24fps)
    "10": {
        "class_type": "CreateVideo",
        "inputs": {
            "images": ["9", 0],
            "fps": 24.0
        }
    },
    # 11. SaveVideo (Output strictly to MP4)
    "11": {
        "class_type": "SaveVideo",
        "inputs": {
            "video": ["10", 0],
            "filename_prefix": "kenmou_true_aa_a100",
            "format": "mp4"
        }
    }
}

def queue():
    data = json.dumps({"prompt": prompt_data, "client_id": "agent_kenmou"}).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/prompt", data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            res_json = json.loads(res.read().decode())
            prompt_id = res_json.get("prompt_id")
            print(f"[SUCCESS] Authentic Kenmou-kun MP4 job queued on Colab A100! Prompt ID: {prompt_id}")
    except urllib.error.HTTPError as e:
        print("HTTP Error:", e.code, e.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    queue()
