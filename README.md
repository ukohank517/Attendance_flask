# AttendanceTicket(出席チケット管理)

### 機能
- 出席登録

- 出席確認

## 使い方

- 設定ファイル: docker-compose.yaml

- アプリ起動: 
  ```
  docker-compose up -d
  ```

- sql-db:

  ``` bash
  docker exec -it [containerID] /bin/bash
  mysql -u root -p
  ```

# 設計書

### DB構造

- organization (組織テーブル)

  |pk|カラム名|変数型|意味、コメント|デフォ|
  |--|--|--|--|--|
  |✔︎|organization_id|VARCHAR(50)|組織ID||
  | |pswd|VARCHAR(50)|パスワード(情報閲覧時に使用)||
  | |ticket_num|INT|チケット数||
  | |event_date|DATETIME(6)|イベント開催日時||
  | |public_date|DATETIME(6)|登録開催日時||
  | |version|INT|管理バージョン|1, インクリメント|
  | |created_at|DATETIME(6)|データ作成日時|current_timestamp()|
  | |updated_at|DATETIME(6)|データ更新日時|current_timestamp()|
  | |deleted|BOOLEAN|論理削除フラグ|false|  

- ticket (チケットテーブル)

  |pk|カラム名|変数型|意味、コメント|デフォ|
  |--|--|--|--|--|
  |✔︎|ticket_id|INT|チケットID||
  |✔︎|organization_id|VARCHAR(50)|組織ID||
  | |last_name|VARCHAR(50)|姓||
  | |first_name|VARCHAR(50)|名前||
  | |email|VARCHAR(100)|メールアドレス||
  | |famali_id|VARCHAR(50)|家族識別子(乱数)||
  | |comment|VARCHAR(250)|コメント||
  | |memo|VARCHAR(250)|メモ||
  | |version|INT|管理バージョン|1, インクリメント|
  | |created_at|DATETIME(6)|データ作成日時|current_timestamp()|
  | |updated_at|DATETIME(6)|データ更新日時|current_timestamp()|
  | |deleted|BOOLEAN|論理削除フラグ|false|  


  