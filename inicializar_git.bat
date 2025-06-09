@echo off
setlocal


set COMMIT_MSG=Primeiro commit
echo ----------------------------------------
echo Inicializando reposit�rio Git...
echo ----------------------------------------
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    git init
    echo Git inicializado com sucesso.
) else (
    echo Este diret�rio j� � um reposit�rio Git.
)
git add .
git commit -m "mensagem qualquer" 2>nul
git branch -M main
echo.
echo ? Reposit�rio Git inicializado com commit e branch main.
pause
