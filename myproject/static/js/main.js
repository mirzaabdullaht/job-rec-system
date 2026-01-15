function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const csrfToken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function() {
    console.log("JobRec Application Initialized!");

    // Job filtering and search on jobs page
    const filterBtn = document.querySelector('.filter-btn');

    if (filterBtn) {
      filterBtn.addEventListener('click', applyFilters);
    }

    // Apply and Bookmark buttons on job cards
    document.addEventListener('click', async (e) => {
      const applyBtn = e.target.closest('.btn-apply');
      const bookmarkBtn = e.target.closest('.btn-bookmark');
      const unbookmarkBtn = e.target.closest('.btn-unbookmark');
      const viewDetailsBtn = e.target.closest('.view-details');

      if (applyBtn) {
        e.preventDefault();
        const id = applyBtn.dataset.jobId;
        await applyToJob(id);
      }
      if (bookmarkBtn) {
        e.preventDefault();
        const id = bookmarkBtn.dataset.jobId;
        await bookmarkJob(id);
      }
      if (unbookmarkBtn) {
        e.preventDefault();
        const id = unbookmarkBtn.dataset.jobId;
        await removeBookmark(id);
      }
      if (viewDetailsBtn) {
        e.preventDefault();
        const id = viewDetailsBtn.dataset.jobId;
        await showJobDetails(id);
      }
    });

    // Search functionality on homepage
    const searchBtn = document.querySelector('.btn-search');
    const searchBar = document.querySelector('.search-bar');
    if (searchBtn && searchBar) {
      searchBtn.addEventListener('click', () => {
        const q = searchBar.value.trim();
        if (q) {
          window.location.href = `/jobs/?keyword=${encodeURIComponent(q)}`;
        }
      });
      searchBar.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBtn.click();
      });
    }
});

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function applyFilters() {
  const keyword = document.getElementById('keyword')?.value || '';
  const location = document.getElementById('location')?.value || '';
  const jobType = document.getElementById('job-type')?.value || '';
  const salaryRange = document.getElementById('salary-range')?.value || '';

  const params = new URLSearchParams();
  if (keyword) params.append('keyword', keyword);
  if (location) params.append('location', location);
  if (jobType && jobType !== 'All') params.append('job_type', jobType);
  if (salaryRange) {
    const [min, max] = salaryRange.split('-');
    if (min) params.append('salary_min', min);
    if (max) params.append('salary_max', max);
  }

  const url = `/jobs/?${params.toString()}`;
  window.location.href = url;
}

function clearFilters() {
  const keyword = document.getElementById('keyword');
  const location = document.getElementById('location');
  const jobType = document.getElementById('job-type');
  const salaryRange = document.getElementById('salary-range');
  
  if (keyword) keyword.value = '';
  if (location) location.value = '';
  if (jobType) jobType.value = '';
  if (salaryRange) salaryRange.value = '';
  
  window.location.href = '/jobs/';
}

async function applyToJob(jobId) {
  if (!confirm('Apply to this job?')) return;
  try {
    const res = await fetch(`/accounts/api/jobs/${jobId}/apply/`, {
      method: 'POST',
      headers: { 
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    });
    
    // Check if response is JSON
    const contentType = res.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.error('Expected JSON but got:', contentType);
      if (res.status === 401 || res.status === 403) {
        alert('Please log in to apply for jobs');
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
      }
      throw new Error('Server returned non-JSON response. Please refresh and try again.');
    }
    
    const data = await res.json();
    
    if (res.ok && data.success) {
      alert('Applied successfully!');
      // Change button text to show applied status
      const buttons = document.querySelectorAll(`[data-job-id="${jobId}"].btn-apply`);
      buttons.forEach(btn => {
        btn.textContent = '✓ Applied';
        btn.disabled = true;
        btn.style.opacity = '0.7';
      });
      if (typeof updateNotificationBadge === 'function') {
        updateNotificationBadge();
      }
      location.reload();
    } else {
      alert(data.error || 'Failed to apply');
    }
  } catch (err) {
    console.error('Apply error:', err);
    alert('Error: ' + err.message);
  }
}

