// var map;
// let markers = new Set();

// document.addEventListener('DOMContentLoaded', function() {
//     map = L.map('map').setView([49.8397, 24.0297], 12);
//     map.zoomControl.remove();
//     L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
//         maxZoom: 19,
//         attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
//     }).addTo(map);

//     fetch('/services/')
//         .then(response => response.json())
//         .then(data => {
//             data.companies.forEach(company => {
//                 var marker = L.marker([company.latitude, company.longititude]).bindPopup(`<b>${company.name}</b>`);
//                 markers.add(marker);
//             });

//             markers.forEach(marker => {
//                 marker.addTo(map);
//             });
//         });

//     fetch('/data/')
//         .then(response => response.json())
//         .then(data => {
//             const serviceTypeSelect = document.getElementById('serviceTypeSelect');
//             const serviceSelect = document.getElementById('serviceSelect');
//             const companySelect = document.getElementById('companySelect');

//             data.service_types.forEach(type => {
//                 const option = document.createElement('option');
//                 option.value = type.id;
//                 option.text = type.name;
//                 serviceTypeSelect.appendChild(option);
//             });

//             data.services.forEach(service => {
//                 const option = document.createElement('option');
//                 option.value = service.id;
//                 option.text = service.name;
//                 serviceSelect.appendChild(option);
//             });

//             data.companies.forEach(company => {
//                 const option = document.createElement('option');
//                 option.value = company.id;
//                 option.text = company.name;
//                 companySelect.appendChild(option);
//             });
//         });
// });


// document.getElementById('applyFiltersBtn').addEventListener('click', function() {
//     const serviceType = document.getElementById('serviceTypeSelect').value;
//     const service = document.getElementById('serviceSelect').value;
//     const company = document.getElementById('companySelect').value;

//     fetch(`/filter/?company=${company}&service=${service}&service_type=${serviceType}`)
//         .then(response => response.json())
//         .then(data => {
//             const uniqueCompanies = {};

//             data.results.forEach(result => {
//                 const companyName = result.name;
//                 const latitude = result.latitude;
//                 const longititude = result.longititude;
//                 const from = result.from;
//                 const to = result.to

//                 if (latitude !== undefined && longititude !== undefined) {
//                     const coordinates = [latitude, longititude];
//                     if (!uniqueCompanies[companyName]) {
//                         uniqueCompanies[companyName] = coordinates;
//                     }
//                 } else {
//                     console.error(`Invalid coordinates for company: ${companyName}`);
//                 }
//             });

//             markers.forEach(marker => map.removeLayer(marker));
//             markers.clear();

//             Object.keys(uniqueCompanies).forEach(companyName => {
//                 const coords = uniqueCompanies[companyName];
//                 var marker = L.marker(coords).bindPopup(`<b>${companyName}</b>`);
//                 markers.add(marker);
//             });

//             markers.forEach(marker => {
//                 marker.addTo(map);
//             });

//             console.log(markers);
//         });
// });

var map;
let markers = []; // Масив для маркерів компаній
let priceMarkers = []; // Масив для маркерів з цінами

document.addEventListener('DOMContentLoaded', function () {
    map = L.map('map').setView([49.8397, 24.0297], 12);
    map.zoomControl.remove();
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    loadCompanies();
    loadDropdownData();
});

function loadCompanies() {
    fetch('/services/')
        .then(response => response.json())
        .then(data => {
            // Видаляємо старі маркери перед додаванням нових
            markers.forEach(marker => map.removeLayer(marker));
            markers = [];

            data.companies.forEach(company => {
                var marker = L.marker([company.latitude, company.longititude])
                    .bindPopup(`<b>${company.name}</b>`);
                markers.push(marker);
            });

            markers.forEach(marker => marker.addTo(map));
        });
}

function loadDropdownData() {
    fetch('/data/')
        .then(response => response.json())
        .then(data => {
            const serviceTypeSelect = document.getElementById('serviceTypeSelect');
            const serviceSelect = document.getElementById('serviceSelect');
            const companySelect = document.getElementById('companySelect');

            data.service_types.forEach(type => {
                const option = document.createElement('option');
                option.value = type.id;
                option.text = type.name;
                serviceTypeSelect.appendChild(option);
            });

            data.services.forEach(service => {
                const option = document.createElement('option');
                option.value = service.id;
                option.text = service.name;
                serviceSelect.appendChild(option);
            });

            data.companies.forEach(company => {
                const option = document.createElement('option');
                option.value = company.id;
                option.text = company.name;
                companySelect.appendChild(option);
            });
        });
}

document.getElementById('applyFiltersBtn').addEventListener('click', function () {
    const serviceType = document.getElementById('serviceTypeSelect').value;
    const service = document.getElementById('serviceSelect').value;
    const company = document.getElementById('companySelect').value;

    // Видаляємо всі старі маркери перед додаванням нових
    markers.forEach(marker => map.removeLayer(marker));
    markers = [];

    // Видаляємо всі маркери з цінами
    priceMarkers.forEach(marker => map.removeLayer(marker));
    priceMarkers = [];

    fetch(`/filter/?company=${company}&service=${service}&service_type=${serviceType}`)
        .then(response => response.json())
        .then(data => {
            const uniqueCompanies = {};
            const showPrice = service !== ""; // Відображати ціну тільки якщо вибрано послугу

            data.results.forEach(result => {
                const companyName = result.name;
                const latitude = result.latitude;
                const longititude = result.longititude;
                const from = result.from;
                const to = result.to;

                if (latitude !== undefined && longititude !== undefined) {
                    const coordinates = [latitude, longititude];
                    uniqueCompanies[companyName] = { coords: coordinates, from, to };
                } else {
                    console.error(`Invalid coordinates for company: ${companyName}`);
                }
            });

            Object.keys(uniqueCompanies).forEach(companyName => {
                const { coords, from, to } = uniqueCompanies[companyName];

                // Додаємо маркер компанії
                const companyMarker = L.marker(coords).bindPopup(`<b>${companyName}</b>`);
                markers.push(companyMarker);
                companyMarker.addTo(map);

                // Додаємо маркер з ціною, якщо вибрано послугу
                if (showPrice) {
                    const priceInfo = to ? `${from} - ${to}` : from;
                    const priceMarker = L.marker(coords, {
                        icon: L.divIcon({
                            className: 'price-label',
                            html: `<div class="price-text">${priceInfo}</div>`,
                            iconSize: [50, 20], // Розмір контейнера
                            iconAnchor: [25, 30] // Зміщення контейнера вгору
                        })
                    }).addTo(map);
                    priceMarkers.push(priceMarker);
                }
            });
        });
});
