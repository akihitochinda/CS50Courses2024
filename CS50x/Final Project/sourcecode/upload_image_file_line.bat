rem ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----
rem LINEへ画像ファイルをアップロードするモジュール
rem 引数1:アクセストークン
rem 引数2:コメント
rem 引数3:画像ファイルの絶対パス＋ファイル名
rem ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----

rem @echo off
curl -X POST -H "Authorization: Bearer %1" -F "message = %~2" -F "imageFile=@%3 %4 %5 %6" https://notify-api.line.me/api/notify

rem pause