async function bookmarkJob(jobId) {
  try {
    const res = await fetch(`/accounts/api/jobs/${jobId}/bookmark/`, {
      method: 'POST',
      headers: { 
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    });
    
    const contentType = res.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      if (res.status === 401 || res.status === 403) {
        alert('Please log in to bookmark jobs');
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
      }
      throw new Error('Server returned non-JSON response');
    }
    
    const data = await res.json();
    if (res.ok && data.success) {
      alert('Bookmarked!');
      location.reload();
    } else {
      alert(data.error || 'Failed to bookmark');
    }
  } catch (err) {
    console.error('Bookmark error:', err);
    alert('Error: ' + err.message);
  }
}

async function removeBookmark(jobId) {
  try {
    const res = await fetch(`/accounts/api/jobs/${jobId}/bookmark/`, {
      method: 'DELETE',
      headers: { 
        'X-CSRFToken': csrfToken,
        'Content-Type': 'application/json'
      },
      credentials: 'same-origin'
    });
    
    const contentType = res.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      if (res.status === 401 || res.status === 403) {
        alert('Please log in to remove bookmarks');
        window.location.href = '/login/?next=' + window.location.pathname;
        return;
      }
      throw new Error('Server returned non-JSON response');
    }
    
    const data = await res.json();
    if (res.ok && data.success) {
      alert('Bookmark removed!');
      location.reload();
    } else {
      alert(data.error || 'Failed to remove bookmark');
    }
  } catch (err) {
    console.error(err);
    alert('Error: ' + err.message);
  }
}

async function showJobDetails(jobId) {
  try {
    const res = await fetch(`/accounts/api/jobs/${jobId}/`);
    const job = await res.json();
    
    const salary = job.salary_min && job.salary_max 
      ? `$${Number(job.salary_min).toLocaleString()} - $${Number(job.salary_max).toLocaleString()}`
      : 'Not specified';
    
    const category = job.category ? job.category.name : 'Uncategorized';
    
    const detailsHtml = `
      <div style="background: white; padding: 30px; border-radius: 16px; max-width: 700px; margin: 20px auto; box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
        <h2 style="color: #111827; margin-bottom: 10px; font-weight: 800;">${job.title}</h2>
        <h3 style="color: #6b7280; margin-bottom: 20px; font-weight: 600;">${job.company_name}</h3>
        
        <div style="display: flex; gap: 15px; margin-bottom: 20px; flex-wrap: wrap;">
          <span style="background: #ede9fe; color: #7c3aed; padding: 8px 16px; border-radius: 20px; font-weight: 700;">
            ${job.job_type}
          </span>
          <span style="background: #dbeafe; color: #1e40af; padding: 8px 16px; border-radius: 20px; font-weight: 700;">
            ${category}
          </span>
        </div>
        
        <div style="margin-bottom: 15px; color: #111827; font-weight: 600;">
          <strong>📍 Location:</strong> <span style="color: #6b7280;">${job.location}</span>
        </div>
        
        <div style="margin-bottom: 15px; color: #111827; font-weight: 600;">
          <strong>💰 Salary:</strong> <span style="color: #059669;">${salary}</span>
        </div>
        
        <div style="margin-bottom: 15px; color: #111827; font-weight: 600;">
          <strong>📅 Posted:</strong> <span style="color: #6b7280;">${new Date(job.posted_date).toLocaleDateString()}</span>
        </div>
        
        <div style="margin: 20px 0;">
          <h4 style="color: #111827; margin-bottom: 10px; font-weight: 700;">Description</h4>
          <p style="color: #5a6370; line-height: 1.7; background: #f9fafb; padding: 15px; border-radius: 8px;">${job.description}</p>
        </div>
        
        ${job.requirements ? `
          <div style="margin: 20px 0;">
            <h4 style="color: #111827; margin-bottom: 10px; font-weight: 700;">Requirements</h4>
            <p style="color: #5a6370; line-height: 1.7; background: #f9fafb; padding: 15px; border-radius: 8px;">${job.requirements}</p>
          </div>
        ` : ''}
        
        <div style="margin-top: 25px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
          <button onclick="applyToJob(${job.id})" style="background: #7c3aed; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 700;">
            Apply Now
          </button>
          <button onclick="bookmarkJob(${job.id})" style="background: #e5e7eb; color: #111827; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 700;">
            Bookmark
          </button>
          <button onclick="closeJobDetails()" style="background: #f3f4f6; color: #111827; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 700;">
            Close
          </button>
        </div>
      </div>
    `;
    
    const overlay = document.createElement('div');
    overlay.id = 'job-detail-modal';
    overlay.style.cssText = 'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 9999; overflow-y: auto; padding: 20px;';
    overlay.innerHTML = detailsHtml;
    overlay.onclick = (e) => { if (e.target === overlay) closeJobDetails(); };
    document.body.appendChild(overlay);
  } catch (err) {
    console.error(err);
    alert('Failed to load job details');
  }
}

