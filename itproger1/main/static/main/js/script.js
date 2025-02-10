let map;
let markers = [];
let priceMarkers = [];

document.addEventListener('DOMContentLoaded', () => {
    initializeMap();
    loadCompanies();
    loadDropdownData();
    addEventListeners();
});

function initializeMap() {
    map = L.map('map').setView([49.8397, 24.0297], 12);
    map.zoomControl.remove();
    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; CartoDB'
    }).addTo(map);
}

function addEventListeners() {
    document.getElementById('toggleButton').addEventListener('click', () => {
        document.querySelector('aside').classList.toggle('hidden');
    });
    document.querySelectorAll('select').forEach(select => {
        select.addEventListener('change', applyFilters);
    });
}

function addElementToAside({ service, price, maxPrice, company }) {
    const serviceCard = document.createElement('div');
    serviceCard.classList.add('cardItem');
    serviceCard.innerHTML = `
        <div class="service">${service}</div>
        <div class="price">${price}${maxPrice ? ` - ${maxPrice}` : ''}</div>
        <div class="company">${company}</div>
    `;
    document.getElementById('aside').appendChild(serviceCard);
}

function addMarkerToMap(coords, companyName, priceInfo = '') {
    const companyMarker = L.marker(coords).bindPopup(`<b>${companyName}</b>`).addTo(map);
    markers.push(companyMarker);

    if (priceInfo) {
        const priceMarker = L.marker(coords, {
            icon: L.divIcon({
                className: 'price-label',
                html: `<div class="price-text">${priceInfo}</div>`,
                iconSize: [50, 20],
                iconAnchor: [25, 30]
            })
        }).addTo(map);
        priceMarkers.push(priceMarker);
    }
}

function clearAside() {
    document.getElementById('aside').innerHTML = '<h3>Список компаній</h3>';
}

function loadCompanies() {
    fetch('/services/')
        .then(response => response.json())
        .then(data => {
            clearMap();
            data.companies.forEach(({ latitude, longititude, name }) => {
                addMarkerToMap([latitude, longititude], name);
            });
        });
}

function populateDropdown(selectId, options) {
    const select = document.getElementById(selectId);
    select.innerHTML = '<option value="">Всі</option>';
    options.forEach(({ id, name }) => {
        const option = document.createElement('option');
        option.value = id;
        option.text = name;
        select.appendChild(option);
    });
}

function loadDropdownData() {
    fetch('/data/')
        .then(response => response.json())
        .then(({ service_types, services, companies, prices }) => {
            populateDropdown('serviceTypeSelect', service_types);
            populateDropdown('serviceSelect', services);
            populateDropdown('companySelect', companies);
            prices.forEach(card => addElementToAside({
                service: card['service__name'],
                price: card.min_price,
                maxPrice: card.max_price || '', 
                company: card['company__name']
            }));
        });
}

function clearMap() {
    markers.forEach(marker => map.removeLayer(marker));
    priceMarkers.forEach(marker => map.removeLayer(marker));
    markers = [];
    priceMarkers = [];
}

function applyFilters() {
    const serviceType = document.getElementById('serviceTypeSelect').value;
    const service = document.getElementById('serviceSelect').value;
    const company = document.getElementById('companySelect').value;

    clearMap();
    clearAside();

    fetch(`/filter/?company=${company}&service=${service}&service_type=${serviceType}`)
        .then(response => response.json())
        .then(data => {
            const uniqueCompanies = {};
            const showPrice = service !== "";

            data.results.forEach(({ name, latitude, longititude, from, to, service }) => {
                if (latitude !== undefined && longititude !== undefined) {
                    uniqueCompanies[name] = { coords: [latitude, longititude], from, to };
                    addElementToAside({
                        service,
                        price: from,
                        maxPrice: to ? to : '', 
                        company: name
                    });
                } else {
                    console.error(`Invalid coordinates for company: ${name}`);
                }
            });

            Object.entries(uniqueCompanies).forEach(([companyName, { coords, from, to }]) => {
                addMarkerToMap(coords, companyName, showPrice ? (to ? `${from} - ${to}` : from) : '');
            });
        });
}
