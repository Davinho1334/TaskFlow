@echo off
set REPO_URL=https://github.com/Davinho1334/TaskFlow.git

git init
git add .
git commit -m "Primeiro commit"
git branch -M main

REM Substitui o remote se já existir
git remote remove origin 2>nul
git remote add origin %REPO_URL%

git push -u origin main

echo Projeto local vinculado ao GitHub com sucesso!
pause
