# Get-Response-Of-Face-API-Kube  
## Description  
face-recognition-from-an-image-kubeの結果をUIに共有するマイクロサービスです。前行程のマイクロサービスのface-recognition-from-an-image-kubeから顔ステータスとゲストIDを受け取り、その結果をRedisに書き込むことでUIとデータ連携します。

## Prerequisite  
* Kubernetesの同一ネームスペースにRedisが起動している。

## Requirements  
```
redis==3.0.0
```
## I/O
#### Input
カンバンのメタデータから下記の情報を入力
* ゲストキー(rediskey)
UIと判定結果を共有するためのRedisのキー
* 顔ステータス(status)
前行程のface-recognition-from-an-image-kubeで登録済みか、新規か記載する。
* 人物ID(guest_id)
MySQLに登録されているゲストID
#### Output  
Redisに下記の情報を出力
* key
カンバンから連携された、ゲストキーの値を使用する。
* value
下記のフォーマットで出力する。
```
(A) 前行程のface-recognition-from-an-image-kubeでの処理が成功している場合。（aionのライブラリのget_resultメソッドで判断する。）
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
### Getting Started  
1. 下記コマンドでDockerイメージを作成する。  
```
make docker-build
```
2. Project.ymlに設定を記載し、AionCore経由でコンテナを起動する。  
project.ymlへの記載例  
get_kanban_itrメソッドを使用するので、multiple: noとして起動する。   
```
  get-response-of-face-api:
    multiple: no
```