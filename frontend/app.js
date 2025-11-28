/**
 * MetaScan Frontend - Vanilla JavaScript
 * Image forensics metadata inspector
 */

// State management
let currentMetadata = null;
let currentFileName = null;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const uploadSection = document.getElementById('uploadSection');
const resultsSection = document.getElementById('resultsSection');
const errorMessage = document.getElementById('errorMessage');
const spinner = document.getElementById('spinner');
const loadingText = document.getElementById('loadingText');
const newFileBtn = document.getElementById('newFileBtn');
const exportJsonBtn = document.getElementById('exportJsonBtn');
const downloadThumbBtn = document.getElementById('downloadThumbBtn');
const copyJsonBtn = document.getElementById('copyJsonBtn');
const tabButtons = document.querySelectorAll('.tab');
const tabPanes = document.querySelectorAll('.tab-pane');

// ============================================================================
// Event Listeners
// ============================================================================

browseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
        const file = e.target.files[0];
        if (file.type.startsWith('image/')) {
            handleFileUpload(file);
        } else {
            showError('Please select an image file');
        }
    }
});

// Drag and drop
dropzone.addEventListener('dragenter', (e) => {
    e.preventDefault();
    dropzone.classList.add('active');
});

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('active');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('active');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('active');

    const files = e.dataTransfer.files;
    if (files && files[0]) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            handleFileUpload(file);
        } else {
            showError('Please drop an image file');
        }
    }
});

// Tab switching
tabButtons.forEach((button) => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        switchTab(tabName);
    });
});

newFileBtn.addEventListener('click', () => {
    resetUploadForm();
});

exportJsonBtn.addEventListener('click', () => {
    exportJSON();
});

downloadThumbBtn.addEventListener('click', () => {
    downloadThumbnail();
});

copyJsonBtn.addEventListener('click', () => {
    copyJSON();
});

// ============================================================================
// File Upload and Analysis
// ============================================================================

async function handleFileUpload(file) {
    clearError();
    showLoading(true);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('http://localhost:8000/api/inspect', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze image');
        }

        const data = await response.json();

        if (data.success) {
            currentMetadata = data.data;
            currentFileName = file.name;
            displayResults();
        } else {
            throw new Error(data.error || 'Analysis failed');
        }
    } catch (err) {
        showError(err.message);
        console.error('Error:', err);
    } finally {
        showLoading(false);
    }
}

// ============================================================================
// Display Results
// ============================================================================

function displayResults() {
    uploadSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');

    // Display file info
    const fileInfo = currentMetadata.file_info;
    document.getElementById('fileName').textContent = escapeHtml(currentFileName);
    
    let infoText = `${fileInfo.format} • ${formatFileSize(fileInfo.size_bytes)}`;
    if (fileInfo.width && fileInfo.height) {
        infoText += ` • ${fileInfo.width}×${fileInfo.height}px`;
    }
    document.getElementById('fileInfo').textContent = infoText;

    // Display thumbnail
    if (currentMetadata.thumbnail_base64) {
        const thumb = document.getElementById('thumbnailPreview');
        thumb.src = `data:image/jpeg;base64,${currentMetadata.thumbnail_base64}`;
        thumb.classList.remove('hidden');
        downloadThumbBtn.classList.remove('hidden');
    }

    // Display anomalies
    if (currentMetadata.anomalies && currentMetadata.anomalies.length > 0) {
        const anomaliesSection = document.getElementById('anomaliesSection');
        const anomaliesList = document.getElementById('anomaliesList');
        anomaliesList.innerHTML = currentMetadata.anomalies
            .map((anomaly) => `<li>${escapeHtml(anomaly)}</li>`)
            .join('');
        anomaliesSection.classList.remove('hidden');
    }

    // Populate tabs
    populateOverviewTab();
    populateExifTab();
    populateHashesTab();
    populateJsonTab();

    // Reset to overview tab
    switchTab('overview');
}

function populateOverviewTab() {
    const fileInfo = currentMetadata.file_info;
    const exif = currentMetadata.exif;
    const gps = currentMetadata.gps;

    const rows = [
        ['Filename', escapeHtml(currentFileName)],
        ['File Size', formatFileSize(fileInfo.size_bytes)],
        ['MIME Type', fileInfo.mime],
        ['Image Format', fileInfo.format],
    ];

    if (fileInfo.width && fileInfo.height) {
        rows.push(['Dimensions', `${fileInfo.width} × ${fileInfo.height} pixels`]);
    }

    if (exif.datetime_original) {
        rows.push(['Capture DateTime', escapeHtml(exif.datetime_original)]);
    }

    if (exif.make || exif.model) {
        const camera = (exif.make ? escapeHtml(exif.make) : '') +
            (exif.model ? ` ${escapeHtml(exif.model)}` : '');
        rows.push(['Camera', camera]);
    }

    if (gps && (gps.lat || gps.lon)) {
        rows.push(['GPS Coordinates', `${gps.lat?.toFixed(4)}, ${gps.lon?.toFixed(4)}`]);
    }

    const tbody = document.getElementById('overviewTable');
    tbody.innerHTML = rows
        .map((row) => `<tr><td class="label">${row[0]}</td><td>${row[1]}</td></tr>`)
        .join('');
}

