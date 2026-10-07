document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const login = document.getElementById('login').value.trim();
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value.trim();
    const phone = document.getElementById('phone').value.trim();

    const msg = document.getElementById('message');
    msg.textContent = '';
    msg.className = '';

    // Клиентская валидация (белый список)
    if (!/^[A-Za-z0-9]{6,50}$/.test(login)) {
        return showError('Логин: от 6 до 50 символов, только латиница и цифры');
    }
    if (password.length < 8) {
        return showError('Пароль должен быть не короче 8 символов');
    }
    if (!/^8\(\d{3}\)\d{3}-\d{2}-\d{2}$/.test(phone)) {
        return showError('Телефон в формате 8(XXX)XXX-XX-XX');
    }
    if (!/^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/.test(email)) {
        return showError('Некорректный email');
    }

    // Отправка на сервер (серверная валидация обязательна!)
    const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login, password, email, phone })
    });
    const data = await res.json();

    if (data.success) {
        msg.className = 'success';
        msg.textContent = 'Пользователь успешно создан!';
        setTimeout(() => window.location.href = '/api/auth/login', 1000);
    } else {
        showError(data.message);
    }
});

function showError(text) {
    const msg = document.getElementById('message');
    msg.className = 'error';
    msg.textContent = text;
}
