/**
 * Flask Management Systems - Client UI Controller
 * Handles sidebar toggles, confirmation modals, flash dismissal, and validation aids.
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Sidebar Toggle
  const sidebar = document.getElementById('sidebar');
  const toggleBtn = document.getElementById('sidebarToggle');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      sidebar.classList.toggle('open');
    });

    document.addEventListener('click', function (e) {
      if (sidebar.classList.contains('open') && !sidebar.contains(e.target) && e.target !== toggleBtn) {
        sidebar.classList.remove('open');
      }
    });
  }

  // 2. Alert Dismissal
  const alertCloseBtns = document.querySelectorAll('.alert-close');
  alertCloseBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const alert = btn.closest('.alert');
      if (alert) {
        alert.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        alert.style.opacity = '0';
        alert.style.transform = 'translateY(-8px)';
        setTimeout(() => alert.remove(), 300);
      }
    });
  });

  // Auto-dismiss success flash messages after 6 seconds
  const autoAlerts = document.querySelectorAll('.alert-success');
  autoAlerts.forEach(function (alert) {
    setTimeout(function () {
      if (alert && alert.parentElement) {
        alert.style.transition = 'opacity 0.5s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 500);
      }
    }, 6000);
  });

  // 3. Delete Confirmation Modal
  const deleteModal = document.getElementById('deleteConfirmModal');
  const deleteForm = document.getElementById('deleteForm');
  const deleteItemName = document.getElementById('deleteItemName');
  const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');

  const deleteTriggers = document.querySelectorAll('.btn-delete-trigger');
  deleteTriggers.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const actionUrl = btn.getAttribute('data-action');
      const itemName = btn.getAttribute('data-name') || 'this record';

      if (deleteForm && deleteItemName && deleteModal) {
        deleteForm.setAttribute('action', actionUrl);
        deleteItemName.textContent = itemName;
        deleteModal.classList.add('open');
      }
    });
  });

  if (cancelDeleteBtn && deleteModal) {
    cancelDeleteBtn.addEventListener('click', function () {
      deleteModal.classList.remove('open');
    });

    deleteModal.addEventListener('click', function (e) {
      if (e.target === deleteModal) {
        deleteModal.classList.remove('open');
      }
    });
  }

  // 4. Date Picker Min Date Enforcement
  const datePickers = document.querySelectorAll('input[type="date"][data-min-today]');
  if (datePickers.length > 0) {
    const today = new Date().toISOString().split('T')[0];
    datePickers.forEach(function (picker) {
      picker.setAttribute('min', today);
    });
  }

  // 5. Client-Side Instant Table Filter
  const clientFilterInput = document.getElementById('clientTableSearch');
  if (clientFilterInput) {
    clientFilterInput.addEventListener('input', function () {
      const term = clientFilterInput.value.toLowerCase().trim();
      const rows = document.querySelectorAll('.data-table tbody tr');
      rows.forEach(function (row) {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(term) ? '' : 'none';
      });
    });
  }
});
