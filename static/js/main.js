$(function () {
    $(".hamburger").on("click", function() {
        $(".menu").toggleClass("active");
        $(".hamburger").toggleClass("active");
        $(".mobmenu").toggleClass("active");
    });
    while ($(".menu").hasClass("active")) {
        $(screen).on("click", function() {
            $(".menu").removeClass("active");
        });
    }
});

$(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 1) {
            $(".menu").addClass('active');
        } else {
            $(".menu").removeClass('active');
        }
    });
});

$(function () {
    $(document).on('click', 'a[href^="#"]', function (event) {
        event.preventDefault();

        $('html, body').animate({
            scrollTop: $($.attr(this, 'href')).offset().top
        }, 500);
    });
});

const swiper = new Swiper('.swiper', {
    // Optional parameters
    loop: true,
    slidesPerView: 3,
    direction: 'horizontal',
    centeredSlides: true,
    // Navigation arrows
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    coverflowEffect: {
        rotate: 30,
        slideShadows: false,
    },
    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 5
        },
        576: {
            slidesPerView: 1,
            spaceBetween: 10
        },
        768: {
            slidesPerView: 2,
            spaceBetween: 20
        },
        992: {
            slidesPerView: 2,
            spaceBetween: 50,
        }
        
    },
    slideNextClass: 'slider-next',
    slidePrevClass: 'slider-prev',
    slideActiveClass: 'slider-active',
    
});

const myswiper = new Swiper('.my-swiper', {
    // Optional parameters
    loop: true,
    slidesPerView: 2,
    spaceBetween: 20,
    direction: 'horizontal',
    centeredSlides: true,
    // autoplay: {
    //     delay: 5000,
    // },
    breakpoints: {
        320: {
            slidesPerView: 1,
            spaceBetween: 10
        },
        576: {
            slidesPerView: 2,
            spaceBetween: 30
        }

    }

});

// focus content
const animItems = document.querySelectorAll('.anim-items');

if (animItems.length > 0) {
    window.addEventListener('scroll', animOnScroll);

    function animOnScroll(params) {
        for (let index = 0; index < animItems.length; index++) {
            const animItem = animItems[index];
            const animItemHeight = animItem.offsetHeight;
            const animItemOffset = offset(animItem).top;
            const animStart = 4;

            let animItemPoint = window.innerHeight - animItemHeight / animStart;

            if (animItemHeight > window.innerHeight) {
                animItemPoint = window.innerHeight - window.innerHeight / animStart;
            }
            if ((pageYOffset > animItemOffset - animItemPoint) && pageYOffset < (animItemOffset + animItemHeight)) {
                animItem.classList.add('active');
            } else {
                if (!animItem.classList.contains('anim-no-hide')) {
                    animItem.classList.remove('active');
                }
            }
        }

    }

    function offset(el) {
        const rect = el.getBoundingClientRect(),
            scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
        scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        return { top: rect.top + scrollTop, left: rect.left + scrollLeft };

    }
    animOnScroll();
}











    
