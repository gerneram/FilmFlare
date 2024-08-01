document.addEventListener("DOMContentLoaded", function () {
    let box = document.querySelector('.box');
    let dots = document.querySelectorAll('.dot');
    let images = box.querySelectorAll('span img');
    let BackForCarousel = document.querySelector('.new_cinema')
    let currentDegree = 0;
    let currentImageIndex = 0;

    box.style.transform = `perspective(1000px) rotateY(${currentDegree}deg)`;
    function adjustTranslateZ() {
        var width = window.innerWidth;
        var baseTranslateZ = 200;
        var difference = Math.max(1200 - width, 0) / 100;
        var newTranslateZ = baseTranslateZ - (difference * 18);
        var elements = document.querySelectorAll('.box span');
        elements.forEach(function (el, index) {
            // Используйте getComputedStyle для доступа к CSS переменной
            var i = parseInt(getComputedStyle(el).getPropertyValue('--i'), 10);
            el.style.transform = `translate(-50%, -50%) rotateY(${i * 45}deg) translateZ(${newTranslateZ}px)`;
        });
    }

    // Устанавливаем начальное значение translateZ
    adjustTranslateZ();

    // Устанавливаем обработчик на изменение размера окна
    window.addEventListener('resize', adjustTranslateZ);
    function setActiveDot(index) {
        dots.forEach(dot => dot.classList.remove('active'));
        dots[index].classList.add('active');
    }
    function updateVideo(index) {
        const videoElement = document.querySelector('.bg_video');
        const videoSource = images[index].getAttribute('data-video');
        videoElement.querySelector('.carousel_trailer').src = videoSource;
        videoElement.load();
        videoElement.play();
    }
    function setTitle(index) {
        const aboutCinemaElement = document.querySelector('.Title_for_film');
        const title = images[index].getAttribute('data-title');
        aboutCinemaElement.textContent = title;
    }
    function setDescription(index) {
        const TextToFilm = document.querySelector('.Text_for_film');
        const description = images[index].getAttribute('data-description');
        TextToFilm.textContent = description;
    }

    function setActiveImage(index) {
        images.forEach(image => image.style.filter = "brightness(0.5)");
        images[index].style.filter = "brightness(1)";
        updateVideo(index);
        setDescription(index);
        setTitle(index);
    }


    // Установка активного изображения при загрузке
    setActiveImage(currentImageIndex);

    dots.forEach(dot => {
        dot.addEventListener('click', function () {
            let index = parseInt(dot.getAttribute('data-index'));
            currentImageIndex = index;
            currentDegree = -index * 45;
            box.style.transform = `perspective(1000px) rotateY(${currentDegree}deg)`;
            setActiveDot(index);
            setActiveImage(index);
        });
    });

    document.querySelector('.control-right').addEventListener('click', function () {
        currentImageIndex = (currentImageIndex + 1) % dots.length;
        currentDegree = -currentImageIndex * 45;
        box.style.transform = `perspective(1000px) rotateY(${currentDegree}deg)`;
        setActiveDot(currentImageIndex);
        setActiveImage(currentImageIndex);
    });

    document.querySelector('.control-left').addEventListener('click', function () {
        currentImageIndex = (currentImageIndex - 1 + dots.length) % dots.length;
        currentDegree = -currentImageIndex * 45;
        box.style.transform = `perspective(1000px) rotateY(${currentDegree}deg)`;
        setActiveDot(currentImageIndex);
        setActiveImage(currentImageIndex);
    });

    setInterval(function () {
        document.querySelector('.control-right').click();
    }, 90000);

    document.querySelector('.sound-toggle').addEventListener('click', function () {
        const videoElement = document.querySelector('.bg_video');
        console.log("Button clicked!");
        // Проверьте, включен ли звук у видео
        if (videoElement.muted) {
            videoElement.muted = false;
            this.textContent = "🔊";  // Измените иконку на звук
        } else {
            videoElement.muted = true;
            this.textContent = "🔇";  // Измените иконку на беззвучный
        }
    });
    window.onresize = function () {
        var videoHeight = document.getElementById('trailer').offsetHeight;
        var commentsSection = document.querySelector('.comments-section');
        var commentForm = document.getElementById('commentForm');
        var commentText = document.getElementById('commentText');
        var submitButton = commentForm.querySelector('button[type="submit"]');

        // Установка высоты блока комментариев равной видео
        commentsSection.style.height = videoHeight + 'px';

        // Расчёт высоты формы и текстового поля
        var formHeight = videoHeight * 0.4; // 40% от видео
        commentForm.style.height = formHeight + 'px';

        // Установка высоты кнопки
        var buttonHeight = formHeight * 0.2; // 20% от формы
        submitButton.style.height = buttonHeight + 'px';

        // Установка высоты текстового поля
        var textAreaHeight = formHeight - buttonHeight; // Оставшаяся часть от формы
        commentText.style.height = textAreaHeight + 'px';
    };


    document.addEventListener("DOMContentLoaded", function () {
        const firstPageBtn = document.getElementById("firstPageBtn");
        const secondPageBtn = document.getElementById("secondPageBtn");
        const firstPage = document.getElementById("firstPage");
        const secondPage = document.getElementById("secondPage");

        firstPageBtn.addEventListener("click", function () {
            firstPage.style.transform = "translateY(0)";
            secondPage.style.transform = "translateY(100%)";
        });

        secondPageBtn.addEventListener("click", function () {
            firstPage.style.transform = "translateY(-100%)";
            secondPage.style.transform = "translateY(0)";
        });
    });
});


