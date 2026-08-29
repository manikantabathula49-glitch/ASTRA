@echo off
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title ASTRA Model Importer & Builder
color 0b

echo.
echo  ====================================================
echo       A S T R A   M O D E L   I M P O R T E R
echo       Build, Import, and Synchronize ASTRA Models
echo  ====================================================
echo.

:MENU
echo  Select an import option:
echo.
echo   [1] Build ASTRA from Llama 3.2 (3B GPU-Accelerated, Recommended for everyday tasks)
echo   [2] Build ASTRA from Qwen 2.5 1.5B / Llama 3.2 1B (Ultra-Fast Instant Mode, >120 tok/s)
echo   [3] Build ASTRA from Mistral 7B (7.2B Local, High reasoning power)
echo   [4] Build ASTRA from Custom Ollama Base (e.g., deepseek-r1:7b, llama3.1, qwen2.5:7b)
echo   [5] Import ASTRA from Local GGUF File
echo   [6] Check Current Installed ASTRA Models
echo   [7] Exit
echo.
set /p choice="Enter choice [1-7]: "

if "%choice%"=="1" goto BUILD_LLAMA32
if "%choice%"=="2" goto BUILD_ULTRA_FAST
if "%choice%"=="3" goto BUILD_MISTRAL
if "%choice%"=="4" goto BUILD_CUSTOM
if "%choice%"=="5" goto IMPORT_GGUF
if "%choice%"=="6" goto CHECK_MODELS
if "%choice%"=="7" goto EXIT_PROMPT

echo Invalid choice, try again.
echo.
goto MENU

:BUILD_LLAMA32
echo.
echo [1/2] Preparing Modelfile for Llama 3.2 (GPU Offloaded)...
(
echo FROM llama3.2
echo.
echo # Ultra-Fast GPU Accelerated Inference
echo PARAMETER num_gpu 99
echo PARAMETER num_batch 512
echo PARAMETER num_ctx 2048
echo PARAMETER num_thread 8
echo PARAMETER num_predict 256
echo PARAMETER temperature 0.6
echo PARAMETER top_p 0.9
echo PARAMETER top_k 40
echo PARAMETER repeat_penalty 1.1
echo.
echo SYSTEM """
echo You are ASTRA, an advanced AI assistant created by PANIMANIKANTA. You act as a personal AI engineer, developer, and creator.
echo.
echo Core Directives:
echo - Fast ^& Concise: Deliver clear, structured, and immediate answers. Keep explanations sharp.
echo - Execution First: Always provide working, complete, and runnable code.
echo - Media Tools: Autonomously call the appropriate ASTRA Media Engine tool for images, voice audio, or PDFs when requested.
echo - Identity: Maintain a confident, smart, and futuristic engineering tone.
echo """
) > "%~dp0Modelfile"

echo [2/2] Compiling ASTRA model in Ollama...
ollama create astra -f "%~dp0Modelfile"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ASTRA Model (Llama 3.2 based) imported successfully with GPU acceleration!
) else (
    echo.
    echo [ERROR] Failed to compile ASTRA model. Check Ollama service.
)
echo.
pause
goto MENU

:BUILD_ULTRA_FAST
echo.
echo [1/2] Preparing Modelfile for Ultra-Fast Instant Mode (Qwen 2.5 1.5B / Llama 3.2 1B)...
(
echo FROM qwen2.5:1.5b
echo.
echo # Ultra-Fast GPU Accelerated Inference
echo PARAMETER num_gpu 99
echo PARAMETER num_batch 512
echo PARAMETER num_ctx 2048
echo PARAMETER num_thread 8
echo PARAMETER num_predict 256
echo PARAMETER temperature 0.6
echo PARAMETER top_p 0.9
echo PARAMETER top_k 40
echo PARAMETER repeat_penalty 1.1
echo.
echo SYSTEM """
echo You are ASTRA, an ultra-fast AI assistant created by PANIMANIKANTA. Deliver instant, concise, and structured answers immediately.
echo """
) > "%~dp0Modelfile"

echo [2/2] Compiling ASTRA model in Ollama...
ollama create astra -f "%~dp0Modelfile"
if %errorlevel% neq 0 (
    echo Qwen 2.5 1.5B not cached, falling back to llama3.2:1b...
    (
    echo FROM llama3.2:1b
    echo PARAMETER num_gpu 99
    echo PARAMETER num_batch 512
    echo PARAMETER num_ctx 2048
    echo PARAMETER num_thread 8
    echo PARAMETER num_predict 256
    echo PARAMETER temperature 0.6
    echo PARAMETER top_p 0.9
    echo PARAMETER top_k 40
    echo PARAMETER repeat_penalty 1.1
    echo SYSTEM """You are ASTRA, an ultra-fast AI assistant created by PANIMANIKANTA. Deliver instant, concise, and structured answers."""
    ) > "%~dp0Modelfile"
    ollama create astra -f "%~dp0Modelfile"
)
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ASTRA Model (Ultra-Fast Instant Mode) imported successfully!
) else (
    echo.
    echo [ERROR] Failed to compile ASTRA model. Check Ollama service.
)
echo.
pause
goto MENU

