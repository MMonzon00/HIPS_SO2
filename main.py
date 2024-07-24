import sys
sys.path.insert(1,f"{sys.path[0]}/commands")
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import PlainTextResponse
from typing import Optional
import os
from dotenv import load_dotenv
import hash_bin, verify_connections, check_for_sniffers, manage_processes, check_tmp, cronjob_examiner, check_connections_logs
import examine_logs as examineLogs, check_mail_queue as cmq
import check_ddos
# from logging_notification import log_event, notify_admin


# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = FastAPI()

# Añadir middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "your-secret-key"))

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.getenv("BASIC_AUTH_USERNAME")
    correct_password = os.getenv("BASIC_AUTH_PASSWORD")
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/", response_class=HTMLResponse)
async def homePage(request: Request):
    username: Optional[str] = request.session.get("username")
    if username:
        html_code = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Martin-HIPS</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f0f8ff;
            }}
            h1 {{
                margin-bottom: 20px;
                color: #333;
            }}
            .container {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }}
            a {{
                text-decoration: none;
            }}
            .btn {{
                background-color: #4CAF50;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                border: none;
                transition: background-color 0.3s;
                display: block;
                text-align: center;
            }}
            .btn:hover {{
                background-color: #45a049;
            }}
        </style>
        </head>
        <body>
        <h1>Martin-HIPS</h1>
        <div class="container">
            <a href="/verify_system_binaries" class="btn">Verify system binaries</a>
            <a href="/verify_logged_in_users" class="btn">Verify logged in users</a>
            <a href="/check_sniffers" class="btn">Check sniffers and promiscuous mode</a>
            <a href="/examine_logs" class="btn">Examine log files</a>
            <a href="/check_mail_queue" class="btn">Check mail queue size</a>
            <a href="/check_memory_processes" class="btn">Check memory consuming processes</a>
            <a href="/verify_tmp_directory" class="btn">Verify /tmp directory</a>
            <a href="/control_ddos" class="btn">Control DDOS attack</a>
            <a href="/examine_cron_jobs" class="btn">Examine cron jobs</a>
            <a href="/verify_invalid_access_attempts" class="btn">Verify invalid access attempts</a>
            <a href="/logout" class="btn">Logout</a>
        </div>
        </body>
        </html>
        """
    else:
        html_code = """
        <html>
            <head>
                <title>Login</title>
            </head>
            <body>
                <h1>Please log in</h1>
                <form action="/login" method="post">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password">
                    <button type="submit">Log In</button>
                </form>
            </body>
        </html>
        """
    return HTMLResponse(content=html_code)

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    correct_username = os.getenv("BASIC_AUTH_USERNAME")
    correct_password = os.getenv("BASIC_AUTH_PASSWORD")
    if username != correct_username or password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    request.session['username'] = username
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
async def logout(request: Request):
    request.session.pop('username', None)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

def get_current_username(request: Request) -> str:
    username: Optional[str] = request.session.get("username")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return username

@app.get("/verify_system_binaries", response_class=PlainTextResponse)
async def verify_system_binaries(username: str = Depends(get_current_username)):
    try:
        # Code to verify system binaries
        result = hash_bin.verify_integrity_files()
        formatted_result = "\n".join(result)
        return f"status:\n{formatted_result}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/verify_logged_in_users", response_class=PlainTextResponse)
async def verify_logged_in_users(username: str = Depends(get_current_username)):
    try:
        # Code to verify logged in users
        result = verify_connections.verify_logged_in_users()
        return f"status:\n{result}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/check_sniffers", response_class=PlainTextResponse)
async def check_sniffers(username: str = Depends(get_current_username)):
    try:
        # Perform checks using the imported function
        results = check_for_sniffers.perform_checks()

        return PlainTextResponse(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/examine_logs", response_class=PlainTextResponse)
async def examine_logs(username: str = Depends(get_current_username)):
    try:
        result = examineLogs.analyze_access_log() 
        return PlainTextResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/check_mail_queue", response_class=PlainTextResponse)
async def check_mail_queue(username: str = Depends(get_current_username)):
    # Código para verificar el tamaño de la cola de mails
    return cmq.check_mail_queue()
@app.get("/check_memory_processes", response_class=PlainTextResponse)
async def check_memory_processes(username: str = Depends(get_current_username), threshold: float = 10.0):
    try:
        # List processes consuming high memory
        high_memory_processes = manage_processes.list_high_memory_processes(threshold)
        if high_memory_processes:
            response = "Processes consuming high memory:\n"
            for pid, mem_percent, command in high_memory_processes:
                response += f"PID: {pid}, Memory %: {mem_percent:.2f}, Command: {command}\n"
                if mem_percent > 50.0:
                    response += f"Killing process with PID {pid} consuming {mem_percent:.2f}% memory...\n"
                    manage_processes.kill_process(pid)
            return response
        else:
            return f"No processes consuming more than {threshold}% memory."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/verify_tmp_directory", response_class=PlainTextResponse)
async def verify_tmp_directory(username: str = Depends(get_current_username)):
    try:
        # Check for suspicious files in /tmp
        suspicious_files = check_tmp.check_tmp_directory()

        if suspicious_files:
            for file_path in suspicious_files:
                check_tmp.log_event(file_path)
            # Move suspicious files to quarantine folder
            check_tmp.quarantine_files(suspicious_files)
            return f"Suspicious files found and moved to quarantine: {', '.join(suspicious_files)}"
        else:
            check_tmp.log_event("No suspicious files found in /tmp")
            return "No suspicious files found in /tmp"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/control_ddos", response_class=PlainTextResponse)
async def control_ddos(username: str = Depends(get_current_username)):
    # Código para controlar ataque de DDOS
    return check_ddos.check_DDOS_attack_dns()

@app.get("/examine_cron_jobs", response_class=PlainTextResponse)
async def list_system_cron_endpoint(username: str = Depends(get_current_username)):
    try:
        # List system-wide cronjobs
        system_cronjobs = cronjob_examiner.list_system_cron()
        if system_cronjobs:
            response = "System-wide cronjobs:\n\n"
            for job in system_cronjobs:
                response += f"{job}\n\n"
            return PlainTextResponse(response)
        else:
            return PlainTextResponse("No system-wide cronjobs found or error retrieving them.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/verify_invalid_access_attempts", response_class=PlainTextResponse)
async def failed_attempts(username: str = Depends(get_current_username)):
    try:
        # Analyze failed login attempts
        user_attempts, ip_attempts = check_connections_logs.analyze_failed_attempts()

        # Format results
        user_output = "Users with repetitive failed attempts:\n"
        for user, attempts in user_attempts.items():
            if attempts > 5:  # Threshold for repetitive attempts
                user_output += f"User {user} has {attempts} failed attempts.\n"

        ip_output = "\nIPs with multiple failed attempts from different users:\n"
        for ip, attempts in ip_attempts.items():
            if attempts > 5:  # Threshold for multiple user attempts
                ip_output += f"IP {ip} has {attempts} failed attempts.\n"

        return PlainTextResponse(user_output + ip_output)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8769,
        log_level="debug",
        reload=True,
    )
