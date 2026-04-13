let currentChapterIndex = 0;

function displayChapter(index) {
    const chapterItems = document.querySelectorAll('#chapters li');
    const visibleItemsCount = 7;
    const halfVisible = Math.floor(visibleItemsCount / 2);

    chapterItems.forEach((item, idx) => {
        item.classList.remove('selected');
        item.classList.remove('chapter-item');
        if (idx == index) {
            item.classList.add("chapter-item");
        }
        else if (document.querySelector(`.chapter-content[data-chapter="${idx}"]`).style.display == 'block' && idx != index) {
            document.querySelector(`.chapter-content[data-chapter="${idx}"]`).style.display = 'none';
        }
    });

    chapterItems[index].classList.add('selected', 'chapter-item');
    currentChapterIndex = index;
    console.log(index);
    console.log(chapterItems[index].classList);
    document.querySelector(`.chapter-content[data-chapter="${index}"]`).style.display = 'block';
}


function displayPreviousChapter() {
    if (currentChapterIndex > 0) {
        displayChapter(currentChapterIndex - 1);
    }
}

function displayNextChapter() {
    const chapterItems = document.querySelectorAll('#chapters li');
    if (currentChapterIndex < chapterItems.length - 1) {
        displayChapter(currentChapterIndex + 1);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const chapterItems = document.querySelectorAll('#chapters li');
    console.log('ChapterItems');
    console.log(chapterItems);
    chapterItems.forEach((item, index) => {
        item.addEventListener('click', () => displayChapter(index));
    });

    const nextButton = document.querySelector('.forward-button');
    const backButton = document.querySelector('.back-button');

    nextButton.addEventListener('click', displayNextChapter);
    backButton.addEventListener('click', displayPreviousChapter);

    displayChapter(0); // Показать первую главу при загрузке
});
