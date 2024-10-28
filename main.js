function btn() {
    const content = document.getElementById('content');
    const steps = document.querySelectorAll('.step');
    steps.forEach(s => s.style.display = 'none');
        content.style.display = 'block';
}
function btnc() {
    const content = document.getElementById('contentc');
    content.innerHTML = '<h3>Ini PEngeliatan</h3>';
}
