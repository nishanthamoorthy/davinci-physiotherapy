document.addEventListener('DOMContentLoaded', function () {

  // Preloader
  const preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', function () {
      preloader.classList.add('loaded');
      setTimeout(() => preloader.remove(), 500);
    });
    // Fallback in case load event already fired
    setTimeout(() => preloader.classList.add('loaded'), 1200);
  }

  // AOS animation init
  if (window.AOS) {
    AOS.init({ duration: 800, once: true, offset: 60 });
  }

  // Sticky navbar shadow on scroll
  const navbar = document.querySelector('.main-navbar');
  function handleScroll() {
    if (window.scrollY > 20) {
      navbar && navbar.classList.add('scrolled');
    } else {
      navbar && navbar.classList.remove('scrolled');
    }

    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
      backToTop.style.display = window.scrollY > 400 ? 'flex' : 'none';
    }
  }
  window.addEventListener('scroll', handleScroll);
  handleScroll();

  // Back to top button
  const backToTop = document.getElementById('backToTop');
  if (backToTop) {
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // Smooth scroll for in-page anchors
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId.length > 1) {
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });

  // Bootstrap form validation styling
  const forms = document.querySelectorAll('.needs-validation');
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');
    }, false);
  });

  // Auto-dismiss flash messages
  document.querySelectorAll('.alert-dismissible').forEach(alertEl => {
    setTimeout(() => {
      const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
      alert && alert.close();
    }, 5000);
  });

  // Lazy loading images (native attribute fallback helper)
  document.querySelectorAll('img[data-src]').forEach(img => {
    img.src = img.getAttribute('data-src');
    img.removeAttribute('data-src');
  });

  // Mobile sidebar toggle (admin)
  const sidebarToggle = document.getElementById('sidebarToggle');
  const adminSidebar = document.getElementById('adminSidebar');
  if (sidebarToggle && adminSidebar) {
    sidebarToggle.addEventListener('click', () => adminSidebar.classList.toggle('show'));
  }
});
