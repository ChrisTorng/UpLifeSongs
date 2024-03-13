# SongsRemix 如何自行製作曲目庫

[此文最新版本在 SongsRemixDemo](https://github.com/ChrisTorng/SongsRemixDemo/blob/main/HowTo_zht.md) 上。

## 簡介
  SongsRemix 分軌網站主功能均由原作者線上直接提供，功能有改善亦會自動更新。自行製作之曲目庫只需製作維護自己的曲目檔案及清單。

  以下安裝相關步驟若有問題，請先至各官網檢視詳細說明。若其他操作步驟有問題，請發 [Issue](https://github.com/ChrisTorng/SongsRemixDemo/issues) 通知我。

### 第一次預備
  1. 安裝必要工具
  2. 建立自己的曲目庫
  3. 本機測試
  4. 修改並發佈

### 之後每一次加曲目
  1. 取得來源音檔
  2. 製作分軌
  3. 檔案搬移與更名
  4. 製作波形圖
  5. 加入曲目資料
  6. 發佈更新

  以下分段詳細說明。

## 第一次預備

### 1. 安裝必要工具
  * 以下安裝相關步驟若有問題，請先至各官網檢視詳細說明
  * 安裝 [Python](https://www.python.org/) (工具執行環境)
    * 開啟命令列執行: `pip install matplotlib pydub`

  * 安裝 [Node.js](https://nodejs.org/) (網頁伺服器)
    *  於命令列執行 `npm install -g http-server` 安裝網頁伺服器
    * Windows 下若遇到路徑錯誤，可建立空資料夾: `mkdir %USERPROFILE%\AppData\Roaming\npm` 後再重試

  * 安裝 [Git](https://git-scm.com/) (上傳更新版本)
  * 安裝 [yt-dlg](https://oleksis.github.io/youtube-dl-gui/) (下載音檔)
  * 安裝分軌工具，以下二擇一:
    * 命令列 [Demucs](https://github.com/facebookresearch/demucs#requirements) (支援各 OS)
      1. 若無 4GB VRAM 以上 GPU ，則 `pip install demucs --user`
      2. 若有，請詳細看各 OS 之安裝步驟

    * [Ultimate Vocal Remover](https://github.com/anjok07/ultimatevocalremovergui) (Windows 圖形介面)
      1. 安裝完成後執行，選擇 mp3
      2. 左下扳手圖示 - Additional Settings - Mp3 Bitrate: 160k

         實測 96k/128k 轉出來的音檔時間長度都不正確，160k/320k 則正常。來源音檔是 128k，故此處使用 160k。

      3. Download Center - 選取 Demucs - 下拉選取 Demucs v4 | htdemucs_6s - 按下載圖示
      4. CHOOSE PROCESS METHOD: Demucs; CHOOSE DEMUCS MODEL: v4 | htdemucs_6s

### 2. 建立自己的曲目庫
  1. 註冊免費 GitHub 帳號
  2. 開啟 [SongsRemixDemo](https://github.com/ChrisTorng/SongsRemixDemo) - Use this template - Create a new repository
  3. Reposity name 輸入欲建立之曲目庫的英數代碼名稱 - Create repository
  4. 綠色 Code 下拉 - 按 複製 圖示
  5. 開啟命令列，切換到欲建立曲目庫之上層目錄
  6. 輸入 `git clone ` 後面貼上目標網址再執行，格式為 `https://github.com/(自己 GitHub 帳號代碼)/(自己曲目庫代碼).git`
  7. 以純文字編輯器開啟 index.html，修改第六行 title 內容為「自己的曲目庫名稱 - SongsRemix」

### 3. 本機測試
  1. 命令列 `cd` 進入曲目庫目錄
  2. 執行 `npx http-server --cors -p 3001` 啟動本機網站，或於 Windows 中執行 `run`
  3. 開啟 [http://localhost:3001](http://localhost:3001) 檢視成果

### 4. 修改並發佈
  1. 以純文字編輯器開啟 songsList.json
  2. 修改 `title`/`titleUrl` 欄位為自己的曲目庫名稱及對應網址後存檔
  3. 重新整理網頁，確認名稱與網址正確
  4. 再於曲目庫資料夾開啟新的命令列視窗，執行
     ```
     git add .
     git commit -m "Update"
     git push origin main
     ```
     或於 Windows 上執行 `push`，以將本機修改推送到 GitHub 網站上
  5. 設定自動發佈: 開啟自己的 GitHub 曲目庫網頁 - 上排 Settings - 左側 Pages - Branch - none - main - Save
  6. 到上排 Actions 中檢視進度，等待顯示綠燈
  7. 上排 Settings - 左側 Pages - Visit site 開啟發佈網站

## 之後每一次加曲目

### 1. 取得來源音檔
  1. 執行 yt_dlg - 貼上所有 YouTube 網址 (若為播放清單，則會全部一次下載)
  2. ... - 選擇輸出資料夾為曲目庫資料夾 - 點 default 下拉 - 選擇 mp3 - Add - 右下角 Start
  3. 將所有來源 mp3 檔名變更為預定顯示的文字

### 2. 製作分軌
  依先前安裝的工具，以下二擇一:
  * 命令列 Demucs
    1. 切換到曲目庫資料夾
    2. `python -m demucs -n htdemucs_6s --mp3 --mp3-bitrate 128 "(音檔名稱)"`

       (實測使用符合來源檔案之 128K 位元速率無異常)

    3. 如果安裝 GPU 版本但執行有錯誤，則加上 -d cpu 參數改用 CPU (速度慢) 試試看。若還有任何問題請查閱 [Demucs 官網說明](https://github.com/facebookresearch/demucs#requirements)
    4. 將所有 mp3 檔案均依上法轉換

  * Windows: Ultimate Vocal Remover
    1. Select Input - 選擇所有來源 mp3 檔
    2. Select Output - 選擇曲目庫資料夾
    3. 若有 4GB VRAM 以上GPU，選擇 GPU Conversion 執行會快很多。若執行出錯則取消此項
    4. Start Processing

    CHOOSE PROCESS METHOD 選擇 Audio Tools 後，CHOOSE AUDIO TOOL 還有 Change Pitch (移調) 功能可用，正值代表升調半音數，負值為降調半音數。

### 3. 檔案搬移與更名
  1. 於曲目庫資料夾開啟命令列
  2. 以下二擇一:
     * Demucs 命令列工具轉換者，執行 `python demucs_move.py`
     * Ultimate Vocal Remover 轉換者，執行 `python uvr_move.py`
  
  它會將目前資料夾中所有 mp3 檔 (以及分軌檔)，依曲目檔名自動搬移至新建立之資料夾，並僅留樂器名稱檔名 (必須全小寫，不含複數結尾 s)，來源檔案則改名為 original.mp3

### 4. 製作波形圖
  執行 `python waveform.py`
  
  它會自動搜尋所有子資料夾下所有 mp3 未有對應 png 檔者，自動建立對應波形圖

### 5. 加入曲目資料
  第 2 步 製作分軌 需要跑一些時間，建議可以同步進行這個項目。
  1. 編輯曲目庫中 `songsList.json`
  2. 複製/修改 `groups` 項目
  3. 更新 `subTitle`。`subTitleUrl` 可事後增加，目前還沒有則清空內容字串
  4. 修改各曲目之 `name` 必須符合資料夾名稱，`youtubeId` 由 YouTube 網址中之 `v=` 參數後取得 (11 碼英數字元含 -_ 但不含 &)
  5. 同第一次本機測試方法確認

### 6. 發佈更新
  1. 於曲目庫資料夾開啟命令列，執行
     ```
     git add .
     git commit -m "Update"
     git push origin main
     ```
     或於 Windows 上執行 `push`
  2. 待 Actions 中執行完畢，開啟線上曲目庫網站確認

### 溫馨提醒
  恭喜完成建立自己的曲目庫。請發 [Issue](https://github.com/ChrisTorng/SongsRemix/issues) 通知我加入 [SongsRemix](https://github.com/ChrisTorng/SongsRemix) 曲目庫清單。也方便後續若有功能異動，任何不相容變動等，可以預先通知作因應。

  若遇到任何問題，或有功能需求都可發 [Issue](https://github.com/ChrisTorng/SongsRemix/issues)。也歡迎任何貢獻，包括程式、畫面與教學文件等。未來計畫請參見 [SongsRemix](https://github.com/ChrisTorng/SongsRemix)。
