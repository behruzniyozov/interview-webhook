# Python Webhook Challenge

This project is a Python script designed to solve a two-part webhook-based API challenge. It simultaneously runs a client and a local `FastAPI` web server to perform a complete handshake with a remote API endpoint.



## 📖 How It Works

The script operates in two concurrent threads:

1.  **🖥️ Server Thread:**
    * Starts a local `FastAPI` server on port `5001`.
    * This server listens for incoming `POST` or `GET` requests on the `/webhook` endpoint.
    * Its job is to "catch" the `part2` code sent by the remote API.

2.  **🤖 Client Thread:**
    * **Step 1:** Prompts the user to enter a public URL (which you must get from `ngrok`).
    * **Step 2:** Sends an initial `POST` request to the remote API (`https://test.icorp.uz/interview.php`). This request contains a test message and your public `ngrok` webhook URL.
    * **Step 3:** The remote API responds with `part1` of a secret code.
    * **Step 4:** The remote API *also* sends a *new* request to your public `ngrok` URL, which `ngrok` forwards to your local `/webhook` server. This request contains `part2` of the code.
    * **Step 5:** The client waits until the server thread has received `part2`.
    * **Step 6:** The client combines `part1` and `part2` to create a `combined_code`.
    * **Step 7:** The client sends a final `GET` request to the remote API with the `combined_code`.
    * **Step 8:** The script prints the final message from the server and verifies if it matches the original message sent.

---

## 🛠️ Requirements

* Python 3.7+
* An [ngrok](https://ngrok.com/) account and the `ngrok` CLI tool.
* The following Python libraries:
    * `fastapi`
    * `uvicorn`
    * `requests`

---

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/behruzniyozov/web-hook.git](https://github.com/behruzniyozov/web-hook.git)
    cd web-hook
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required libraries:**
    ```bash
    pip install fastapi uvicorn requests
    ```
    *(Alternatively, create a `requirements.txt` file and run `pip install -r requirements.txt`)*

---

## 🚀 How to Run

This script requires **two terminals** to run correctly.

### Terminal 1: Start `ngrok`

You must first expose your local server's port (`5001`) to the public internet using `ngrok`.

1.  Open your first terminal window.
2.  Run the following command:
    ```bash
    ngrok http 5001
    ```
3.  `ngrok` will give you a public "Forwarding" URL. **Copy the `https://` URL.** It will look something like this:
    `https://1a2b-3c4d-5e6f.ngrok.io`

### Terminal 2: Run the Python Script

1.  Open your second terminal window in the same project directory.
2.  Make sure your virtual environment is activated (`source .venv/bin/activate`).
3.  Run the script:
    ```bash
    python task.py
    ```
4.  The script will start the server and then prompt you:
    `[Client] Enter your public ngrok URL (e.g., https://xyz.ngrok.io):`
5.  **Paste the `ngrok` URL** you copied from Terminal 1 and press **Enter**.

The script will now run the full challenge automatically.

---

## 📋 Example Output

Your two terminals will look something like this:

**Terminal 1 (ngrok):**