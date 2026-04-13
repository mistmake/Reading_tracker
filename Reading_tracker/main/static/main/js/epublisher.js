function uploadEpub() {
    const fileInput = document.getElementById('epubFileInput');
    const file = fileInput.files[0];

    if (file) {
        if (file.name.endsWith('.epub')) {
            // логика для отправки на сервер педик ты
        } else {
            alert('Пожалуйста, выберите файл с расширением .epub');
        }
    } else {
        alert('Пожалуйста, выберите файл для загрузки');
    }
}