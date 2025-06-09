@echo off
setlocal


set COMMIT_MSG=Primeiro commit
echo ----------------------------------------
echo Inicializando repositório Git...
echo ----------------------------------------
git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    git init
    echo Git inicializado com sucesso.
) else (
    echo Este diretório já é um repositório Git.
)
git add .
git commit -m "mensagem qualquer" 2>nul
git branch -M main
echo.
echo ? Repositório Git inicializado com commit e branch main.
pause
