import mysql.connector

def accessMysql(user_id, target_id_list, workspase_id, channel_id):
    _user_id  = user_id
    _target_id_list = target_id_list
    _workspace_id = workspase_id
    _channel_id = channel_id

    # コネクションの作成
    _conn = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='hometoku',
        password='vPZrDNYjLfsV',
        database='hometoku'
    )

    # コネクションが切れた時に再接続してくれるよう設定
    _conn.ping(reconnect=True)

    # 接続できているかどうか確認
    print(_conn.is_connected())

    # DB操作用にカーソルを作成
    _cur = _conn.cursor(buffered=True)

    # usersテーブルの作成 ： ユーザーID、ほめられた回数、ワークスペースのIDを管理する #
    _cur.execute("""CREATE TABLE IF NOT EXISTS `users` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `user_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
      `price` int(11) NOT NULL DEFAULT 0,
      `workspace_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
      PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")

    # channelsテーブルの作成 ： チャンネルIDを管理する#
    _cur.execute("""CREATE TABLE IF NOT EXISTS `channels` (
      `channel_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
      PRIMARY KEY (channel_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")

    # belongsテーブルの作成 ： usersのユーザーが所属しているチャンネルを紐づけて管理する #
    _cur.execute("""CREATE TABLE IF NOT EXISTS `belongs` (
      `id` int(11) NOT NULL,
      `channel_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
      PRIMARY KEY (id, channel_id),
      FOREIGN KEY (id) REFERENCES users(id),
      FOREIGN KEY (channel_id) REFERENCES channels(channel_id) ON UPDATE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci""")

    # Mysqlに登録
    insertMysql(_user_id, _workspace_id, _channel_id, _cur, _conn)

    # 褒めピーポーの追加
    for _home_people in _target_id_list:
        _cur.execute("select exists (select * from users where user_id = %s)",(_home_people,))
        if _cur.fetchone()[0] == 0 :
            insertMysql(_home_people, _workspace_id, _channel_id, _cur, _conn)
            print("褒めピーポーがDBにいなかったので、新しく追加したよ")

        _cur.execute("update users set price = price + 1 where user_id = %s and workspace_id = %s",(_home_people, _workspace_id))
        _conn.commit()
        print("homeポイント追加")

    # DB操作が終わったらカーソルとコネクションを閉じる
    _cur.close()
    _conn.close()

def insertMysql(user_id, workspase_id, channel_id, cur, conn):
    _user_id        = user_id
    _workspace_id   = workspase_id
    _channel_id     = channel_id
    _cur            = cur
    _conn           = conn

    try:
        #usersテーブルとbelongsテーブルの中でidが同じものを内部結合し、user_id, workspace_id, channel_idが全部一致するか確認する。
        _sql = "select exists(select u.id, u.user_id, u.workspace_id, b.channel_id from users u INNER join belongs b on u.id = b.id where u.user_id = %s and u.workspace_id = %s and b.channel_id = %s)"
        _cur.execute(_sql, (_user_id, _workspace_id, _channel_id))

        #一致するものがない場合は、それぞれのテーブルにデータを追加する。
        if(_cur.fetchone()[0] == 0):

            # channelsテーブルに存在しない場合は、channelsテーブルにチャンネルIDを追加#
            _cur.execute("select exists (select * from channels where channel_id = %s)",(_channel_id,))
            if _cur.fetchone()[0] == 0 :
                _cur.execute("INSERT INTO channels (channel_id) VALUES (%s)", (_channel_id,))
                _conn.commit()

            # userIDが異なる場合、usersテーブルに追加#
            _cur.execute("select exists (select * from users where user_id = %s)", (_user_id,))
            if _cur.fetchone()[0] == 0 :
                _cur.execute("INSERT INTO users (user_id, price, workspace_id) VALUES (%s, %s, %s)", (_user_id, 0, _workspace_id))
                _conn.commit()

            # ワークスペースIDが異なる場合、usersテーブルに追加 #
            _cur.execute("select exists (select * from users where workspace_id = %s)", (_workspace_id,))
            if _cur.fetchone()[0] == 0 :
                _cur.execute("INSERT INTO users (user_id, price, workspace_id) VALUES (%s, %s, %s)", (_user_id, 0, _workspace_id))
                _conn.commit()

            _cur.execute("select * from users order by id desc limit 1;")
            _last_row = _cur.fetchone()
            _id = _last_row[0]
            _cur.execute("INSERT INTO belongs (id, channel_id) VALUES (%s, %s)", (_id, _channel_id))
            _conn.commit()
            print("データは挿入は成功したよ")

        else:
            print("データは存在するので追加しませんでした。")

    # except mysql.connector.errors.IntegrityError:
    except mysql.connector.errors.IntegrityError:
        print("挿入する情報が重複しています。")

# テスト用 #
accessMysql("SLIC",["DVSPPS","SICJML","FOFFFLL"],"DPXAL", "KCOFOPAP")