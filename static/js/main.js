// Auto-dismiss success toasts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.alert--toast').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 400);
    }, 4000);
  });
});
// ── Notification Dropdown Toggle ──────────────────────
function toggleDropdown() {
  const dropdown = document.getElementById('notifDropdown');
  if (dropdown) dropdown.classList.toggle('open');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(e) {
  const bell = document.getElementById('notifBell');
  if (bell && !bell.contains(e.target)) {
    const dropdown = document.getElementById('notifDropdown');
    if (dropdown) dropdown.classList.remove('open');
  }
});

// ── Dismiss notification (bell + banner) ─────────────
document.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-url]');
  if (!btn) return;

  e.preventDefault();
  const url = btn.dataset.url;
  const id  = btn.dataset.id;

  fetch(url, {
    method: 'GET',
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
  .then(res => res.json())
  .then(() => {
    // Remove from dropdown
    const item = document.getElementById(`notif-${id}`);
    if (item) item.remove();

    // Remove from critical banner
    const bannerBtn = document.querySelector(
      `.critical-banner__dismiss[data-id="${id}"]`
    );
    if (bannerBtn) {
      bannerBtn.closest('.critical-banner__item')?.remove();
    }

    // Update badge count
    const badge = document.querySelector('.notif-bell__badge');
    if (badge) {
      const count = parseInt(badge.textContent) - 1;
      if (count <= 0) badge.remove();
      else badge.textContent = count;
    }

    // Remove banner if no more critical items
    const banner = document.getElementById('criticalBanner');
    if (banner && banner.querySelectorAll('.critical-banner__item').length === 0) {
      banner.remove();
    }
  });
});