function closeJobDetails() {
  const modal = document.getElementById('job-detail-modal');
  if (modal) modal.remove();
}

// ============== PROFILE PICTURE UPLOAD ==============
function initProfilePictureUpload() {
  const profilePic = document.getElementById('profilePic');
  const changePicBtn = document.getElementById('changePicBtn');
  const profilePicInput = document.getElementById('profilePicInput');

  if (profilePic) {
    profilePic.addEventListener('click', () => {
      profilePicInput.click();
    });
  }

  if (changePicBtn) {
    changePicBtn.addEventListener('click', () => {
      profilePicInput.click();
    });
  }

  if (profilePicInput) {
    profilePicInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append('profile_picture', file);

      try {
        const res = await fetch('/accounts/api/profile/picture/', {
          method: 'POST',
          headers: { 'X-CSRFToken': csrfToken },
          body: formData,
        });
        const data = await res.json();
        if (data.success) {
          alert('Profile picture updated successfully!');
          location.reload();
        } else {
          alert(data.error || 'Failed to upload picture');
        }
      } catch (err) {
        console.error(err);
        alert('Error uploading picture: ' + err.message);
      }
    });
  }
}

// ============== NOTIFICATION MODAL ==============
function openNotificationModal() {
  const modal = document.getElementById('notificationModal');
  if (!modal) {
    console.error('Notification modal not found!');
    return;
  }
  
  modal.classList.add('show');
  const notifList = document.getElementById('notificationsList');
  if (!notifList) {
    console.error('Notifications list not found!');
    return;
  }
  
  notifList.innerHTML = '<p class="empty-message">Loading notifications...</p>';
  
  console.log('Opening notifications modal...');
  console.log('CSRF Token:', csrfToken);
  
  // Fetch and display notifications from database
  fetch('/accounts/api/notifications/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    credentials: 'same-origin'
  })
    .then(async (r) => {
      console.log('Response status:', r.status);
      if (r.status === 401) {
        notifList.innerHTML = '<p class="empty-message">🔒 Please log in to view notifications.</p>';
        throw new Error('Auth required');
      }
      if (!r.ok) {
        let errBody = {};
        try { errBody = await r.json(); } catch (e) {}
        throw new Error(`HTTP ${r.status}: ${JSON.stringify(errBody)}`);
      }
      return r.json();
    })
    .then(data => {
      console.log('API Response:', data);
      const notifs = data.items || [];
      
      if (notifs.length === 0) {
        notifList.innerHTML = '<p class="empty-message">📭 No notifications yet. When you apply or bookmark jobs, you\'ll see notifications here!</p>';
        return;
      }
      
      let html = '';
      notifs.forEach(notif => {
        const isUnread = !notif.read;
        const createdDate = new Date(notif.created_at);
        
        // Format time: show time if today, date if older
        let timeStr = '';
        const today = new Date();
        const isToday = createdDate.toDateString() === today.toDateString();
        
        if (isToday) {
          timeStr = createdDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        } else {
          timeStr = createdDate.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: createdDate.getFullYear() !== today.getFullYear() ? 'numeric' : undefined });
        }
        
        html += `
          <div class="notification-item ${isUnread ? 'unread' : ''}">
            <div class="notification-title">
              <span>${isUnread ? '🔔' : '✓'}</span> ${escapeHtml(notif.message)}
            </div>
            <div class="notification-time">${timeStr}</div>
          </div>
        `;
      });
      notifList.innerHTML = html;
      
      // Mark all unread notifications as read
      const unreadIds = notifs.filter(n => !n.read).map(n => n.id);
      if (unreadIds.length > 0) {
        fetch('/accounts/api/notifications/mark-read/', {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken 
          },
          credentials: 'same-origin',
          body: JSON.stringify({ ids: unreadIds })
        }).then(r => r.json())
          .then(data => {
            console.log('Mark read response:', data);
            if (data.success) {
              updateNotificationBadge();
            }
          })
          .catch(err => console.error('Error marking notifications as read:', err));
      }
    })
    .catch(err => {
      console.error('Error loading notifications:', err);
      if (notifList) {
        notifList.innerHTML = `<p class="empty-message">❌ ${escapeHtml(err.message || 'Failed to load notifications')}</p>`;
      }
    });
}

