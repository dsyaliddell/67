document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const payload = {
        login:    document.getElementById('login').value.trim(),
        password: document.getElementById('password').value
    };
    const msg = document.getElementById('message');

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            msg.className = 'error';
            msg.textContent = data.message;
        }
    } catch (err) {
        msg.className = 'error';
        msg.textContent = 'Ошибка сервера';
    }
});
