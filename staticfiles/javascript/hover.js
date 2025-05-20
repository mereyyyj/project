document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('mouseover', function() {
        this.style.color = 'red';
    });
    link.addEventListener('mouseout', function() {
        this.style.color = 'blue';
    });
});