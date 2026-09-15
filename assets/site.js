(function () {
  var root = document.documentElement;
  var store = {
    get: function (key) { try { return localStorage.getItem(key); } catch (e) { return null; } },
    set: function (key, value) {
      try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, value); } catch (e) {}
    }
  };

  function applyTheme(mode) {
    if (mode === 'light' || mode === 'dark') root.setAttribute('data-theme', mode);
    else { root.removeAttribute('data-theme'); mode = 'auto'; }
    document.querySelectorAll('[data-theme-set]').forEach(function (button) {
      button.setAttribute('aria-pressed', String(button.getAttribute('data-theme-set') === mode));
    });
    return mode;
  }
  var theme = applyTheme(store.get('ag-theme'));
  function saveTheme(mode) {
    theme = applyTheme(mode);
    store.set('ag-theme', theme === 'auto' ? null : theme);
  }

  var greeting = document.querySelector('[data-greeting]');
  if (greeting) {
    var hour = new Date().getHours();
    var it = root.lang === 'it';
    greeting.textContent = hour >= 5 && hour < 12 ? (it ? 'Buongiorno' : 'Good morning')
      : hour >= 12 && hour < 18 ? (it ? 'Buon pomeriggio' : 'Good afternoon')
      : (it ? 'Buonasera' : 'Good evening');
  }

  document.addEventListener('click', function (event) {
    var target = event.target;

    var setTheme = target.closest('[data-theme-set]');
    if (setTheme) { saveTheme(setTheme.getAttribute('data-theme-set')); return; }
    if (target.closest('[data-theme-cycle]')) { saveTheme({ auto: 'light', light: 'dark', dark: 'auto' }[theme]); return; }

    var bio = target.closest('[data-bio]');
    if (bio) {
      var length = bio.getAttribute('data-bio');
      document.querySelectorAll('[data-bio]').forEach(function (b) { b.setAttribute('aria-pressed', String(b === bio)); });
      document.querySelectorAll('[data-bio-panel]').forEach(function (panel) { panel.hidden = panel.getAttribute('data-bio-panel') !== length; });
      return;
    }

    var tab = target.closest('[data-filter]');
    if (tab) {
      var filter = tab.getAttribute('data-filter');
      document.querySelectorAll('[data-filter]').forEach(function (t) { t.setAttribute('aria-selected', String(t === tab)); });
      document.querySelectorAll('[data-cat]').forEach(function (row) { row.hidden = filter !== 'all' && row.getAttribute('data-cat') !== filter; });
      return;
    }

    var copy = target.closest('[data-copy]');
    if (copy) {
      var label = copy.querySelector('span');
      var original = label.textContent;
      try {
        navigator.clipboard.writeText(copy.getAttribute('data-copy')).then(function () {
          label.textContent = copy.getAttribute('data-copied');
          setTimeout(function () { label.textContent = original; }, 1600);
        }, function () {});
      } catch (e) {}
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.metaKey || event.ctrlKey || event.altKey || event.defaultPrevented) return;
    var el = event.target;
    if (el && (el.isContentEditable || /^(INPUT|TEXTAREA|SELECT|BUTTON)$/.test(el.tagName))) return;
    var link = document.querySelector('.sidebar [data-shortcut="' + event.key + '"]');
    if (link) window.location.href = link.href;
  });

  var spot = document.querySelector('.spot');
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine) and (prefers-reduced-motion: no-preference)');
  if (spot) {
    var frame = 0, x = 0, y = 0;
    window.addEventListener('pointermove', function (event) {
      if (!finePointer.matches) return;
      x = event.clientX; y = event.clientY;
      if (!frame) frame = requestAnimationFrame(function () {
        spot.style.setProperty('--mx', x + 'px');
        spot.style.setProperty('--my', y + 'px');
        frame = 0;
      });
    }, { passive: true });
  }
})();
