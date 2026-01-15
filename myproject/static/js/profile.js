// Profile page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Modal management
    const modals = {
        editBioModal: document.getElementById('editBioModal'),
        addSkillModal: document.getElementById('addSkillModal'),
        addEducationModal: document.getElementById('addEducationModal'),
        addExperienceModal: document.getElementById('addExperienceModal'),
        notificationModal: document.getElementById('notificationModal')
    };

    // Open modal
    function openModal(modalId) {
        if (modals[modalId]) {
            modals[modalId].classList.add('show');
        }
    }

    // Close modal
    function closeModal(modalId) {
        if (modals[modalId]) {
            modals[modalId].classList.remove('show');
        }
    }

    // Profile picture upload
    const profilePicInput = document.getElementById('profilePicInput');
    const changePicBtn = document.getElementById('changePicBtn');
    if (changePicBtn) {
        changePicBtn.addEventListener('click', function(e) {
            e.preventDefault();
            profilePicInput.click();
        });
    }

    // Profile picture change handler
    if (profilePicInput) {
        profilePicInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    const profilePic = document.getElementById('profilePic');
                    if (profilePic && profilePic.tagName === 'IMG') {
                        profilePic.src = event.target.result;
                    }
                };
                reader.readAsDataURL(this.files[0]);
                // Here you would typically upload the file to the server
                uploadProfilePicture(this.files[0]);
            }
        });
    }

    // Upload profile picture
    function uploadProfilePicture(file) {
        const formData = new FormData();
        formData.append('profile_picture', file);
        formData.append('csrfmiddlewaretoken', window.CSRF_TOKEN);

        fetch('/accounts/api/profile/picture/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Profile picture updated successfully!', 'success');
            } else {
                showToast('Failed to update profile picture', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error updating profile picture', 'error');
        });
    }

    // Bio editing
    const editProfileBtn = document.getElementById('editProfileBtn');
    const bioForm = document.getElementById('bioForm');
    const bioInput = document.getElementById('bioInput');

    if (editProfileBtn) {
        editProfileBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const bioText = document.getElementById('bioText');
            if (bioText) {
                bioInput.value = bioText.textContent !== 'No bio yet.' ? bioText.textContent : '';
            }
            openModal('editBioModal');
        });
    }

    if (bioForm) {
        bioForm.addEventListener('submit', function(e) {
            e.preventDefault();
            updateBio(bioInput.value);
        });
    }

    // Update bio
    function updateBio(bioText) {
        fetch('/accounts/api/profile/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.CSRF_TOKEN
            },
            body: JSON.stringify({
                bio: bioText
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('bioText').textContent = bioText || 'No bio yet.';
                closeModal('editBioModal');
                showToast('Bio updated successfully!', 'success');
            } else {
                showToast('Failed to update bio', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error updating bio', 'error');
        });
    }

    // Skill management
    const addSkillBtn = document.getElementById('addSkillBtn');
    const skillForm = document.getElementById('skillForm');
    const skillInput = document.getElementById('skillInput');

    if (addSkillBtn) {
        addSkillBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openModal('addSkillModal');
        });
    }

    if (skillForm) {
        skillForm.addEventListener('submit', function(e) {
            e.preventDefault();
            addSkill(skillInput.value);
        });
    }

    // Add skill
    function addSkill(skillName) {
        fetch('/accounts/api/profile/', {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.CSRF_TOKEN
            },
            body: JSON.stringify({
                skills: [skillName]
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const skillsContainer = document.getElementById('skillsContainer');
                const skillTag = document.createElement('span');
                skillTag.className = 'skill-tag';
                skillTag.setAttribute('role', 'listitem');
                skillTag.textContent = skillName;
                skillsContainer.appendChild(skillTag);
                skillInput.value = '';
                closeModal('addSkillModal');
                showToast('Skill added successfully!', 'success');
            } else {
                showToast('Failed to add skill', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error adding skill', 'error');
        });
    }

    // Education management
    const addEducationBtn = document.getElementById('addEducationBtn');
    const educationForm = document.getElementById('educationForm');

    if (addEducationBtn) {
        addEducationBtn.addEventListener('click', function(e) {
            e.preventDefault();
            educationForm.reset();
            openModal('addEducationModal');
        });
    }

    if (educationForm) {
        educationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const institution = document.getElementById('institutionInput').value;
            const degree = document.getElementById('degreeInput').value;
            const startYear = document.getElementById('startYearInput').value;
            const endYear = document.getElementById('endYearInput').value;
            addEducation(institution, degree, startYear, endYear);
        });
    }

    // Add education
    function addEducation(institution, degree, startYear, endYear) {
        fetch('/accounts/api/profile/education/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.CSRF_TOKEN
            },
            body: JSON.stringify({
                institution: institution,
                degree: degree,
                start_year: startYear,
                end_year: endYear
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const educationList = document.getElementById('educationList');
                const article = document.createElement('article');
                article.className = 'list-item';
                article.setAttribute('role', 'listitem');
                article.innerHTML = `
                    <div class="list-item-icon" aria-hidden="true">🎓</div>
                    <div class="list-item-content">
                        <strong>${degree}</strong>
                        <p>${institution}</p>
                        <small>${startYear} - ${endYear}</small>
                    </div>
                `;
                educationList.appendChild(article);
                educationForm.reset();
                closeModal('addEducationModal');
                showToast('Education added successfully!', 'success');
            } else {
                showToast('Failed to add education', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error adding education', 'error');
        });
    }

    // Experience management
    const addExperienceBtn = document.getElementById('addExperienceBtn');
    const experienceForm = document.getElementById('experienceForm');

    if (addExperienceBtn) {
        addExperienceBtn.addEventListener('click', function(e) {
            e.preventDefault();
            experienceForm.reset();
            openModal('addExperienceModal');
        });
    }

    if (experienceForm) {
        experienceForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const company = document.getElementById('companyInput').value;
            const role = document.getElementById('roleInput').value;
            const startDate = document.getElementById('startDateInput').value;
            const endDate = document.getElementById('endDateInput').value;
            const description = document.getElementById('descriptionInput').value;
            addExperience(company, role, startDate, endDate, description);
        });
    }

    // Add experience
    function addExperience(company, role, startDate, endDate, description) {
        fetch('/accounts/api/profile/experience/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.CSRF_TOKEN
            },
            body: JSON.stringify({
                company: company,
                role: role,
                start_date: startDate || null,
                end_date: endDate || null,
                description: description
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const experienceList = document.getElementById('experienceList');
                const article = document.createElement('article');
                article.className = 'list-item';
                article.setAttribute('role', 'listitem');
                const formatDate = (dateStr) => {
                    if (!dateStr) return 'N/A';
                    const date = new Date(dateStr);
                    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
                };
                article.innerHTML = `
                    <div class="list-item-icon" aria-hidden="true">💻</div>
                    <div class="list-item-content">
                        <strong>${role}</strong>
                        <p>${company}</p>
                        <small>
                            ${formatDate(startDate)} - 
                            ${endDate ? formatDate(endDate) : 'Present'}
                        </small>
                        ${description ? `<p class="experience-description">${description}</p>` : ''}
                    </div>
                `;
                experienceList.appendChild(article);
                experienceForm.reset();
                closeModal('addExperienceModal');
                showToast('Experience added successfully!', 'success');
            } else {
                showToast('Failed to add experience', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error adding experience', 'error');
        });
    }

    // Resume upload
    const resumeForm = document.getElementById('resumeForm');
    if (resumeForm) {
        resumeForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const resumeInput = document.getElementById('resumeInput');
            if (resumeInput.files && resumeInput.files[0]) {
                uploadResume(resumeInput.files[0]);
            } else {
                showToast('Please select a file', 'error');
            }
        });
    }

    // Upload resume
    function uploadResume(file) {
        const formData = new FormData();
        formData.append('resume', file);
        formData.append('csrfmiddlewaretoken', window.CSRF_TOKEN);

        fetch('/accounts/api/profile/resume/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('resumeForm').reset();
                showToast('Resume uploaded successfully!', 'success');
                // Reload resume section if needed
                location.reload();
            } else {
                showToast('Failed to upload resume', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error uploading resume', 'error');
        });
    }

    // Job apply functionality
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-apply')) {
            const jobId = e.target.dataset.jobId;
            if (jobId) {
                applyToJob(jobId, e.target);
            }
        }
    });

    // Apply to job
    function applyToJob(jobId, button) {
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', window.CSRF_TOKEN);

        fetch(`/accounts/api/jobs/${jobId}/apply/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                button.disabled = true;
                button.textContent = '✓ Applied';
                showToast('Applied successfully!', 'success');
            } else {
                showToast(data.message || 'Failed to apply', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showToast('Error applying to job', 'error');
        });
    }

    // Modal close buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-close')) {
            const modalId = e.target.dataset.modal;
            if (modalId) {
                closeModal(modalId);
            } else if (e.target.dataset.action === 'close-notifications') {
                e.preventDefault();
                modals.notificationModal.classList.remove('show');
            }
        }
    });
    // Handle notification icon click - direct selector
    const notificationBtn = document.getElementById('notificationBtn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (modals.notificationModal) {
                modals.notificationModal.classList.add('show');
                loadNotifications();
            }
        });
    }

    // Close modal when clicking cancel button
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-secondary') && e.target.dataset.modal) {
            closeModal(e.target.dataset.modal);
        }
    });

    // Close modal when clicking outside
    Object.values(modals).forEach(modal => {
        if (modal) {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.classList.remove('show');
                }
            });
        }
    });

    // Notifications
    function loadNotifications() {
        fetch('/accounts/api/notifications/', {
            headers: {
                'X-CSRFToken': window.CSRF_TOKEN
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.items) {
                const notificationsList = document.getElementById('notificationsList');
                notificationsList.innerHTML = '';
                if (data.items.length === 0) {
                    notificationsList.innerHTML = '<p class="empty-message">No notifications.</p>';
                } else {
                    data.items.forEach(notification => {
                        const div = document.createElement('div');
                        div.className = 'notification-item' + (notification.unread ? ' unread' : '');
                        div.innerHTML = `
                            <div class="notification-title">
                                <span aria-hidden="true">📬</span>
                                ${notification.title || 'Notification'}
                            </div>
                            <div class="notification-message">${notification.message}</div>
                            <div class="notification-time">${new Date(notification.created_at).toLocaleString()}</div>
                        `;
                        notificationsList.appendChild(div);
                    });
                }
            }
        })
        .catch(error => console.error('Error loading notifications:', error));
    }

    // Toast notification
    function showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        if (!container) return;

        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.style.cssText = `
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            padding: 16px 20px;
            border-radius: 8px;
            margin-bottom: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = message;
        container.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Load notifications on page load
    loadNotifications();
    setInterval(loadNotifications, 30000); // Refresh every 30 seconds
});
