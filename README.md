# Hometoku
Slack app Hometokuの開発

## スライド
https://docs.google.com/presentation/d/1rma-4fDNjVkG9htI5yMbbt2ryckZBONcv_8WFbjggzQ/edit?usp=sharing

## コーディング規約
[Pythonの基本的なコーディング規約](https://pep8-ja.readthedocs.io/ja/latest/)を参照    
ミスってた部分だけピックアップして書き足す
1. ファイル名：×`positiveWord.py` → ○`positive_word.py`
2. インデント：× Space2個 → ○ Space4個

## 利用パッケージの共有方法
### 準備
1. `$ git pull origin main`
2. `$ python3 -m venv .venv`
3. `$ source .venv/bin/active`

### パッケージのインストールした時
1. `(.venv)$ pip install xxx(インストールするパッケージ)`
2. `(.venv)$ pip freeze > requirements.txt`
3. `(.venv)$ git add .`からいつものpushまで

### 他の人のものを引っ張ってくる時
1. `(.venv)$ git pull`
2. `(.venv)$ pip install -r requirements.txt`

## Tokenの管理
1. Slackの「たいせつなもの」チャンネルでTokenを確認．以下のコマンドを置き換えて打ち込む．
2. `export SLACK_BOT_TOKEN=xoxb-your-token`
3. `export SLACK_SIGNING_SECRET=your-signing-secret`

## ngrokの環境設定
1. [ngrokのダウンロードページ](https://ngrok.com/download)にアクセスしDL
2. ダウンロードしたものを解凍する
3. 解凍して出てきたファイルのあるディレクトリにターミナルで移動
4. `$ printenv PATH`で`/usr/local/bin`にPATHが通っていることを確認
5. `$ mv ngrok /usr/local/bin/`
6. `$ ngrok -v`でバージョンが出ればおk

## テスト環境の立て方
1. mian.pyを動かす → `Bolt is running!`的なのが出てればおk
2. ngrokを動かす
    1. ngrok環境があることを確認する
    2. `$ ngrok http 3000`
    3. `Forwarding      https://a10dc1f0b796.ngrok.io -> http://localhost:`みたいなとこのhttpsリンクをコピー
3. [Slack app の設定画面](https://api.slack.com/apps/A0252JRUBU2/general?)を開く
4. Event Subscriptionsに飛び，トグルをオンにする
5. URLフォームに`コピーしたURL/slack/events`と入力 → 失敗してたら再起動とかしてみる
6. Interactivity & ShortcutsのURLも同じものに更新する
7. 何か設定を変えるならここで変える
8. 変えた場合はOAuth & PermissionsからReinstall in Workspaceでリインストールする
9. Slack上とlogで動作確認開始！
