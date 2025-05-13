document.addEventListener('DOMContentLoaded', function() {
    // تغییر رنگ دینامیک عناصر خاص
    const primaryElements = document.querySelectorAll('.bg-primary');
    primaryElements.forEach(el => {
        el.style.backgroundColor = '#344E41';
    });
});