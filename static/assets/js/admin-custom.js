// اسکریپت‌های سفارشی برای پنل ادمین
document.addEventListener('DOMContentLoaded', function() {
    // افزودن انیمیشن به جدول‌ها
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.classList.add('fade-in');
    });
    
    // بهبود تجربه کاربری در فرم‌ها
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focus');
        });
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focus');
        });
    });
    
    // نمایش توضیحات هنگام هاور روی آیکون‌ها
    const helpIcons = document.querySelectorAll('.help');
    helpIcons.forEach(icon => {
        icon.addEventListener('mouseover', function() {
            const tooltip = this.nextElementSibling;
            if (tooltip && tooltip.classList.contains('tooltip')) {
                tooltip.style.display = 'block';
            }
        });
        icon.addEventListener('mouseout', function() {
            const tooltip = this.nextElementSibling;
            if (tooltip && tooltip.classList.contains('tooltip')) {
                tooltip.style.display = 'none';
            }
        });
    });
    
    // افزودن confirm به دکمه‌های حذف
    const deleteButtons = document.querySelectorAll('.deletelink');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('آیا از حذف این آیتم مطمئن هستید؟ این عمل غیرقابل بازگشت است.')) {
                e.preventDefault();
            }
        });
    });
});