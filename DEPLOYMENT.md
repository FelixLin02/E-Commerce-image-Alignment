# 🚀 如何將應用程式部署上線

若您希望讓其他人透過網際網路存取此服務，最簡單的方式是使用 **Streamlit Community Cloud**。它是免費的，且專為 Streamlit 應用程式設計。

## 📋 準備工作

1.  **GitHub 帳號**：您需要一個 [GitHub](https://github.com/) 帳號。
2.  **程式碼上傳**：您需要將此專案 (`Project` 資料夾內的內容) 上傳到一個新的 GitHub Repository (儲存庫)。

## 步驟一：將程式碼上傳至 GitHub

1.  登入 GitHub 並建立一個新的 Repository (例如命名為 `image-alignment-tool`)。
2.  確保您的 Repository 包含以下關鍵檔案 (這些都已經在您的資料夾中了)：
    *   `app.py` (主程式)
    *   `main.py` (核心邏輯)
    *   `requirements.txt` (套件清單)
    *   `.streamlit/config.toml` (設定檔)
3.  將您電腦上的檔案 Push 到該 GitHub Repository。

## 步驟二：在 Streamlit Community Cloud 部署

1.  前往 [Streamlit Community Cloud](https://share.streamlit.io/) 並使用您的 GitHub 帳號登入。
2.  點擊右上角的 **"New app"** 按鈕。
3.  填寫部署資訊：
    *   **Repository**: 選擇您剛剛建立的 GitHub Repository (例如 `your-name/image-alignment-tool`)。
    *   **Branch**: 通常是 `main` 或 `master`。
    *   **Main file path**: 輸入 `app.py`。
4.  點擊 **"Deploy!"**。

## 步驟三：等待部署完成

*   Streamlit Cloud 會開始下載 `requirements.txt` 中的套件並安裝。
*   這個過程可能需要幾分鐘。
*   完成後，您會獲得一個專屬網址 (例如 `https://image-alignment-tool.streamlit.app`)，您可以將此連結分享給任何人使用。

## 💡 其他注意事項

*   **OpenCV 依賴**：我們已經在 `requirements.txt` 中使用了 `opencv-python-headless`，這是雲端環境正確執行所需的版本，無需更改。
*   **隱私設定**：Streamlit Community Cloud 的免費版應用程式預設是公開的。
*   **資源限制**：免費版有記憶體限制 (通常 1GB)，但對於本專案的圖片處理需求來說應該足夠。

## 🌐 其他部署選項 (進階)

如果您熟悉其他雲端平台，也可以考慮：
*   **Render / Railway / Fly.io**：這些平台也提供免費或低成本的 Python 應用程式託管。
    *   **Start Command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
