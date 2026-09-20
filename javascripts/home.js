function animateCount(el, target) {
  var duration = 800;
  var start = performance.now();
  function step(now) {
    var progress = Math.min((now - start) / duration, 1);
    el.textContent = Math.round(progress * target);
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

function initHomeEffects() {
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length) {
    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -10% 0px" }
    );
    reveals.forEach(function (el) {
      // Only now does the element drop to opacity:0 (see home.css) —
      // arming and observing happen together so nothing goes invisible
      // without an observer already watching to bring it back.
      el.classList.add("reveal-armed");
      revealObserver.observe(el);
    });
  }

  var counters = document.querySelectorAll(".stat-number[data-target]");
  counters.forEach(function (el) {
    var target = parseInt(el.getAttribute("data-target"), 10) || 0;
    var counterObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            animateCount(el, target);
            counterObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    counterObserver.observe(el);
  });
}

/* Material's navigation.instant swaps page content without a full
   reload, so DOMContentLoaded won't refire on internal nav. document$
   is Material's own hook that fires after every page load, instant
   navigation included. */
if (typeof document$ !== "undefined") {
  document$.subscribe(initHomeEffects);
} else {
  document.addEventListener("DOMContentLoaded", initHomeEffects);
}
