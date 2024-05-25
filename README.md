# Attendance_flask(出席チケット管理)

### 機能

コロナ下でイベント開催時、人数制限とイベント開催日当日の出席者の対応

1. 人数制限でイベントを開催したい。

2. イベントチケットは決まった時間で配布開始したい。

3. 事前に登録した出席者の当日の体温を記録したい。

そのため下記機能を用意している:

- イベント登録(by api)
  - イベントの開催日を決め、チケット販売開始日を登録できます。
- 出席登録
  - チケット販売開始日から、イベント開催日の間で、身元を登録して参加登録ができます。
  - 参加登録後、QRコードが発行されます。スクショを撮ってイベント開催日に会場で提示する。(メール送信未実装)

- 出席確認
  - QRコードのスクショを携帯でスキャンし、出席者の体温を登録する。

### 使い方

- 設定ファイル: docker-compose.yaml

- アプリ起動(初期化):
  ```
  docker-compose up -d #(--update)
  ```

- sql-db:

  ``` bash
  docker-compose exec db /bin/bash
  mysql -u root -p
  ```

- data初期化
  初期化時データは`init.sql`によって作成され、`db-data` によって永続化されています。テストデータいらなくなったら`db-data`消してアプリを再度初期化すればDBが再度初期化されます。

# 設計書

### DB構造

- organization

  - TODO

- event (組織テーブル)

  |pk|カラム名|変数型|意味、コメント|デフォ|
  |--|--|--|--|--|
  |✔︎|event_id|VARCHAR(100)|組織ID||
  | |event_name|VARCHAR(100)|イベント名||
  | |organization_id|VARCHAR(100)|組織名|'unknown'|
  | |pswd|VARCHAR(100)|パスワード(情報閲覧時に使用)||
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
  |✔︎|event_id|VARCHAR(50)|イベントID||
  | |name|VARCHAR(100)|名前||
  | |phone_number|VARCHAR(50)|電話番号||
  | |email|VARCHAR(100)|メールアドレス||
  | |family_id|VARCHAR(50)|家族識別子(乱数)||
  | |comment|VARCHAR(250)|コメント||
  | |memo|VARCHAR(250)|メモ||
  | |version|INT|管理バージョン|1, インクリメント|
  | |created_at|DATETIME(6)|データ作成日時|current_timestamp()|
  | |updated_at|DATETIME(6)|データ更新日時|current_timestamp()|
  | |deleted|BOOLEAN|論理削除フラグ|false|



