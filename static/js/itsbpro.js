jQuery(document).ready(function () {
  let toggleFixMenu = () => {
    if ($(window).width() > 860) {
      if ($(window).scrollTop() >= 400) {
        $(".nav").addClass("nav_fixed");
      } else {
        $(".nav").removeClass("nav_fixed");
      }
    } else {
      $(".nav").removeClass("nav_fixed");
    }
  };
  let scaleMenuItemHr = () => {
    $(".nav__link-wrap").hover(
      function () {
        $(this)
          .children(".nav__top-hr")
          .width($(this).children(".nav__link").width());
      },
      function () {
        $(this).children(".nav__top-hr").width(0);
      }
    );
  };
  let showImg = () => {
    let images = document.querySelectorAll('.lazy-img');
    images.forEach((img) => {
      if ($(window).scrollTop() + $(window).height() - img.offsetTop >= -100) {
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.dataset.src = '';
          img.classList.add('lazy_loaded');
        }
      }
    })
  };
  let toggleNav = () => {
    $(".nav").toggleClass("nav_fixed");
    $(".nav").toggleClass("nav_full-height");
  };
  let linkStop = () => {
    $("a").each(function (item) {
      if ($(this).attr("href") == "#" || $(this).attr("href") == "") {
        $(this).attr("href", "404.php");
      }
    });
  };

  // $(".inside-partners").slick({
  //   infinite: true,
  //   speed: 500,
  //   slidesToShow: 4,
  //   arrows: true,
  //   prevArrow:
  //     '<div class="arrow-wrap"><i class="fas fa-chevron-left"></i></div>',
  //   nextArrow:
  //     '<div class="arrow-wrap"><i class="fas fa-chevron-right"></i></div>',
  //   appendArrows: $(".arrow-wrapper"),
  //   slidesToScroll: 1,
  //   autoplay: true,
  //   autoplaySpeed: 3000,
  //   responsive: [
  //     {
  //       breakpoint: 1025,
  //       settings: {
  //         slidesToShow: 3,
  //       },
  //     },
  //     {
  //       breakpoint: 861,
  //       settings: {
  //         slidesToShow: 2,
  //       },
  //     },
  //     {
  //       breakpoint: 641,
  //       settings: {
  //         slidesToShow: 1,
  //         autoplaySpeed: 1000,
  //         arrows: false,
  //       },
  //     },
  //   ],
  // });
  $(".nav__toggle-btn").click(toggleNav);
  $(window).scroll(() => {
    toggleFixMenu();
    showImg();
  });
  linkStop();
  showImg();
  scaleMenuItemHr();
  $(".modal__exit").click(() => {
    $(".modal").addClass("dn");
  });
  $(".main-form").submit(function (event) {
    if (!this.email.value) {
      event.preventDefault();
      let obj = {
        name: this.name.value,
        number: this.number.value,
        text: this.text.value,
      };
      this.name.value = "";
      this.number.value = "";
      this.text.value = "";
      $.ajax({
        url: "/send-smtp",
        data: obj,
        dataType: "html",
        method: "POST",
        beforeSend: () => {
          $(".modal").removeClass("dn");
        },
        success: (data) => {
          $(".modal__loading").addClass("dn");
          $(".modal__success").removeClass("dn");
        },
        error: () => {
          $(".modal__loading").addClass("dn");
          $(".modal__error").removeClass("dn");
        },
      });
    } else {
      $(".modal").removeClass("dn");
      $(".modal__success").removeClass("dn");
    }
  });
});