function populateExifTab() {
    const exif = currentMetadata.exif;
    const gps = currentMetadata.gps;

    const rows = [];

    if (exif.datetime_original) {
        rows.push(['DateTime Original', escapeHtml(exif.datetime_original)]);
    }
    if (exif.make) {
        rows.push(['Camera Make', escapeHtml(exif.make)]);
    }
    if (exif.model) {
        rows.push(['Camera Model', escapeHtml(exif.model)]);
    }
    if (exif.iso) {
        rows.push(['ISO', escapeHtml(String(exif.iso))]);
    }
    if (exif.f_number) {
        rows.push(['F-Number', escapeHtml(exif.f_number)]);
    }
    if (exif.exposure) {
        rows.push(['Exposure', escapeHtml(exif.exposure)]);
    }
    if (exif.focal_length) {
        rows.push(['Focal Length', escapeHtml(exif.focal_length)]);
    }
    if (exif.software) {
        rows.push(['Software', escapeHtml(exif.software)]);
    }

    if (rows.length === 0) {
        document.getElementById('exifTable').innerHTML = '<tr><td colspan="2" class="no-data">No EXIF data found</td></tr>';
    } else {
        const tbody = document.getElementById('exifTable');
        tbody.innerHTML = rows
            .map((row) => `<tr><td class="label">${row[0]}</td><td>${row[1]}</td></tr>`)
            .join('');
    }

    // GPS section
    if (gps && (gps.lat || gps.lon)) {
        const gpsRows = [];
        if (gps.lat) gpsRows.push(['Latitude', gps.lat.toFixed(6)]);
        if (gps.lon) gpsRows.push(['Longitude', gps.lon.toFixed(6)]);
        if (gps.alt) gpsRows.push(['Altitude', `${gps.alt.toFixed(2)} m`]);

        const gpsTable = document.getElementById('gpsTable');
        gpsTable.innerHTML = gpsRows
            .map((row) => `<tr><td class="label">${row[0]}</td><td>${row[1]}</td></tr>`)
            .join('');
        document.getElementById('gpsSection').classList.remove('hidden');
    }

    // Other EXIF tags
    if (exif.other_tags && Object.keys(exif.other_tags).length > 0) {
        const otherRows = Object.entries(exif.other_tags)
            .map((entry) => [escapeHtml(entry[0]), escapeHtml(String(entry[1]).substring(0, 100))])
            .sort();

        const otherTable = document.getElementById('otherExifTable');
        otherTable.innerHTML = otherRows
            .map((row) => `<tr><td class="label">${row[0]}</td><td>${row[1]}</td></tr>`)
            .join('');
        document.getElementById('otherExifSection').classList.remove('hidden');
    }
}

function populateHashesTab() {
    const rows = Object.entries(currentMetadata.hashes)
        .map((entry) => [entry[0].toUpperCase(), entry[1]]);

    const tbody = document.getElementById('hashesTable');
    tbody.innerHTML = rows
        .map((row) => `<tr><td class="label">${row[0]}</td><td class="hash-value">${row[1]}</td></tr>`)
        .join('');

    // Entropy
    const entropy = currentMetadata.entropy;
    document.getElementById('entropyValue').textContent = entropy.toFixed(4);
    const entropyBar = document.getElementById('entropyBar');
    entropyBar.style.width = `${(entropy / 8) * 100}%`;

    // LSB Variance
    document.getElementById('lsbValue').textContent = currentMetadata.lsb_variance.toFixed(4);
}

function populateJsonTab() {
    const jsonString = JSON.stringify(currentMetadata, null, 2);
    document.getElementById('jsonContent').textContent = jsonString;
}

// ============================================================================
// Tab Management
// ============================================================================

function switchTab(tabName) {
    // Update active tab button
    tabButtons.forEach((btn) => {
        if (btn.getAttribute('data-tab') === tabName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Update active tab pane
    tabPanes.forEach((pane) => {
        if (pane.id === `tab-${tabName}`) {
            pane.classList.add('active');
        } else {
            pane.classList.remove('active');
        }
    });
}

// ============================================================================
// Actions
// ============================================================================

function exportJSON() {
    const dataStr = JSON.stringify(currentMetadata, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${currentFileName.replace(/\.[^/.]+$/, '')}_metadata.json`;
    link.click();
    URL.revokeObjectURL(url);
}

function downloadThumbnail() {
    if (!currentMetadata.thumbnail_base64) {
        alert('No thumbnail available');
        return;
    }
    const link = document.createElement('a');
    link.href = `data:image/jpeg;base64,${currentMetadata.thumbnail_base64}`;
    link.download = `${currentFileName.replace(/\.[^/.]+$/, '')}_thumb.jpg`;
    link.click();
}

function copyJSON() {
    const jsonString = JSON.stringify(currentMetadata, null, 2);
    navigator.clipboard.writeText(jsonString).then(() => {
        const btn = copyJsonBtn;
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        setTimeout(() => {
            btn.textContent = originalText;
        }, 2000);
    });
}

function resetUploadForm() {
    currentMetadata = null;
    currentFileName = null;
    fileInput.value = '';
    uploadSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
    clearError();
}

// ============================================================================
// Utility Functions
// ============================================================================

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
}

function clearError() {
    errorMessage.textContent = '';
    errorMessage.classList.add('hidden');
}

function showLoading(show) {
    if (show) {
        dropzone.classList.add('loading');
        spinner.classList.remove('hidden');
        loadingText.classList.remove('hidden');
    } else {
        dropzone.classList.remove('loading');
        spinner.classList.add('hidden');
        loadingText.classList.add('hidden');
    }
}

function formatFileSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i];
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, (m) => map[m]);
}
