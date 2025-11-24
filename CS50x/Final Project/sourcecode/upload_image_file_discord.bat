rem @echo off
curl -X POST %1 -H "content-type: multipart/form-data" -F "username=%~2" -F "content=%~3" -F "imageFile=@%4 %5 %6 %7"
 
rem pause