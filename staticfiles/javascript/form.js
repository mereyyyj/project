const form = document.createElement('form');
form.innerHTML = '<input type="text" id="name" placeholder="Введите имя"> <button type="submit">Отправить</button>';
document.body.appendChild(form);
form.addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Привет, ' + document.getElementById('name').value);
});