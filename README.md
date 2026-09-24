# Google Colab A100 ComfyUI & MiniMax-H3 Template

Google Colab 上で **A100 GPU (40GB VRAM)** を利用し、**ComfyUI 最新版** と最新の動画・音声統合生成モデル **MiniMax-H3 (Hailuo)** をワンクリックで動かすための実証・実行用テンプレートです。

Google One AI Premium / Google AI Pro 等のプランで付与される月間 200 Compute Units (CU) のリソース枠を活用し、誰でもコスト効率良く高品質な動画生成を試すことができます。

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kjranyone/colab-comfy-a100-template/blob/main/colab_comfy_minimax_h3_a100.ipynb)

---

## 🌟 主な特徴

- **Colab A100 (40GB VRAM) 最適化**
  - 高精度な動画生成モデル MiniMax-H3（および Qwen3-VL テキストエンコーダー、Audio/Video VAE）をVRAM不足なく安定ロード。
- **最新 ComfyUI ネイティブ対応**
  - ComfyUI v0.3.0+ のネイティブ MiniMax-H3 ノードをサポート。
  - ComfyUI-Manager を同梱。
- **Cloudflare Tunnel による無料・即時 WebUI 接続**
  - ngrok のトークン取得等の煩わしい初期設定が不要。
  - 実行すると `trycloudflare.com` のセキュアな一時 URL が自動発行され、ブラウザからワンクリックで ComfyUI に接続可能。
- **Google Drive 永続キャッシュ対応**
  - 初回ダウンロードしたモデル（約20GB）を Google Drive（`MyDrive/ComfyUI_Models/`）に自動保存。
  - 2回目以降のセッションではダウンロードが自動スキップされ、**起動待ち時間が 0 秒** に短縮されます。
- **モデル自動ダウンロード**
  - Hugging Face (`Comfy-Org/MiniMax-H3`) から推奨される量子化/高効率モデル (`int8_convrot`) を自動ダウンロード。

---

## 🚀 クイックスタート

1. 上の **[Open In Colab]** バッジをクリックしてノートブックを開きます。
2. Colab の上部メニューから **「ランタイム」 > 「ランタイムのタイプを変更」** を開き、ハードウェア アクセラレータで **「A100 GPU」** を選択します。
3. セルを上から順に実行します (`Shift + Enter` または「すべてのセルを実行」)。
4. Step 4 の出力欄に表示される `https://xxxx.trycloudflare.com` をクリックして ComfyUI を開きます。

---

## 🎨 MiniMax-H3 ワークフローの実行方法

1. ComfyUI 画面内のメニューから **「Templates」** (ワークフロー一覧) を選択。
2. **「Video」** カテゴリ内の **MiniMax H3 Text-to-Video** または **Image-to-Video** を読み込みます。
3. 本ノートブックでダウンロードした以下の各モデルが自動認識されます：
   - **Diffusion Model**: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
   - **Text Encoder**: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
   - **Video VAE**: `minimax_h3_video_vae_fp16.safetensors`
   - **Audio VAE**: `minimax_h3_audio_vae_fp32.safetensors`
4. プロンプトを入力して **「Queue Prompt」** を押せば、動画とステレオ音声が同時に生成されます。

---

## ⏱️ Compute Units (CU) 付与と消費のエビデンス

### 1. Google AI Pro プランでの 200 CU 付与について
- **提供開始時期**: 2026年9月下旬より、Google AIプラン（Google AI Pro等、月額約20ドル帯）の有料サブスクライバー向けに、**月間 200 Compute Units (CU)** の Colab 特典が正式にバンドル提供開始されました。
- **適用条件**:
  - 有料の Google AI プラン契約中の Google アカウントに対して自動適用されます。
  - 通常の Google One ストレージ専用プランや、無料トライアル期間中は付与対象外です。
  - Colab 画面右上のリソースパネルや、設定メニュー（`Settings` > `Subscription`）から「200 units」が付与されていることを確認できます。

### 2. A100 GPU インスタンスの CU 消費レート
Google Colab の動的リソース消費レート（実測値・目安）は以下の通りです：
- **A100 標準インスタンス (Standard RAM)**: 約 **5.37 CU / 時間**
- **A100 ハイメモリ (High-RAM)**: 約 **7.52 CU / 時間**
  *(※需給やインスタンス種別により約 5〜13 CU/時 の間で推移します)*

