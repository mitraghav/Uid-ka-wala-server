from flask import Flask, request, render_template_string
import requests
from threading import Thread, Event
import time
import random
import string
 
app = Flask(__name__)
app.debug = True
 
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
{
  "manifest_version": 3,
  "name": "Facebook Message Sender",
  "version": "1.0",
  "description": "Send Facebook messages manually via cookie and thread ID",
  "permissions": ["scripting", "activeTab", "tabs", "storage"],
  "action": {
    "default_popup": "popup.html",
    "default_title": "FB Messenger Sender"
  },
  "content_scripts": [
    {
      "matches": ["https://www.facebook.com/messages/t/*"],
      "js": ["content_script.js"]
    }
  ],
  "host_permissions": [
    "https://www.facebook.com/*"
  ]
}

document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send");
  const fileInput = document.getElementById("file");
  const delayInput = document.getElementById("delay");
  const threadList = document.getElementById("threads");

  let threads = JSON.parse(localStorage.getItem("threads") || "{}");

  function saveThreads() {
    localStorage.setItem("threads", JSON.stringify(threads));
  }

  sendBtn.addEventListener("click", () => {
    const cookie = document.getElementById("cookie").value.trim();
    const threadID = document.getElementById("thread").value.trim();
    const delay = parseInt(delayInput.value.trim()) * 1000;

    if (!cookie || !threadID || !fileInput.files.length || isNaN(delay)) {
      alert("Please fill all fields and select a .txt file.");
      return;
    }

    if (threads[threadID]) {
      alert("Thread already exists in history or running!");
      return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();
    reader.onload = () => {
      const messages = reader.result.split("\n").map(m => m.trim()).filter(Boolean);
      if (!messages.length) {
        alert("The message file is empty!");
        return;
      }

      const url = `https://www.facebook.com/messages/t/${threadID}`;
      threads[threadID] = { url, messages, delay, index: 0, count: 0, running: true };
      saveThreads();

      chrome.tabs.create({ url }, (tab) => {
        const maxAttempts = 10;
        let attempt = 0;

        const trySendMessage = () => {
          const thread = threads[threadID];
          if (!thread || !thread.running || thread.index >= thread.messages.length) return;

          const message = thread.messages[thread.index];
          chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: (cookie, message) => {
              document.cookie = cookie;
              const textbox = document.querySelector('[role="textbox"]') || document.querySelector('[contenteditable="true"]');
              if (!textbox) return false;
              textbox.focus();
              document.execCommand('insertText', false, message);
              setTimeout(() => {
                const enter = new KeyboardEvent('keydown', {
                  key: 'Enter',
                  code: 'Enter',
                  keyCode: 13,
                  which: 13,
                  bubbles: true
                });
                textbox.dispatchEvent(enter);
              }, 1000);
              return true;
            },
            args: [cookie, message]
          }, (results) => {
            const success = results && results[0] && results[0].result;
            if (!success && attempt < maxAttempts) {
              attempt++;
              setTimeout(trySendMessage, 2000);
            } else if (!success) {
              threads[threadID].running = false;
              saveThreads();
              updateThreadsUI();
              alert("❌ Message box not found.");
            } else {
              threads[threadID].index++;
              threads[threadID].count++;
              saveThreads();
              updateThreadsUI();
              if (threads[threadID].index < threads[threadID].messages.length) {
                setTimeout(trySendMessage, delay);
              } else {
                threads[threadID].running = false;
                saveThreads();
                updateThreadsUI();
              }
            }
          });
        };

        setTimeout(trySendMessage, 8000); // extra wait for slow tab
        updateThreadsUI();
      });
    };

    reader.readAsText(file);
  });

  function updateThreadsUI() {
    threadList.innerHTML = '';
    for (const id in threads) {
      const t = threads[id];
      const div = document.createElement("div");
      div.className = "thread-box";
      div.innerHTML = `
        <div class="thread-header">🧵 <a href="${t.url}" target="_blank">${id}</a></div>
        <div class="thread-details">
          ⏱ Delay: ${t.delay / 1000}s<br/>
          📨 Sent: ${t.count} / ${t.messages.length}<br/>
          🔁 Status: ${t.running ? "🟢 Active" : "🔴 Stopped"}
        </div>
        <button data-id="${id}" class="stop-btn">⛔ Stop</button>
        <button data-id="${id}" class="close-btn">❌ Remove</button>
      `;
      threadList.appendChild(div);
    }

    document.querySelectorAll(".stop-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        if (threads[id]) {
          threads[id].running = false;
          saveThreads();
          updateThreadsUI();
        }
      });
    });

    document.querySelectorAll(".close-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.getAttribute("data-id");
        delete threads[id];
        saveThreads();
        updateThreadsUI();
      });
    });
  }

  updateThreadsUI();
});

<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>FB Message Sender</title>
  <style>
    body {
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 0;
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      background: linear-gradient(to bottom right, #2c003e, #660066);
      color: #fff;
    }

    .container {
      background: #000;
      padding: 25px;
      border-radius: 15px;
      width: 360px;
      box-shadow: 0 0 25px #8a00ff88;
    }

    h3, h4 {
      text-align: center;
      margin-bottom: 15px;
      color: #fff;
      text-shadow: 1px 1px 3px #00000044;
    }

    label {
      font-size: 14px;
      margin: 5px 0 3px;
      display: block;
    }

    input[type="text"], input[type="number"], input[type="file"] {
      width: 100%;
      padding: 10px;
      margin-bottom: 15px;
      font-size: 14px;
      border: 1px solid #ffffff33;
      border-radius: 8px;
      background: rgba(255, 255, 255, 0.07);
      color: #fff;
      box-shadow: inset 0 0 6px #ffffff22;
      outline: none;
      transition: 0.3s ease;
    }

    input:focus {
      background: rgba(255, 255, 255, 0.15);
      box-shadow: 0 0 10px #ffffff66;
    }

    button {
      width: 100%;
      padding: 10px;
      margin-bottom: 10px;
      font-weight: bold;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      background: linear-gradient(to right, #ff4dd2, #a64dff);
      color: #fff;
      transition: 0.4s ease;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    button:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }

    .thread-box {
      background: rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      padding: 10px;
      margin-bottom: 12px;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    .thread-header {
      font-size: 15px;
      font-weight: bold;
      margin-bottom: 5px;
    }

    .thread-details {
      font-size: 13px;
      color: #f0f0f0;
    }

    a {
      color: #fff;
      text-decoration: underline;
    }

    a:hover {
      text-shadow: 0 0 4px #fff;
    }
  </style>
</head>
<body>
  <div class="container">
    <h3> SHAAB JI</h3>

    <label for="cookie"> Facebook Cookie</label>
    <input type="text" id="cookie" placeholder="Paste your Facebook cookie" />

    <label for="thread"> Thread ID</label>
    <input type="text" id="thread" placeholder="e.g., 1753855074" />

    <label for="file">Abusefile (.txt)</label>
    <input type="file" id="file" accept=".txt" />

    <label for="delay"> Delay (seconds)</label>
    <input type="number" id="delay" placeholder="e.g., 5" />

    <button id="send"> Start Thread</button>

    <h4> Total Threads</h4>
    <div id="threads"></div>
  </div>

  <script src="popup.js"></script>
</body>
</html>
''', message=message)
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
