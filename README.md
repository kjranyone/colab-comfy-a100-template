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

> 💡 **節約のポイント**: 検証完了後は、Colab 上部メニュー「ランタイム」>「ランタイムの接続を解除して削除」を必ず実行してください。セッションを終了しないとアイドル状態でも CU が消費され続けます。

---

## 📜 ライセンス・利用規約
- MiniMax-H3 モデルは [MiniMax H3 Community License](https://huggingface.co/Comfy-Org/MiniMax-H3) に従います。
- ComfyUI は [GPL-3.0 License](https://github.com/comfyanonymous/ComfyUI/blob/master/LICENSE) です。