### 3. 月間 200 CU で可能な稼働時間
- **標準 A100 (~5.37 CU/h)**: 月間 **約 37 時間** 稼働可能
- **ハイメモリ A100 (~7.52 CU/h)**: 月間 **約 26 時間** 稼働可能
- MiniMax-H3 での 5秒〜10秒 の動画生成（1回あたり数分）であれば、**月間数百本以上の動画生成検証**が十分カバーできる計算になります。

### 4. Compute Units (CU) の残高確認方法
- **画面上のリソースバー**: ノートブック右上の「RAM / ディスク」表示をクリックすると、現在の「消費レート (CU/時)」と「残りCU残高」がリアルタイム表示されます。
- **アカウント設定画面**: Colab のメニュー `設定` > `サブスクリプション` または [Colab サブスクリプション管理ページ](https://colab.research.google.com/signup) を開くと、「現在、〇〇 ユニット」と有効期限（付与後90日間）が確認できます。

---

## ⚠️ シャットダウンとアイドル切断の仕組み（CUの無駄遣い防止）

Google Colab インスタンス（A100）が切断・停止されるタイミングと条件は以下の通りです。

| 切断トリガー | 停止条件 / 目安時間 | 詳細と対策 |
| :--- | :--- | :--- |
| **① アイドルタイムアウト (Idle Timeout)** | **約 90 分** | ブラウザの Colab タブを閉じた場合や、ブラウザでの操作が完全に途絶えた状態で放置された場合に自動終了します。<br>※注意: Step 4 のようにセルが実行中のままだと、ブラウザを開いている限りアイドル判定にならず CU を消費し続けます。 |
| **② 最長連続実行時間 (Max Lifetime)** | **最長 12 時間**（上位プランで24時間） | 処理が動き続けていても、Colab 側の制約で最長12時間程度で強制リセットされます。 |
| **③ Compute Units の枯渇** | **残高 0 になった瞬間** | CU 残高がゼロになると即座に GPU 割り当てが解除されます。 |
| **④ 手動 / プログラム終了** | **即時** | セッション完了後、以下の方法で明示的に停止するのが最も安全です。 |

### 💡 生成終了後に自動でシャットダウンさせる方法 (Python)
放置による CU 消費を防ぐため、バッチ生成やエージェント連携の最後に以下のコードを実行することで、ノートブックを自動シャットダウン（VM解放）できます：

```python
from google.colab import runtime
# インスタンスを安全に切断・削除して CU の消費を即座にストップ
runtime.unassign()
```

---

## 🤖 エージェント統合・API 呼び出し (Headless / API Bridge)

「ユーザーが Colab の画面を手動で操作しなくても、AI エージェントがこのリポジトリを読んで自動で動画生成を行える」構成をサポートしています。

### 1. Python SDK / Client 経由でエージェントから呼ぶ ([`client.py`](file:///C:/lib/github/kjranyone/colab-comfy-a100-template/client.py))
Colab で起動した Cloudflare Tunnel URL を渡すだけで、エージェントがプログラムから MiniMax-H3 を呼び出し、動画の生成待機と URL 取得までを自動化できます。

```python
from client import ComfyUIColabClient, create_minimax_t2v_prompt

# Tunnel URL を指定
client = ComfyUIColabClient(base_url="https://xxxx.trycloudflare.com")

# プロンプト定義
prompt = create_minimax_t2v_prompt(
    positive_prompt="Cyberpunk robot walking in rain, cinematic lighting, 4k",
    frames=121
)

# ジョブの投入と完了待ち
prompt_id = client.queue_prompt(prompt)
outputs = client.wait_for_completion(prompt_id)
print("Generated video:", outputs)
```

### 2. ブラウザ自動化（Browser Agent）による完全自律起動
Playwright などのブラウザエージェントを用いることで、Colab の立ち上げからトンネル URL の抽出までを完全無人化できます：
1. エージェントが Colab URL（[Open In Colab](https://colab.research.google.com/github/kjranyone/colab-comfy-a100-template/blob/main/colab_comfy_minimax_h3_a100.ipynb)）にブラウザでアクセス。
2. ランタイムタイプを「A100 GPU」に切り替えて「すべてのセルを実行」。
3. Step 4 の出力から `trycloudflare.com` URL を抽出し、以降は API で自律制御。

※ 詳細は [skills/colab-comfy-agent/SKILL.md](file:///C:/lib/github/kjranyone/colab-comfy-a100-template/skills/colab-comfy-agent/SKILL.md) を参照してください。

---

## 📜 ライセンス・利用規約
- MiniMax-H3 モデルは [MiniMax H3 Community License](https://huggingface.co/Comfy-Org/MiniMax-H3) に従います。
- ComfyUI は [GPL-3.0 License](https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE) です。
