document.addEventListener('DOMContentLoaded', function() {
    // افزودن کلاس فعال به عناصر
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add('active');
        }
    });

    // مدیریت رنگ دکمه‌ها
    document.querySelectorAll('.btn').forEach(btn => {
        if (btn.classList.contains('btn-primary')) {
            btn.style.setProperty('background', 'var(--tg-accent)', 'important');
            btn.style.setProperty('border-color', 'var(--tg-primary)', 'important');
            btn.style.setProperty('color', 'var(--tg-background)', 'important');
            
            // افزودن افکت hover
            btn.addEventListener('mouseenter', function() {
                this.style.setProperty('background', 'var(--tg-primary)', 'important');
                this.style.setProperty('transform', 'translateY(-2px)', 'important');
                this.style.setProperty('box-shadow', 'var(--shadow-sm)', 'important');
            });
            
            btn.addEventListener('mouseleave', function() {
                this.style.setProperty('background', 'var(--tg-accent)', 'important');
                this.style.setProperty('transform', 'translateY(0)', 'important');
                this.style.setProperty('box-shadow', 'none', 'important');
            });
        }
    });

    // افزودن انیمیشن به جدول‌ها
    const tables = document.querySelectorAll('table');
    tables.forEach(table => {
        table.classList.add('fade-in');
    });
    
    // بهبود تجربه کاربری در فرم‌ها
    const formInputs = document.querySelectorAll('.form-control');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.setProperty('border-color', 'var(--tg-secondary)', 'important');
            this.style.setProperty('box-shadow', '0 0 0 3px rgba(163, 177, 138, 0.3)', 'important');
        });
        input.addEventListener('blur', function() {
            this.style.setProperty('border-color', 'var(--tg-border)', 'important');
            this.style.setProperty('box-shadow', 'none', 'important');
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
    
    // رفع مشکل کش مرورگر
    if (window.performance) {
        if (performance.navigation.type === 1) {
            window.location.reload(true);
        }
    }
    console.log('Admin custom JS loaded!'); // باید در کنسول دیده شود
});


// // اسکریپت‌های سفارشی برای پنل ادمین
// document.addEventListener('DOMContentLoaded', function() {
//     // افزودن انیمیشن به جدول‌ها
//     const tables = document.querySelectorAll('table');
//     tables.forEach(table => {
//         table.classList.add('fade-in');
//     });
    
//     // بهبود تجربه کاربری در فرم‌ها
//     const formInputs = document.querySelectorAll('.form-control');
//     formInputs.forEach(input => {
//         input.addEventListener('focus', function() {
//             this.parentElement.classList.add('focus');
//         });
//         input.addEventListener('blur', function() {
//             this.parentElement.classList.remove('focus');
//         });
//     });
    
//     // نمایش توضیحات هنگام هاور روی آیکون‌ها
//     const helpIcons = document.querySelectorAll('.help');
//     helpIcons.forEach(icon => {
//         icon.addEventListener('mouseover', function() {
//             const tooltip = this.nextElementSibling;
//             if (tooltip && tooltip.classList.contains('tooltip')) {
//                 tooltip.style.display = 'block';
//             }
//         });
//         icon.addEventListener('mouseout', function() {
//             const tooltip = this.nextElementSibling;
//             if (tooltip && tooltip.classList.contains('tooltip')) {
//                 tooltip.style.display = 'none';
//             }
//         });
//     });
    
//     // افزودن confirm به دکمه‌های حذف
//     const deleteButtons = document.querySelectorAll('.deletelink');
//     deleteButtons.forEach(button => {
//         button.addEventListener('click', function(e) {
//             if (!confirm('آیا از حذف این آیتم مطمئن هستید؟ این عمل غیرقابل بازگشت است.')) {
//                 e.preventDefault();
//             }
//         });
//     });
// });