function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setLanguage(lang) {
    fetch(`/api/auth/set-language/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ language_preference: lang })
    }).then(() => {
        window.location.reload();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const languageLinks = document.querySelectorAll('[href*="?lang="]');
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const lang = this.href.split('lang=')[1];
            setLanguage(lang);
        });
    });
});
