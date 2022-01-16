const getCounter = (api, page) => {
  const url = `${api}/get_counter?code=zaoSONFT/a46xuxkCGHFGU9DZ5e9GMWLYj7MWGgFTNmL7frIjSla1w==&page=${page}`

  fetch(
    url,
    { headers: { 'Access-Control-Allow-Origin': 'http://localhost:4000', 'Access-Control-Allow-Methods': 'GET' } }
  )
    .then((response) => {
      return response.json()
    })
    .then((response) => {
      console.log(response)
      document.getElementById('counter-value').innerHTML = response.counter
    })
}

const updateCounter = (api, page) => {
  const url = `${api}/update_counter?code=DyKh//KzE7BhrZWyZKiaaBnvJqqemF3zzaP/RgH2eQsgsBZ6jdV7lg==`

  fetch(url, {
    method: 'POST',
    body: JSON.stringify({ page })
  })
    .then((response) => {
      getCounter(api, page)
    })
}

(function () {
  "use strict";

  window.addEventListener('load', () => {
    on_page_load()
  });

  /**
   * Function gets called when page is loaded.
   */
  function on_page_load() {
    // Initialize On-scroll Animations
    AOS.init({
      anchorPlacement: 'top-left',
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
      disable: 'mobile'
    });
  }

  /**
   * Navbar effects and scrolltop buttons upon scrolling
   */
  const navbar = document.getElementById('header-nav')
  var body = document.getElementsByTagName("body")[0]
  const scrollTop = document.getElementById('scrolltop')
  window.onscroll = () => {
    if (window.scrollY > 0) {
      navbar.classList.add('fixed-top', 'shadow-sm')
      body.style.paddingTop = navbar.offsetHeight + "px"
      scrollTop.style.visibility = "visible";
      scrollTop.style.opacity = 1;
    } else {
      navbar.classList.remove('fixed-top', 'shadow-sm')
      body.style.paddingTop = "0px"
      scrollTop.style.visibility = "hidden";
      scrollTop.style.opacity = 0;
    }
  };

  /**
   * Masonry Grid
   */
  var elem = document.querySelector('.grid');
  if (elem) {
    imagesLoaded(elem, function () {
      try {
        new Masonry(elem, {
          itemSelector: '.grid-item',
          percentPosition: true,
          horizontalOrder: true
        });
      } catch (error) {
        console.error(error)
      }
    })
  }

  /**
   * Big Picture Popup for images and videos
   */
  document.querySelectorAll("[data-bigpicture]").forEach((function (e) {
    e.addEventListener("click", (function (t) {
      t.preventDefault();
      const data = JSON.parse(e.dataset.bigpicture)
      BigPicture({
        el: t.target,
        ...data
      })
    })
    )
  }))

  /**
   * Big Picture Popup for Photo Gallary
   */
  document.querySelectorAll(".bp-gallery a").forEach((function (e) {
    var caption = e.querySelector('figcaption')
    var img = e.querySelector('img')
    // set the link present on the item to the caption in full view
    img.dataset.caption = '<a class="link-light" target="_blank" href="' + e.href + '">' + caption.innerHTML + '</a>';
    window.console.log(caption, img)
    e.addEventListener("click", (function (t) {
      t.preventDefault();
      BigPicture({
        el: t.target,
        gallery: '.bp-gallery',
      })
    })
    )
  }))

  // Add your javascript here
  const apiEndpoint = 'https://acg-resume-az-dev-counter.azurewebsites.net/api'

  updateCounter(apiEndpoint, 'home')
})();