// 이미 로드된 데이터를 전역 변수로 저장합니다.
let resultsHellomarket = [];
let resultsJoongonara = [];
let resultsFruitfamily = [];
let resultsYes24 = [];
let resultsAladin = [];

document.addEventListener('DOMContentLoaded', () => {
    // HTML에서 데이터를 추출하여 JavaScript 변수에 저장합니다.
    const hellomarketData = JSON.parse(document.getElementById('hellomarket-data').textContent);
    const joongonaraData = JSON.parse(document.getElementById('joongonara-data').textContent);
    const fruitfamilyData = JSON.parse(document.getElementById('fruitfamily-data').textContent);
    const yes24Data = JSON.parse(document.getElementById('yes24-data').textContent);
    const aladinData = JSON.parse(document.getElementById('aladin-data').textContent);

    resultsHellomarket = hellomarketData;
    resultsJoongonara = joongonaraData;
    resultsFruitfamily = fruitfamilyData;
    resultsYes24 = yes24Data;
    resultsAladin = aladinData;
});

function sortResults() {
    // "낮은 가격순"으로 정렬합니다.
    resultsHellomarket.sort((a, b) => parseInt(a[1].replace(/[^0-9]/g, '')) - parseInt(b[1].replace(/[^0-9]/g, '')));
    resultsJoongonara.sort((a, b) => parseInt(a[1].replace(/[^0-9]/g, '')) - parseInt(b[1].replace(/[^0-9]/g, '')));
    resultsFruitfamily.sort((a, b) => parseInt(a[1].replace(/[^0-9]/g, '')) - parseInt(b[1].replace(/[^0-9]/g, '')));
    resultsYes24.sort((a, b) => parseInt(a[1].replace(/[^0-9]/g, '')) - parseInt(b[1].replace(/[^0-9]/g, '')));
    resultsAladin.sort((a, b) => parseInt(a[1].replace(/[^0-9]/g, '')) - parseInt(b[1].replace(/[^0-9]/g, '')));

    // 업데이트된 결과를 화면에 표시합니다.
    updateResults();
}

function updateResults() {
    const hellomarketSection = document.getElementById('hellomarket-results');
    const joongonaraSection = document.getElementById('joongonara-results');
    const fruitfamilySection = document.getElementById('fruitfamily-results');
    const yes24Section = document.getElementById('yes24-results');
    const aladinSection = document.getElementById('aladin-results');

    // 결과 섹션을 비웁니다.
    hellomarketSection.innerHTML = '';
    joongonaraSection.innerHTML = '';
    fruitfamilySection.innerHTML = '';
    yes24Section.innerHTML = '';
    aladinSection.innerHTML = '';

    // 헬로마켓 결과 업데이트
    resultsHellomarket.forEach(item => {
        const itemDiv = document.createElement('li');
        itemDiv.innerHTML = `
            <img src="${item[3]}" alt="${item[0]}" width="100"><br>
            <strong>${item[0]}</strong>: ${item[1]} <br>
            <a href="${item[2]}" target="_blank">상품 보기</a>
        `;
        hellomarketSection.appendChild(itemDiv);
    });

    // 중고나라 결과 업데이트
    resultsJoongonara.forEach(item => {
        const itemDiv = document.createElement('li');
        itemDiv.innerHTML = `
            <img src="${item[3]}" alt="${item[0]}" width="100"><br>
            <strong>${item[0]}</strong>: ${item[1]} <br>
            <a href="${item[2]}" target="_blank">상품 보기</a>
        `;
        joongonaraSection.appendChild(itemDiv);
    });

    // 후루츠패밀리 결과 업데이트
    resultsFruitfamily.forEach(item => {
        const itemDiv = document.createElement('li');
        itemDiv.innerHTML = `
            <img src="${item[3]}" alt="${item[0]}" width="100"><br>
            <strong>${item[0]}</strong>: ${item[1]} <br>
            <a href="${item[2]}" target="_blank">상품 보기</a>
        `;
        fruitfamilySection.appendChild(itemDiv);
    });

    // 예스24 결과 업데이트
    resultsYes24.forEach(item => {
        const itemDiv = document.createElement('li');
        itemDiv.innerHTML = `
            <img src="${item[3]}" alt="${item[0]}" width="100"><br>
            <strong>${item[0]}</strong>: ${item[1]} <br>
            <a href="${item[2]}" target="_blank">상품 보기</a>
        `;
        yes24Section.appendChild(itemDiv);
    });

    // 알라딘 결과 업데이트
    resultsAladin.forEach(item => {
        const itemDiv = document.createElement('li');
        itemDiv.innerHTML = `
            <img src="${item[3]}" alt="${item[0]}" width="100"><br>
            <strong>${item[0]}</strong>: ${item[1]} <br>
            <a href="${item[2]}" target="_blank">상품 보기</a>
        `;
        aladinSection.appendChild(itemDiv);
    });
}
