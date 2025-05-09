document.addEventListener('DOMContentLoaded', function() {
    // عناصر اصلی
    const modeSwitcher = document.querySelector('.mode-switcher-btn');
    const htmlElement = document.documentElement;
    
    // تنظیم تم اولیه با اولویت‌بندی:
    // 1. انتخاب کاربر از localStorage
    // 2. تنظیمات سیستم عامل
    // 3. حالت پیش‌فرض (light)
    const storedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = storedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    // اعمال تم اولیه
    applyTheme(initialTheme);
    
    // رویداد کلیک برای تغییر تم
    if (modeSwitcher) {
        modeSwitcher.addEventListener('click', function() {
            const currentTheme = htmlElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            applyTheme(newTheme);
            
            // ذخیره انتخاب کاربر
            localStorage.setItem('theme', newTheme);
            
            // ارسال رویداد سفارشی برای سایر اسکریپت‌ها
            document.dispatchEvent(new CustomEvent('themeChanged', {
                detail: { theme: newTheme }
            }));
        });
    }
    
    // گوش دادن به تغییرات سیستم
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        // فقط اگر کاربر قبلاً انتخابی نکرده باشد
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            applyTheme(newTheme);
        }
    });
    
    // تابع اعمال تم
    function applyTheme(theme) {
        // اضافه کردن کلاس برای انیمیشن‌های روان
        htmlElement.classList.add('theme-transition');
        
        // اعمال تم جدید
        htmlElement.setAttribute('data-theme', theme);
        
        // به‌روزرسانی آیکون
        updateModeIcon(theme);
        
        // حذف کلاس انیمیشن پس از اتمام
        setTimeout(() => {
            htmlElement.classList.remove('theme-transition');
        }, 400);
    }
    
    // تابع به‌روزرسانی آیکون
    function updateModeIcon(theme) {
        const lightIcon = document.querySelector('.light-icon');
        const darkIcon = document.querySelector('.dark-icon');
        
        if (theme === 'dark') {
            if (lightIcon) {
                lightIcon.style.opacity = '0';
                lightIcon.style.transform = 'scale(0.5) rotate(-90deg)';
            }
            if (darkIcon) {
                darkIcon.style.opacity = '1';
                darkIcon.style.transform = 'scale(1) rotate(0deg)';
            }
        } else {
            if (lightIcon) {
                lightIcon.style.opacity = '1';
                lightIcon.style.transform = 'scale(1) rotate(0deg)';
            }
            if (darkIcon) {
                darkIcon.style.opacity = '0';
                darkIcon.style.transform = 'scale(0.5) rotate(90deg)';
            }
        }
    }
    
    // جلوگیری از فلاش محتوای سفید (FOUT)
    (function() {
        // اعمال سریع تم قبل از لود کامل صفحه
        htmlElement.setAttribute('data-theme', initialTheme);
        
        // اضافه کردن کلاس برای کنترل انیمیشن‌های اولیه
        htmlElement.classList.add('theme-loading');
        
        // حذف کلاس پس از لود کامل صفحه
        window.addEventListener('load', function() {
            setTimeout(() => {
                htmlElement.classList.remove('theme-loading');
            }, 100);
        });
    })();
});