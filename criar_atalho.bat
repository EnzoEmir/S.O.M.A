@echo off
setlocal enabledelayedexpansion

:: Define o título da janela do console
title Criador de Atalho para main.py

echo.
echo    =======================================================
echo                Criador de Atalho para S.O.M.A
echo    =======================================================
echo.
echo  Este script ira criar um atalho na sua Area de Trabalho
echo  para o arquivo 'main.py' encontrado nesta pasta.
echo.
echo  Procurando pelo arquivo 'main.py'...
echo.

set "PASTA_SCRIPT=%~dp0"
set "ARQUIVO_PY_NOME=main.py"
set "ARQUIVO_PY_CAMINHO=%PASTA_SCRIPT%%ARQUIVO_PY_NOME%"

:: Verifica se o arquivo main.py existe na pasta
if not exist "%ARQUIVO_PY_CAMINHO%" (
    echo [ERRO] O arquivo '%ARQUIVO_PY_NOME%' nao foi encontrado na pasta:
    echo        "%PASTA_SCRIPT%"
    echo.
    echo Por favor, certifique-se que este .bat esta na mesma pasta que o seu '%ARQUIVO_PY_NOME%'.
    echo.
    pause
    exit /b
)

echo Encontrado: %ARQUIVO_PY_NOME%
echo.

:: Verifica se o Python está instalado e acessível
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi encontrado no sistema.
    echo.
    echo Por favor, certifique-se que o Python esta instalado e esta no PATH do sistema.
    echo Voce pode baixar o Python em: https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

echo Python encontrado no sistema.
echo.

:: Verifica se existe um ambiente virtual na pasta e define o comando
set "VENV_PYTHONW=%PASTA_SCRIPT%.venv\Scripts\pythonw.exe"
set "VENV_PYTHON=%PASTA_SCRIPT%.venv\Scripts\python.exe"

if exist "%VENV_PYTHONW%" (
    echo Ambiente virtual encontrado - usando pythonw.exe do venv
    set "COMANDO_TARGET=%VENV_PYTHONW%"
    goto :comando_definido
)

if exist "%VENV_PYTHON%" (
    echo Ambiente virtual encontrado - usando python.exe do venv  
    set "COMANDO_TARGET=%VENV_PYTHON%"
    goto :comando_definido
)

:: Se não há venv, usa o Python do sistema
pythonw --version >nul 2>&1
if %errorlevel% equ 0 (
    set "COMANDO_TARGET=pythonw.exe"
    echo Usando pythonw.exe do sistema ^(sem janela de console^)
) else (
    set "COMANDO_TARGET=python.exe"
    echo Usando python.exe do sistema ^(com janela de console^)
)

:comando_definido
set "COMANDO_ARGS=%ARQUIVO_PY_CAMINHO%"

:: Define os nomes e caminhos baseados em "main"
set "NOME_BASE=main"
set "NOME_ATALHO=S.O.M.A"
set "CAMINHO_ATALHO=%UserProfile%\Desktop\%NOME_ATALHO%.lnk"
set "CAMINHO_ICONE=%PASTA_SCRIPT%%NOME_BASE%.ico"

echo  Configuracoes do atalho:
echo    - Nome: %NOME_ATALHO%
echo    - Destino: %COMANDO_TARGET% %COMANDO_ARGS%
echo    - Pasta de trabalho: %PASTA_SCRIPT%
echo.

:: Verifica se existe um ícone chamado "main.ico"
if exist "%CAMINHO_ICONE%" (
    echo Icone encontrado: %CAMINHO_ICONE%
) else (
    echo Icone 'main.ico' nao encontrado. O atalho usara o icone padrao.
    set "CAMINHO_ICONE="
)

echo.
echo Criando atalho...

:: Usa um VBScript temporário para criar o atalho com todas as propriedades
set "VBS_TEMP=%TEMP%\criar_atalho_temp.vbs"

(
    echo Set oWS = WScript.CreateObject^("WScript.Shell"^)
    echo sLinkFile = "%CAMINHO_ATALHO%"
    echo Set oLink = oWS.CreateShortcut^(sLinkFile^)
    echo oLink.TargetPath = "%COMANDO_TARGET%"
    echo oLink.Arguments = "%COMANDO_ARGS%"
    echo oLink.WorkingDirectory = "%PASTA_SCRIPT%"
    if defined CAMINHO_ICONE (
        echo oLink.IconLocation = "%CAMINHO_ICONE%"
    )
    echo oLink.Save
) > "%VBS_TEMP%"

:: Executa o VBScript e depois o apaga
cscript //nologo "%VBS_TEMP%" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao criar o atalho.
    echo.
    del "%VBS_TEMP%" 2>nul
    pause
    exit /b
)
del "%VBS_TEMP%"

echo.
echo    =======================================================
echo      Atalho criado com sucesso na sua Area de Trabalho!
echo    =======================================================
echo.
pause