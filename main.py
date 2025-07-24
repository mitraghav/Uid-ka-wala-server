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
