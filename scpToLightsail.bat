@echo off

:: PEM 파일 경로 (Windows 경로에서는 백슬래시 사용)
set PEM_PATH=C:\Users\jscha\Desktop\project\dang-il-backend\LightsailDefaultKey-ap-northeast-2.pem

:: 로컬 경로 (전송할 파일/디렉터리 경로)
set LOCAL_PATH=C:\Users\jscha\Desktop\project\dang-il-backend\app

:: 원격 서버 정보
set REMOTE_USER=ubuntu
set REMOTE_HOST=15.164.63.35
set REMOTE_PATH=/home/ubuntu/ArtisticSW2024-dangil

:: SCP 명령 실행 (윈도우에서는 Git Bash 또는 OpenSSH 클라이언트 필요)
scp -i "%PEM_PATH%" -r "%LOCAL_PATH%" %REMOTE_USER%@%REMOTE_HOST%:%REMOTE_PATH%

:: 명령 실행 결과 확인
if %errorlevel% equ 0 (
    echo 파일 전송이 성공적으로 완료되었습니다.
) else (
    echo 파일 전송에 실패했습니다.
)
pause
