/* =============================================
   PlaceForge AI — Main JavaScript
   ============================================= */

// ─── User Menu Toggle ───
function toggleUserMenu() {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', function (e) {
    const menu = document.querySelector('.user-menu');
    const dropdown = document.getElementById('userDropdown');
    if (dropdown && menu && !menu.contains(e.target)) {
        dropdown.classList.remove('show');
    }
});

// ─── Mobile Sidebar Toggle ───
function toggleMobileSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('open');
}

// Close sidebar on outside click
document.addEventListener('click', function (e) {
    const sidebar = document.getElementById('sidebar');
    const hamburger = document.querySelector('.hamburger');
    if (sidebar && hamburger && !sidebar.contains(e.target) && !hamburger.contains(e.target)) {
        sidebar.classList.remove('open');
    }
});

// ─── Notifications Toggle ───
function toggleNotifications() {
    // Placeholder for notification panel
    const badge = document.querySelector('.notif-badge');
    if (badge) badge.style.display = 'none';
}

// ─── Chatbot Widget Toggle ───
function toggleChatbot() {
    const body = document.getElementById('chatbotBody');
    const btn = document.getElementById('chatbotToggleBtn');
    if (!body) return;
    if (body.style.display === 'none') {
        body.style.display = 'flex';
        if (btn) btn.textContent = '−';
    } else {
        body.style.display = 'none';
        if (btn) btn.textContent = '+';
    }
}

// ─── Widget Chatbot Send ───
async function sendChatMessage() {
    const input = document.getElementById('chatbotInput');
    if (!input) return;
    const msg = input.value.trim();
    if (!msg) return;
    input.value = '';

    appendWidgetMessage(msg, 'user');
    const typing = appendWidgetMessage('...', 'bot');

    try {
        const csrfToken = getCookie('csrftoken');
        const res = await fetch('/chatbot/send/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
            body: JSON.stringify({ message: msg })
        });
        const data = await res.json();
        typing.remove();
        appendWidgetMessage(data.response, 'bot');
    } catch (e) {
        typing.remove();
        appendWidgetMessage('Sorry, I could not respond right now.', 'bot');
    }
}

function appendWidgetMessage(text, role) {
    const container = document.getElementById('chatbotMessages');
    if (!container) return null;
    const div = document.createElement('div');
    div.className = `chat-message ${role}-message`;
    div.innerHTML = `<div class="chat-bubble">${text}</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}

function handleChatEnter(e) {
    if (e.key === 'Enter') sendChatMessage();
}

// ─── CSRF Cookie Helper ───
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// ─── Progress Bars Animation ───
function animateProgressBars() {
    const bars = document.querySelectorAll('.progress-bar-fill');
    bars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => { bar.style.width = width; }, 100);
    });
}

// ─── Auto-dismiss alerts ───
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-8px)';
            alert.style.transition = 'all 0.3s';
            setTimeout(() => alert.remove(), 300);
        }, 4000);
    });
}

// ─── Smooth hover effects on cards ───
function initCardHovers() {
    const cards = document.querySelectorAll('.question-card, .stat-card, .feature-item');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transition = 'all 0.2s';
        });
    });
}

// ─── Init ───
document.addEventListener('DOMContentLoaded', function () {
    animateProgressBars();
    autoDismissAlerts();
    initCardHovers();
});
