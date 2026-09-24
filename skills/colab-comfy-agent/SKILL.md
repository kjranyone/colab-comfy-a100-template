---
name: colab-comfy-agent
description: Automates or interacts with Google Colab ComfyUI A100 instances to trigger MiniMax-H3 video generation via API or headless browser.
---

# Colab ComfyUI Video Agent Skill

This skill allows agents to operate or trigger video generation tasks using Google Colab running ComfyUI on an A100 GPU instance.

## Execution Patterns

### Pattern 1: Direct API Call via Cloudflare Tunnel
When the Colab notebook is already running and has outputted a `trycloudflare.com` URL:
1. Initialize the client using `client.py`:
   ```python
   from client import ComfyUIColabClient, create_minimax_t2v_prompt

   client = ComfyUIColabClient(base_url="https://your-tunnel.trycloudflare.com")
   prompt_dict = create_minimax_t2v_prompt("A cinematic shot of a futuristic cyberpunk city at night with neon lights, 4k, photorealistic")
   prompt_id = client.queue_prompt(prompt_dict)
   outputs = client.wait_for_completion(prompt_id)
   ```
2. Download or view generated output video.

### Pattern 2: Browser Automation (Headless Browser)
If the user wants complete end-to-end automation from spinning up Colab to video creation:
1. Open Google Colab URL with Playwright / Chrome DevTools:
   `https://colab.research.google.com/github/kjranyone/colab-comfy-a100-template/blob/main/colab_comfy_minimax_h3_a100.ipynb`
2. Select runtime: **Change runtime type** -> **A100 GPU**.
3. Trigger **Run all cells** (`Ctrl+F9`).
4. Read the stdout of Step 4 to extract the `trycloudflare.com` tunnel URL.
5. Send generation request via API or directly interact with the ComfyUI web UI.
