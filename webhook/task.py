import requests
import json
import threading
import time
import uvicorn
from fastapi import FastAPI, Request
# FIX 1: Import JSONResponse for the server
from starlette.responses import JSONResponse 

# --- 1. Global Variable to Share Code ---
PART_2_CODE = None
API_ENDPOINT = "https://test.icorp.uz/interview.php"

# --- 2. The Server Part (FastAPI) ---
app = FastAPI()

# FIX 1: Use the correct FastAPI decorators instead of @app.route
@app.post("/webhook")
@app.get("/webhook")
async def webhook_listener(request: Request):
    """This function runs when the API sends the 2nd part of the code to our URL."""
    global PART_2_CODE
    
    print("\n--- [Server] Webhook Received! ---")
    
    try:
        data = await request.json()
        print(f"[Server] Received JSON: {data}")
        PART_2_CODE = data.get('part2') or data.get('code') or str(data)
    except Exception:
        try:
            data = await request.body()
            PART_2_CODE = data.decode('utf-8')
            print(f"[Server] Received Raw Data: {PART_2_CODE}")
        except Exception as e:
            print(f"[Server] ERROR reading request: {e}")
            PART_2_CODE = "ERROR"
            
    print(f"[Server] Extracted Part 2 Code: {PART_2_CODE}")
    
    # This now works correctly because of the @app.post decorator
    return {"status": "ok"}

def run_server():
    """Runs the FastAPI server on port 5001."""
    print("[Server] Starting Uvicorn server...")
    # Use port 5001 to avoid conflict with macOS AirPlay
    uvicorn.run(app, host="0.0.0.0", port=5001, log_level="info")


# --- 3. The Client Part (The Main Script) ---
def run_client():
    global PART_2_CODE
    
    time.sleep(2) 
    print("--- [Client] Server is running in background. ---")
    
    try:
        ngrok_url = input("[Client] Enter your public ngrok URL (e.g., https://xyz.ngrok.io): ")
        if not ngrok_url.startswith("https://"):
            print("Invalid URL. Make sure it starts with 'https://'")
            return
            
        webhook_url = f"{ngrok_url}/webhook"
    except EOFError:
        print("No input provided. Exiting.")
        return

    # --- Step 1: Perform POST to get Part 1 ---
    my_message = "Hello from MyCalendarProject!"
    payload = {
        "msg": my_message,
        "url": webhook_url
    }
    
    print(f"\n[Client] Sending POST to {API_ENDPOINT} with payload: {payload}")
    try:
        response = requests.post(API_ENDPOINT, json=payload)
        response.raise_for_status()
        response_json = response.json()
        print(f"[Client] POST Response JSON: {response_json}")
        
        part_1_code = response_json.get('part1') or response_json.get('code')
        if not part_1_code:
            print("[Client] ERROR: Could not find 'part1' or 'code' in the response.")
            return
        print(f"\n[Client] SUCCESS: Got Part 1 = {part_1_code}")

    except requests.exceptions.RequestException as e:
        print(f"[Client] ERROR during POST request: {e}")
        return

    # --- Step 3: Wait for Part 2 ---
    print("[Client] Waiting for Part 2 to arrive at the webhook...")
    wait_time = 0
    while PART_2_CODE is None and wait_time < 30:
        time.sleep(1)
        wait_time += 1
        print("[Client] ...waiting...")

    if PART_2_CODE is None:
        print("[Client] ERROR: Never received Part 2 from the webhook.")
        return
        
    print(f"[Client] SUCCESS: Got Part 2 = {PART_2_CODE}")

    # --- Step 4: Concatenate and perform GET ---
    combined_code = str(part_1_code) + str(PART_2_CODE)
    print(f"\n[Client] Combined Code: {combined_code}")
    
    get_params = {'code': combined_code}
    print(f"[Client] Sending GET to {API_ENDPOINT} with code...")
    
    try:
        final_response = requests.get(API_ENDPOINT, params=get_params)
        final_response.raise_for_status()
        
        # --- FIX 2: Parse the final JSON response ---
        final_message = ""
        try:
            final_json = final_response.json()
            final_message = final_json.get('msg') # Get the message from the 'msg' key
        except requests.exceptions.JSONDecodeError:
            final_message = final_response.text # Fallback to raw text

        # --- Step 5: Get Final Message ---
        print("\n" + "="*30)
        print(f"✅ FINAL RESULT ✅")
        print(f"Original Message: {my_message}")
        print(f"Returned Message: {final_message}") # This will now be the clean string
        print(f"Combined Key Used: {combined_code}")
        print("="*30 + "\n")
        
        if final_message == my_message:
            print("🎉 Success! The messages match.")
        else:
            print("⚠️ Warning: The returned message does not match the original.")

    except requests.exceptions.RequestException as e:
        print(f"[Client] ERROR during final GET request: {e}")


# --- 4. Main execution ---
if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    run_client()
    print("[Main] Script has finished. Server thread will now close.")