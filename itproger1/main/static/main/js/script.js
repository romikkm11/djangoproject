document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізація карти
    var map = L.map('map').setView([49.8397, 24.0297], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    
    fetch('/services/')
        .then(response => response.json())
        .then(data => {
            
            data.services.forEach(service => {
                L.marker([service.latitude, service.longititude])
                    .addTo(map)
                    .bindPopup(`<b>${service.name}</b>`); 
            });
        })
       
});
