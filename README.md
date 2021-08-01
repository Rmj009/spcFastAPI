### docker build 
### docker run 

- `POSTGRESQL_URL_CLOUD_TENANTL`

  - 連線正式 **DB** 的 **URL**

- `POSTGRESQL_URL_LOCAL_TENANT`

  - 連線 Local **DB** 的 **URL**

- `USER_API_URL`

  - **USER** 使用權限 **API URL**

- `EQUIPMENT_API_URL`

  - **機台** 資訊 **API URL**

- `EQUIPMENT_API_URL_LOCAL`

  - Local **機台** 資訊 **API URL**
  
## 🎻 ./lib/constant/constant.go 參數

- `AppMode`

  - `dev`: 開發使用

    - 可以跳脫 **SSO** 邏輯 方便開發
    - 可以在 middleware 中 設定 `constant.TenantId` 方便開發

  - `pro`:

    - 正式環境使用
    
- `PhotoExpirationTime`
   - 拿照片 從 firebase 的過期時間

- `DownloadMaxCount`
   - 工單下載量

- `FirebaseBucket`
   - firebaseBucket url

### Folder: ./docker 可在 local 端跑測試 DB

- 跑起來：

   - `python3 app.py`

- 關掉：

   - `docker-compose -f docker-compose.yml down --rmi all`

## [Change Log](CHANGELOG.md)