$(document).ready(function () {
    loadMovies('all');

    $(".control-item").click(function () {
        var genre_id = $(this).data('id');
        var genre_text = $(this).text();
        loadMovies(genre_id, genre_text);
    });
});
var filmid = 0;
function loadMovies(genre_id, genre_text) {
    var url = '/get_movies/';
    if (genre_id && genre_id !== 'all') {
        url += '?genre=' + genre_id;
    }

    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            $(".All_cinemas").empty();
            var header = genre_text ? genre_text : 'все фильмы';
            $(".All_cinemas").append("<h1>" + header + "</h1>");
            $(".All_cinemas").append("<div class='movie-container'></div>");

            $.each(response.movies, function (i, movie) {
                var movieItem = $(
                    `<div class="movie-item" onclick="showTrailer('${movie.trailer_url}', ${movie.id})" data-film-id="${movie.id}">
            <img src="${movie.image_url}" alt="${movie.title}">
            <h3>${movie.title}</h3>
            </div>`
                );
                $(".All_cinemas .movie-container").append(movieItem);
            });
        }
    });
}

window.onload = function () {
    const spans = document.querySelectorAll('.box span');
    maxHeight = 0;

    spans.forEach(span => {
        maxHeight = Math.max(maxHeight, span.offsetHeight);
    });
    const carouselContainer = document.querySelector('.carousel-container');
    carouselContainer.style.height = `${maxHeight}px`;
};

function loadComments(filmId) {
    $.ajax({
        url: '/get_comments/' + filmId + '/',
        type: 'GET',
        success: function (response) {
            var commentsList = $('#commentsList');
            commentsList.empty(); // Очищаем список комментариев
            $.each(response.comments, function (i, comment) {
                commentsList.append('<li>' + comment.text + '</li>');
            });
        }
    });
}


// Функция для отображения трейлера
function showTrailer(trailerUrl, filmId) {
    loadComments(filmId);
    var videoElement = document.getElementById('trailer');
    if (trailerUrl.includes('youtube.com') || trailerUrl.includes('youtu.be')) {
        trailerUrl = trailerUrl.replace('watch?v=', 'embed/')
    }
    videoElement.src = trailerUrl;
    $('#myModal').show();
    videoElement.onloadedmetadata = function () {
        window.onresize();

    };

    // Сохранение filmId в глобальной переменной (или использование другого способа для его сохранения)
    $('#myModal').data('film-id', filmId); // Теперь это свойство доступно глобально
}

// Закрытие модального окна и остановка воспроизведения видео
/*$(document).on('click', '.close', function () {   
    $('#myModal').hide();
    $('#video').attr('src', '');
});*/
$(window).on('click', function (event) {
    if ($(event.target).is('#myModal')) {
        $('#myModal').hide();
        $('#trailer').attr('src', '');
    }
});

$('#commentForm').submit(function (e) {
    e.preventDefault(); // Предотвращение обычной отправки формы

    var commentText = $('#commentText').val();
    var filmId = $('#myModal').data('film-id'); // Получение filmId из данных модального окна

    // Важно: проверяем, что filmId был установлен
    if (!filmId) {
        alert('Не выбран фильм для комментирования!');
        return;
    }

    if (commentText.trim() === '') {
        alert('Комментарий не может быть пустым!');
        return;
    }

    // AJAX-запрос на сервер для сохранения комментария
    $.ajax({
        url: '/add_comment/' + filmId + '/',
        type: 'POST',
        data: {
            'text': commentText,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
        },
        success: function (response) {
            if (response.success) {
                $('#commentsList').append('<li class="commentText">' + commentText + '</li>');
                $('#commentText').val('');
            } else {
                alert('Ошибка при добавлении комментария: ' + response.error);
            }
        }
    });
});







