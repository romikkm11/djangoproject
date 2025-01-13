document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація карти
    var map = L.map('map').setView([49.8397, 24.0297], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    
    // Запит до сервера для отримання координат
    fetch('/services/')
        .then(response => response.json())
        .then(data => {
            console.log('Services data:', data);
            // Додаємо маркери на карту
            data.services.forEach(service => {
                L.marker([service.latitude, service.longititude]) // Використовуємо longititude
                    .addTo(map)
                    .bindPopup(`<b>${service.name}</b>`); // Відображення назви послуги
            });
        })
        .catch(error => {
            console.error('Error fetching services:', error);
        });
});