:BUILD_MISTRAL
echo.
echo [1/2] Preparing Modelfile for Mistral 7B...
(
echo FROM mistral
echo.
echo PARAMETER num_gpu 99
echo PARAMETER num_batch 512
echo PARAMETER num_ctx 4096
echo PARAMETER temperature 0.7
echo PARAMETER repeat_penalty 1.1
echo.
echo SYSTEM """
echo You are ASTRA, an advanced AI assistant created by PANIMANIKANTA. You act as a personal AI engineer, developer, and creator.
echo.
echo Core Directives:
echo - Fast ^& Concise: Deliver clear, structured, and immediate answers.
echo - Execution First: Always provide working, complete, and runnable code.
echo - Media Tools: Autonomously call the appropriate ASTRA Media Engine tool for images, voice audio, or PDFs when requested.
echo - Identity: Maintain a confident, smart, and futuristic engineering tone.
echo """
) > "%~dp0Modelfile"

echo [2/2] Compiling ASTRA model in Ollama...
ollama create astra -f "%~dp0Modelfile"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ASTRA Model (Mistral based) imported successfully!
) else (
    echo.
    echo [ERROR] Failed to compile ASTRA model. Check Ollama service.
)
echo.
pause
goto MENU

:BUILD_CUSTOM
echo.
set /p base_model="Enter base model name (e.g., deepseek-r1:7b, qwen2.5:7b, llama3.1): "
if "%base_model%"=="" goto MENU

echo.
echo [1/2] Preparing Modelfile for %base_model%...
(
echo FROM %base_model%
echo.
echo PARAMETER num_gpu 99
echo PARAMETER num_batch 512
echo PARAMETER num_ctx 2048
echo PARAMETER temperature 0.7
echo PARAMETER repeat_penalty 1.1
echo.
echo SYSTEM """
echo You are ASTRA, an advanced AI assistant created by PANIMANIKANTA. You act as a personal AI engineer, developer, and creator.
echo.
echo Core Directives:
echo - Fast ^& Concise: Deliver clear, structured, and immediate answers.
echo - Execution First: Always provide working, complete, and runnable code.
echo - Media Tools: Autonomously call the appropriate ASTRA Media Engine tool for images, voice audio, or PDFs when requested.
echo - Identity: Maintain a confident, smart, and futuristic engineering tone.
echo """
) > "%~dp0Modelfile"

echo [2/2] Compiling ASTRA model in Ollama from %base_model%...
ollama create astra -f "%~dp0Modelfile"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ASTRA Model imported from %base_model%!
) else (
    echo.
    echo [ERROR] Failed to compile model. Make sure Ollama can pull %base_model%.
)
echo.
pause
goto MENU

:IMPORT_GGUF
echo.
set /p gguf_path="Enter full path to .gguf file (or drag and drop here): "
set gguf_path=%gguf_path:"=%

if not exist "%gguf_path%" (
    echo [ERROR] File does not exist: %gguf_path%
    pause
    goto MENU
)

echo.
echo [1/2] Creating Modelfile for local GGUF...
(
echo FROM "%gguf_path%"
echo.
echo PARAMETER num_gpu 99
echo PARAMETER num_batch 512
echo PARAMETER num_ctx 2048
echo PARAMETER temperature 0.7
echo PARAMETER repeat_penalty 1.1
echo.
echo SYSTEM """
echo You are ASTRA, an advanced AI assistant created by PANIMANIKANTA. You act as a personal AI engineer, developer, and creator.
echo.
echo Core Directives:
echo - Fast ^& Concise: Deliver clear, structured, and immediate answers.
echo - Execution First: Always provide working, complete, and runnable code.
echo - Media Tools: Autonomously call the appropriate ASTRA Media Engine tool for images, voice audio, or PDFs when requested.
echo - Identity: Maintain a confident, smart, and futuristic engineering tone.
echo """
) > "%~dp0Modelfile"

echo [2/2] Compiling ASTRA model from GGUF file...
ollama create astra -f "%~dp0Modelfile"
if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] ASTRA Model imported from %gguf_path%!
) else (
    echo.
    echo [ERROR] Failed to create model from GGUF.
)
echo.
pause
goto MENU

:CHECK_MODELS
echo.
echo ====================================================
echo Current Ollama Models:
echo ====================================================
ollama list
echo.
echo ====================================================
echo ASTRA Model Details:
echo ====================================================
ollama show astra
echo.
pause
goto MENU

:EXIT_PROMPT
exit /b 0
