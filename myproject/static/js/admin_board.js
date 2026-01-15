// Admin Board JavaScript
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrfToken = getCookie('csrftoken');
let editingJobId = null;

// ============ MODAL FUNCTIONS ============
function openJobModal(title = 'Add New Job') {
  const modal = document.getElementById('job-modal');
  const modalTitle = document.querySelector('#job-modal .modal-header h2');
  if (modalTitle) modalTitle.textContent = title;
  if (modal) {
    modal.style.display = 'flex';
    modal.classList.add('show');
  }
}

function closeJobModal() {
  const modal = document.getElementById('job-modal');
  const form = document.getElementById('job-form');
  if (modal) {
    modal.style.display = 'none';
    modal.classList.remove('show');
  }
  if (form) form.reset();
  editingJobId = null;
}

// ============ API FUNCTIONS ============
async function fetchJSON(url, opts = {}) {
  const defaultOpts = {
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    credentials: 'same-origin'
  };
  const mergedOpts = { ...defaultOpts, ...opts };
  mergedOpts.headers = { ...defaultOpts.headers, ...(opts.headers || {}) };

  const res = await fetch(url, mergedOpts);
  if (res.status === 401 || res.status === 403) {
    alert('Session expired. Log in again.');
    window.location.href = '/login/?next=' + encodeURIComponent(window.location.pathname);
    throw new Error('Auth required');
  }
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text.substring(0, 100)}`);
  }
  const contentType = res.headers.get('content-type');
  if (!contentType || !contentType.includes('application/json')) {
    const text = await res.text();
    throw new Error(`Expected JSON, got: ${contentType}`);
  }
  return res.json();
}

function updateStatsDom(data) {
  if (document.getElementById('total-jobs')) document.getElementById('total-jobs').textContent = data.totalJobs || 0;
  if (document.getElementById('active-jobs')) document.getElementById('active-jobs').textContent = data.activeJobs || 0;
  if (document.getElementById('total-applications')) document.getElementById('total-applications').textContent = data.totalApplications || 0;
  if (document.getElementById('total-users')) document.getElementById('total-users').textContent = data.totalUsers || 0;
}

async function loadStats() {
  try {
    const data = await fetchJSON('/accounts/api/stats/');
    updateStatsDom(data);
  } catch (e) {
    console.error('[STATS_ERROR]', e);
  }
}

function renderJobs(items) {
  const tbody = document.getElementById('jobs-tbody');
  if (!tbody) return;
  if (!items || items.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 2rem; color: #666;">No jobs found. Click "+ Add New Job" to create one.</td></tr>';
    return;
  }
  tbody.innerHTML = items.map(item => `
    <tr data-id="${item.id}">
      <td><strong>${item.title}</strong></td>
      <td>${item.company_name}</td>
      <td>${item.location || 'N/A'}</td>
      <td><span class="badge badge-info">${item.job_type || 'N/A'}</span></td>
      <td><span class="badge ${item.is_active ? 'badge-success' : 'badge-secondary'}">${item.is_active ? 'Active' : 'Inactive'}</span></td>
      <td>${item.applications || 0}</td>
      <td>
        <button type="button" class="btn btn-sm btn-edit" data-id="${item.id}" title="Edit Job">✏️ Edit</button>
        <button type="button" class="btn btn-sm btn-delete" data-id="${item.id}" title="Delete Job">🗑️ Delete</button>
      </td>
    </tr>
  `).join('');
}

async function loadJobs(params = {}) {
  const q = new URLSearchParams(params).toString();
  try {
    const data = await fetchJSON(`/accounts/api/jobs/?${q}`);
    renderJobs(data.items);
  } catch (e) {
    console.error('[JOBS_ERROR]', e);
    document.getElementById('jobs-tbody').innerHTML = '<tr><td colspan="7" style="text-align:center; color: red; padding: 2rem;">❌ Failed to load jobs: ' + e.message + '</td></tr>';
  }
}

// ============ CRUD OPERATIONS ============
async function editJob(id) {
  try {
    const job = await fetchJSON(`/accounts/api/jobs/${id}/`);
    editingJobId = id;
    const form = document.getElementById('job-form');
    form.querySelector('[name="title"]').value = job.title || '';
    form.querySelector('[name="company_name"]').value = job.company_name || '';
    form.querySelector('[name="location"]').value = job.location || '';
    form.querySelector('[name="job_type"]').value = job.job_type || 'Full-time';
    form.querySelector('[name="description"]').value = job.description || '';
    form.querySelector('[name="salary_min"]').value = job.salary_min || '';
    form.querySelector('[name="salary_max"]').value = job.salary_max || '';
    form.querySelector('[name="is_active"]').checked = job.is_active !== false;
    openJobModal('Edit Job');
  } catch (e) {
    console.error('[EDIT_ERROR]', e);
    alert('Failed to load job: ' + e.message);
  }
}

async function deleteJob(id) {
  if (!confirm('Delete this job? This cannot be undone.')) return;
  try {
    await fetchJSON(`/accounts/api/jobs/${id}/`, { method: 'DELETE' });
    alert('✓ Job deleted!');
    await loadStats();
    await loadJobs();
  } catch (e) {
    console.error('[DELETE_ERROR]', e);
    alert('Failed to delete: ' + e.message);
  }
}

// ============ DOM READY ============
document.addEventListener('DOMContentLoaded', () => {
  // Load data
  loadStats();
  loadJobs();

  // Add Job button
  const addJobBtn = document.getElementById('add-job-btn');
  if (addJobBtn) {
    addJobBtn.addEventListener('click', (e) => {
      e.preventDefault();
      editingJobId = null;
      const form = document.getElementById('job-form');
      if (form) form.reset();
      openJobModal('Add New Job');
    });
  }

  // Job Form
  const jobForm = document.getElementById('job-form');
  if (jobForm) {
    jobForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(jobForm);
      const payload = {
        title: formData.get('title'),
        company_name: formData.get('company_name'),
        location: formData.get('location'),
        job_type: formData.get('job_type'),
        description: formData.get('description'),
        salary_min: formData.get('salary_min') ? parseInt(formData.get('salary_min')) : null,
        salary_max: formData.get('salary_max') ? parseInt(formData.get('salary_max')) : null,
        is_active: formData.get('is_active') === 'on'
      };

      try {
        if (editingJobId) {
          await fetchJSON(`/accounts/api/jobs/${editingJobId}/`, { method: 'PUT', body: JSON.stringify(payload) });
          alert('✓ Updated!');
        } else {
          await fetchJSON('/accounts/api/jobs/', { method: 'POST', body: JSON.stringify(payload) });
          alert('✓ Created!');
        }
        closeJobModal();
        await loadStats();
        await loadJobs();
      } catch (e) {
        console.error('[FORM_ERROR]', e);
        alert('Error: ' + e.message);
      }
    });
  }

  // Search
  const searchInput = document.getElementById('search-jobs');
  if (searchInput) {
    let timeout;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        loadJobs({ q: e.target.value });
      }, 300);
    });
  }

  // Filter
  const statusFilter = document.getElementById('filter-status');
  if (statusFilter) {
    statusFilter.addEventListener('change', (e) => {
      const params = {};
      if (e.target.value === 'active') params.is_active = 'true';
      else if (e.target.value === 'inactive') params.is_active = 'false';
      loadJobs(params);
    });
  }

  // Modal backdrop close
  const modal = document.getElementById('job-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeJobModal();
      // Close button
      if (e.target.closest('[data-action="close-modal"]')) {
        closeJobModal();
      }
    });
  }

  // Edit & Delete buttons (event delegation)
  const jobsContainer = document.getElementById('jobs-table-container');
  if (jobsContainer) {
    jobsContainer.addEventListener('click', (e) => {
      // Check if clicked element or its parent is a button
      const target = e.target.closest('button');
      if (!target) return;
      
      // Edit button
      if (target.classList.contains('btn-edit')) {
        e.preventDefault();
        e.stopPropagation();
        const id = target.dataset.id;
        if (id) editJob(Number(id));
        return;
      }
      
      // Delete button
      if (target.classList.contains('btn-delete')) {
        e.preventDefault();
        e.stopPropagation();
        const id = target.dataset.id;
        if (id) deleteJob(Number(id));
        return;
      }
    });
  }

  console.log('[ADMIN_BOARD] Ready - All event listeners attached');
});
