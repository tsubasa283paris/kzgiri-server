# kzgiri APIサーバ

フロント → <https://github.com/eityans/kzgiri-front>

## 構成

- データベース： MySQL
- APIサーバ： Python
  - HTTPサーバ： uvicorn
  - APIフレームワーク： FastAPI
  - ORM： sqlalchemy
  - マイグレーション管理： alembic

## 環境構築

動作確認済み環境：Ubuntu 20.04（WSL2）、CentOS 9

以下Ubuntu（WSL）環境の手順。

- Python関連
  - pyenvをインストールする。  
    ```
    sudo apt update
    sudo apt install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y
    curl https://pyenv.run | bash

    echo '# pyenv' >> ~/.bashrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    source ~/.bashrc
    ```

  - pyenvでPython3.8をインストール、デフォルトに設定する。  
    ```
    pyenv install 3.8.18
    pyenv global 3.8.18
    ```

  - pipenvをインストールする。  
    ```
    pip install pipenv
    echo '# pipenv' >> ~/.bashrc
    echo 'export PIPENV_VENV_IN_PROJECT=1' >> ~/.bashrc
    source ~/.bashrc
    ```

  - Pipfileに記述されたPIPパッケージをインストールする。  
    ```
    cd /path/to/kzgiri-server
    pipenv install
    ```

- MySQL関連
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
  
  - 以下を `.env` に追記する。  
    ```
    DATABASE_USERHOST=kzgiri-client:kzgiri@localhost
    ```
  
  - マイグレーションを適用する。  
    ```
    pipenv run alembic upgrade head
    ```

- TLS関連
  - <https://zenn.dev/jeffi7/articles/10f7b12d6044ad>  
    上記記事など参考に開発環境用の独自CA、サーバ証明書を作成する。  
    ここでは独自CAの証明書を `~/.myCA/localCA.crt`、サーバ証明書を `~/.myCA/localhost.crt` として作成したものとする。
  - サーバ証明書をUbuntuにインストールする。  
    ```
    sudo cp ~/.myCA/localCA.crt /usr/share/ca-certificates/
    sudo sh -c "echo 'localCA.crt' >> /etc/ca-certificates.conf"
    sudo update-ca-certificates
    ```
  - 環境変数を以下設定する。  
    ```
    echo '# localhost server certificate' >> ~/.bashrc
    echo 'TLS_KEYFILE=~/.myCA/localhost.key' >> ~/.bashrc
    echo 'TLS_CERTFILE=~/.myCA/localhost.crt' >> ~/.bashrc
    source ~/.bashrc
    ```
  
## 実行

```
pipenv run uvicorn main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --ssl-keyfile=$TLS_KEYFILE \
  --ssl-certfile=$TLS_CERTFILE
```

### 動作確認

- localhost環境でHTTPS通信できることを確かめる。
  ```
  sudo apt install jq -y
  curl https://localhost:8001/themes -s | jq
  ````
