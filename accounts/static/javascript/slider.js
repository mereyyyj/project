let currentIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

function showSlide(index) {
    slides.forEach((slide, i) => {
        slide.style.display = (i === index) ? 'block' : 'none';
        dots[i].classList.toggle('active', i === index);
    });
    currentIndex = index;
}

setInterval(() => {
    let next = (currentIndex + 1) % slides.length;
    showSlide(next);
}, 5000);

document.addEventListener("DOMContentLoaded", () => {
    showSlide(0);
});
