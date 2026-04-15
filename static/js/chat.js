const messageHistory = [];

function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
}

function sendQuick(text) {
  document.getElementById('chatInput').value = text;
  sendMessage();
}

async function sendMessage() {
  const input   = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const text    = input.value.trim();
  if (!text) return;

  input.value = '';
  input.style.height = 'auto';

  appendMessage('user', text);
  messageHistory.push({ role: 'user', content: text });

  setLoading(true);
  const typingId = appendTyping();

  try {
    const res = await fetch(`/chat/${PLAN_ID}/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: messageHistory }),
    });

    const data = await res.json();
    removeTyping(typingId);

    if (data.reply) {
      appendMessage('ai', data.reply);
      messageHistory.push({ role: 'assistant', content: data.reply });
    } else {
      appendMessage('ai', 'Sorry, I had trouble responding. Please try again.');
    }
  } catch (err) {
    removeTyping(typingId);
    appendMessage('ai', 'Connection error. Please check your server and try again.');
  }

  setLoading(false);
}

function appendMessage(role, text) {
  const container = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `chat-msg msg-${role}`;

  const formatted = formatText(text);

  if (role === 'ai') {
    div.innerHTML = `
      <div class="msg-avatar">◈</div>
      <div class="msg-bubble">${formatted}</div>
    `;
  } else {
    div.innerHTML = `
      <div class="msg-bubble msg-bubble-user">${formatted}</div>
    `;
  }

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function appendTyping(role) {
  const container = document.getElementById('chatMessages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.className = 'chat-msg msg-ai';
  div.id = id;
  div.innerHTML = `
    <div class="msg-avatar">◈</div>
    <div class="msg-bubble typing-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function setLoading(loading) {
  const btn = document.getElementById('sendBtn');
  document.getElementById('sendIcon').style.display   = loading ? 'none' : 'inline';
  document.getElementById('sendLoader').style.display = loading ? 'inline' : 'none';
  btn.disabled = loading;
  document.getElementById('chatInput').disabled = loading;
}

function formatText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code>$1</code>')
    .replace(/^(\d+)\. /gm, '<br><strong>$1.</strong> ')
    .replace(/^- /gm, '<br>• ')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    .replace(/^(.+)$/, '<p>$1</p>');
}

function clearChat() {
  messageHistory.length = 0;
  const container = document.getElementById('chatMessages');
  container.innerHTML = `
    <div class="chat-msg msg-ai">
      <div class="msg-avatar">◈</div>
      <div class="msg-bubble">
        <p>Chat cleared! What would you like to work on?</p>
      </div>
    </div>
  `;
}

async function loadTips() {
  const box     = document.getElementById('tipsBox');
  const content = document.getElementById('tipsContent');
  box.style.display = 'block';
  content.textContent = 'Generating tips…';

  try {
    const res  = await fetch(`/chat/${PLAN_ID}/tips`);
    const data = await res.json();
    content.innerHTML = formatText(data.tips || 'Could not load tips.');
  } catch {
    content.textContent = 'Failed to load tips.';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('chatInput').focus();
});