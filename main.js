// Ini nyoba gua ngulas DOM dulu sekalian belaajr pake eventlistener
// funcion btn sama btnc itu make onClick di html jadi ga perlu pake button.addEventListener('click', () => {}
// Ini bikin tombol kalo dipencet, div yang classnya 'step' jadi hilang dihalaman trus diganti sama div yang classnya bukan 'step' id='content' yang dari sananya di style display none jadi block(ketampil)
function btn() {
    const content = document.getElementById('content');
    const steps = document.querySelectorAll('.step');
    steps.forEach(s => s.style.display = 'none');
        content.style.display = 'block';
};

// Ini DOM metode buat sintaks baru dari js ke html pas tombol dipencet
function btnc() {
    const content = document.getElementById('contentc');
    content.innerHTML = '<h3>Ini Pengeliatan</h3>';
};

// Ini kalo DOM pake addEventListener kan, ?
function tombol() {
    const button = document.getElementById('buttonku');
    const content = document.getElementById('kontenku');

    button.addEventListener('click', () => {
        content.style.display = 'block';
    });
