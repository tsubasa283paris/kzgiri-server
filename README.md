# kzgiri APIサーバ

フロント → <https://github.com/eityans/kzgiri-front>

## 構成

- データベース： MySQL
- APIサーバ： Ruby on Rails
- テスト： rspec
- ドキュメンテーション： yard

## 環境構築

動作確認済み環境：Ubuntu 20.04（WSL2）

以下Ubuntu（WSL）での開発環境の構築手順。

### Ruby関連

- [rbenv](https://github.com/rbenv/rbenv) をインストールする。  
  ```sh
  git clone https://github.com/rbenv/rbenv.git ~/.rbenv
  nano ~/.bashrc
  # 以下追記
  # eval "$(~/.rbenv/bin/rbenv init - bash)"
  source ~/.bashrc
  git clone https://github.com/rbenv/ruby-build.git "$(rbenv root)"/plugins/ruby-build
  sudo apt update
  sudo apt-get install -y autoconf bison patch build-essential rustc libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libgmp-dev libncurses5-dev libffi-dev libgdbm6 libgdbm-dev libdb-dev uuid-dev
  ```

- rbenvでRuby3.3.3をインストール、当リポジトリでのlocalバージョンに設定する。  
  ```sh
  rbenv install 3.3.3
  rbenv local 3.3.3
  ```

### MySQL関連

- MySQLをインストールする。  
  ```
  sudo apt update
  sudo apt install mysql-server -y
  ```

- データベースサーバデーモンを起動する。  
  ```
  sudo systemctl start mysql.service
  ```

  - `System has not been booted with systemd as init system (...)` といったメッセージが表示される場合、以下を実施する。  
    - `/etc/wsl.conf` を編集し、以下の記述を追加する。  
      ```
      [boot]
      systemd=true
      ```
    - WSLを再起動する。  
      （cmdなどから）  
      ```
      wsl.exe --shutdown
      ```

- `kzgiri` という名前のデータベースを作成する。  
  ```
  sudo mysql
  mysql> CREATE DATABASE kzgiri;
  mysql> \q
  ```

- サーバからアクセスするためのデータベースユーザを作成する。  
  ユーザ名やパスワードは任意。
  ```
  sudo mysql
  mysql> CREATE USER 'kzgiri-client'@'localhost' IDENTIFIED BY 'kzgiri';
  mysql> GRANT ALL PRIVILEGES ON kzgiri.* TO 'kzgiri-client'@'localhost';
  mysql> \q
  ```

- マイグレーションを適用する。  
  ```
  bin/rails db:migrate
  ```

### ドキュメント

「Ruby関連」完了後、`. yard.sh` を実行する。  
ドキュメントのHTMLを返すサーバが起動するので、ブラウザから `localhost:8808` でアクセスする。

## 実行

```
bin/rails server
```
