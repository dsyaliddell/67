document.getElementById('requestForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const eventId = document.getElementById('event_id').value;
    const msg = document.getElementById('message');

    if (!eventId) {
        msg.className = 'error';
        msg.textContent = 'Выберите помещение';
        return;
    }

    const res = await fetch('/create_request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ event_id: eventId })
    });
    const data = await res.json();
    if (data.success) {
        msg.className = 'success';
        msg.textContent = 'Заявка отправлена администратору!';
        setTimeout(() => window.location.href = '/dashboard', 1200);
    } else {
        msg.className = 'error';
        msg.textContent = data.message || 'Ошибка';
    }
});
