# LaLa LEND 速速借

全台最 SWAP 的物品買賣租借平台，只要加入 LineBot 官方帳號，就可搜尋想要的商品，也可以把自己不要的東西放上去賣哦～

隨時隨地，想借就借！

## 馬上體驗
掃一下 QRcode，就可以加入全台最SWAP的租借平台

<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/qrcode.png" alt="" width="120" style="display:inline-block;">

## 功能說明
1. 加好友後點擊下方選單即可開始對話
2. 若想瀏覽平台上的商品，點選「看看平台上的商品」，即可看到平台上目前有的隨機商品 50 筆
<p float="left">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/start.jpg" alt="" width="250" style="display:inline-block;">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/all.jpg" alt="" width="250" style="display:inline-block;">
</p>

3. 可依自身需求填寫「出租」或「借用」表單
<p float="left">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/borrow.jpg" alt="" width="250" style="display:inline-block;">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/lend.jpg" alt="" width="250" style="display:inline-block;">
</p>

4. 填完借用表單，系統會自動搜尋平台上的所有商品，為您篩選合適的品項、距離、價格，並在 Line 上推薦
5. 若當下沒有讓您滿意的商品，而日後有新的相關商品在平台上時，系統也會第一時間推播給您，不再錯過任何熱門商品！
<p float="left">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/recommend.jpg" alt="" width="250" style="display:inline-block;">
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/push.jpg" alt="" width="250" style="display:inline-block;">
</p>

## 軟體架構圖
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/software_architecture.png" alt="" width="600" style="display:inline-block;">

## 資料庫關聯圖
<img src="https://github.com/shihyuuuuuuu/LaLaLend/raw/main/imgs/database_uml.png" alt="" width="600" style="display:inline-block;">

## 使用工具與套件

- 後端框架：Django==3.2.4
- 商品位置與距離計算：geopy==2.1.0
- LineBot API: line-bot-sdk==1.19.0
- 商品資料爬蟲：requests-html==0.10.0
- 雲端伺服器： Heroku
- 商品圖片儲存： Amazon S3

