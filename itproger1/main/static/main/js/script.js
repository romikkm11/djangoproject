var map;
let markers = new Set();

document.addEventListener('DOMContentLoaded', function() {
    map = L.map('map').setView([49.8397, 24.0297], 13);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    fetch('/services/')
        .then(response => response.json())
        .then(data => {
            data.companies.forEach(company => {
                var marker = L.marker([company.latitude, company.longititude]).bindPopup(`<b>${company.name}</b>`);
                markers.add(marker);
            });

            markers.forEach(marker => {
                marker.addTo(map);
            });
        });

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
});


document.getElementById('applyFiltersBtn').addEventListener('click', function() {
    const serviceType = document.getElementById('serviceTypeSelect').value;
    const service = document.getElementById('serviceSelect').value;
    const company = document.getElementById('companySelect').value;

    fetch(`/filter/?company=${company}&service=${service}&service_type=${serviceType}`)
        .then(response => response.json())
        .then(data => {
            const uniqueCompanies = {};

            data.results.forEach(result => {
                const companyName = result.name;
                const latitude = result.latitude;
                const longititude = result.longititude;

                if (latitude !== undefined && longititude !== undefined) {
                    const coordinates = [latitude, longititude];
                    if (!uniqueCompanies[companyName]) {
                        uniqueCompanies[companyName] = coordinates;
                    }
                } else {
                    console.error(`Invalid coordinates for company: ${companyName}`);
                }
            });

            markers.forEach(marker => map.removeLayer(marker));
            markers.clear();

            Object.keys(uniqueCompanies).forEach(companyName => {
                const coords = uniqueCompanies[companyName];
                var marker = L.marker(coords).bindPopup(`<b>${companyName}</b>`);
                markers.add(marker);
            });

            markers.forEach(marker => {
                marker.addTo(map);
            });

            console.log(markers);
        });
});

