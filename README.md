# Get-Response-Of-Face-API-Kube  
## 概要 
face-recognition-from-an-image-kubeの結果をUIに共有するマイクロサービスです。前行程のマイクロサービスのface-recognition-from-an-image-kubeから顔ステータスとゲストIDを受け取り、その結果をRedisに書き込むことでUIとデータ連携します。


## 動作環境
このマイクロサービスはAIONのプラットフォーム上での動作を前提としています。 使用する際は、事前にAIONの動作環境を用意してください。

また、Kubernetesの同一ネームスペースにRedisが起動していることが必要です。

- OS: Linux
  
- CPU: Intel64/AMD64/ARM64
 
- Kubernetes
 
- AION
 
- Kubernetes

- redis==3.0.0

## I/O
#### 入力
kanbanのメタデータから下記の情報を入力します。

* ゲストキー(rediskey)
UIと判定結果を共有するためのRedisのキー

* 顔ステータス(status)
前行程のface-recognition-from-an-image-kubeで登録済みか、新規か記載

* 人物ID(guest_id)
MySQLに登録されているゲストID
#### 出力  
Redisに下記の情報を出力します。

* key
kanbanから連携された、ゲストキーの値を使用

* value
下記のフォーマットで出力
```
(A) 前行程のface-recognition-from-an-image-kubeでの処理が成功している場合。（aionのライブラリのget_resultメソッドで判断します。）
{
    "status": "success",
    "customer": 顔ステータス,
    "age_by_face": 年齢,
    "gender_by_face": 性別,
    "image_path": 顔判定に使用した画像のファイルパス
}
(B) 前行程のface-recognition-from-an-image-kubeでの処理が失敗している場合。
{
    "status": "failed",
    "customer": "",
    "guest_id": "",
    "failed_ms": "face-recognition-from-an-image-kube"
}
```
### セットアップ  
1. このリポジトリをクローンし、makeコマンドを用いてDocker container imageのビルドを行ってください。
  
```
$ cd get-response-of-face-api-kube
$ make docker-build
```

2. Project.ymlに設定を記載し、AionCore経由でコンテナを起動してください。  
project.ymlへの記載例  
get_kanban_itrメソッドを使用するので、multiple: noとして起動してください。

```
 get-response-of-face-api:
 multiple: no
```