function closeNotificationModal() {
  const modal = document.getElementById('notificationModal');
  if (modal) modal.classList.remove('show');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
  const modal = document.getElementById('notificationModal');
  if (modal && e.target === modal) {
    closeNotificationModal();
  }
  
  // Handle data-action attributes
  const actionElement = e.target.closest('[data-action]');
  if (actionElement) {
    const action = actionElement.dataset.action;
    
    switch(action) {
      case 'open-notifications':
        e.preventDefault();
        openNotificationModal();
        break;
      case 'close-notifications':
        e.preventDefault();
        closeNotificationModal();
        break;
      case 'clear-filters':
        e.preventDefault();
        clearFilters();
        break;
    }
  }
});

// ============== NOTIFICATION BADGE ==============
function updateNotificationBadge() {
  fetch('/accounts/api/notifications/', { credentials: 'same-origin' })
    .then(async (r) => {
      if (r.status === 401) {
        return { items: [] }; // not logged in, hide badge
      }
      if (!r.ok) {
        const body = await r.text();
        throw new Error(`HTTP ${r.status}: ${body.substring(0, 120)}`);
      }
      return r.json();
    })
    .then(data => {
      const unreadCount = data.items ? data.items.filter(n => !n.read).length : 0;
      const badge = document.getElementById('notif-badge');
      if (badge) {
        if (unreadCount > 0) {
          badge.textContent = unreadCount;
          badge.style.display = 'flex';
        } else {
          badge.style.display = 'none';
        }
      }
    })
    .catch(err => console.log('Notification update skipped:', err));
}

// ============== PROFILE STATS UPDATE ==============
function updateProfileStats() {
  const appCount = document.getElementById('app-count');
  const bookmarkCount = document.getElementById('bookmark-count');

  if (appCount) {
    fetch('/accounts/api/applications/')
      .then(r => r.json())
      .then(data => {
        appCount.textContent = data.items ? data.items.length : 0;
      })
      .catch(err => console.log('App count update skipped:', err));
  }

  if (bookmarkCount) {
    fetch('/accounts/api/bookmarks/')
      .then(r => r.json())
      .then(data => {
        bookmarkCount.textContent = data.items ? data.items.length : 0;
      })
      .catch(err => console.log('Bookmark count update skipped:', err));
  }
}

// Initialize profile features on page load
document.addEventListener('DOMContentLoaded', function() {
  initProfilePictureUpload();
  updateNotificationBadge();
  updateProfileStats();
  
  // Update notification badge every 30 seconds
  setInterval(updateNotificationBadge, 30000);
  
  // Handle notification icon click on all pages
  const notificationBtn = document.getElementById('notificationBtn') || document.querySelector('[data-action="open-notifications"]');
  if (notificationBtn) {
    notificationBtn.addEventListener('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      openNotificationModal();
    });
  }
  
  // Close notification modal
  document.addEventListener('click', function(e) {
    if (e.target.dataset.action === 'close-notifications') {
      e.preventDefault();
      closeNotificationModal();
    }
  });
});
