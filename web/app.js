/**
 * Vietnamese Text Corrector - Web Frontend JavaScript
 * Handles API calls and UI interactions
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// DOM Elements
const elements = {
    inputText: document.getElementById('input-text'),
    outputText: document.getElementById('output-text'),
    inputCount: document.getElementById('input-count'),
    outputCount: document.getElementById('output-count'),
    changesBody: document.getElementById('changes-body'),
    changesCount: document.getElementById('changes-count'),
    emptyState: document.getElementById('empty-state'),
    explanation: document.getElementById('explanation'),
    log: document.getElementById('log'),
    loading: document.getElementById('loading'),
    loadingProgress: document.getElementById('loading-progress'),
    statusDot: document.querySelector('.status-dot'),
    statusText: document.querySelector('.status-text'),
    btnProcess: document.getElementById('btn-process'),
    btnPaste: document.getElementById('btn-paste'),
    btnCopy: document.getElementById('btn-copy'),
    btnClear: document.getElementById('btn-clear'),
    btnClearLog: document.getElementById('btn-clear-log'),
    btnUpload: document.getElementById('btn-upload'),
    btnDownload: document.getElementById('btn-download'),
    btnCorrectDocx: document.getElementById('btn-correct-docx'),
    fileInput: document.getElementById('file-input'),
    modelSelect: document.getElementById('model-select'),
    pipelineSelect: document.getElementById('pipeline-select')
};

// Store results for explanation display
let resultsData = [];

// ================================================
// Utility Functions
// ================================================

function countWords(text) {
    return text.trim() ? text.trim().split(/\s+/).length : 0;
}

function updateWordCount(element, text) {
    const count = countWords(text);
    element.textContent = `${count} từ`;
}

function setStatus(status, text) {
    elements.statusDot.className = 'status-dot';
    if (status === 'processing') {
        elements.statusDot.classList.add('processing');
    } else if (status === 'error') {
        elements.statusDot.classList.add('error');
    }
    elements.statusText.textContent = text;
}

function showLoading(show, progressText = '') {
    if (show) {
        elements.loading.classList.add('active');
    } else {
        elements.loading.classList.remove('active');
    }
    elements.loadingProgress.textContent = progressText;
}

function addLog(message, type = 'normal') {
    const entry = document.createElement('div');
    entry.className = `log-entry ${type}`;
    entry.textContent = message;
    elements.log.appendChild(entry);
    elements.log.scrollTop = elements.log.scrollHeight;
}

function clearLog() {
    elements.log.innerHTML = '<div class="log-entry">🚀 Sẵn sàng sửa lỗi văn bản...</div>';
}

function setButtonsEnabled(enabled) {
    elements.btnProcess.disabled = !enabled;
    elements.btnPaste.disabled = !enabled;
    elements.btnClear.disabled = !enabled;
}

// ================================================
// API Functions
// ================================================

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        if (data.status === 'ok') {
            setStatus('ready', 'API sẵn sàng');
            addLog('✅ Kết nối API thành công', 'success');

            // Dynamically populate Ollama models
            if (data.ollama_available && data.ollama_models && data.ollama_models.length > 0) {
                populateOllamaModels(data.ollama_models);
                addLog(`🌐 Ollama: ${data.ollama_models.length} models available`, 'info');
            } else {
                addLog('⚠️ Ollama API không khả dụng', 'warning');
            }

            return true;
        }
    } catch (error) {
        setStatus('error', 'Không kết nối được API');
        addLog(`❌ Lỗi kết nối API: ${error.message}`, 'error');
        return false;
    }
}

function populateOllamaModels(models) {
    // Find or create Ollama optgroup
    let ollamaGroup = elements.modelSelect.querySelector('optgroup[label*="Ollama"]');

    if (!ollamaGroup) {
        ollamaGroup = document.createElement('optgroup');
        ollamaGroup.label = '🌐 Online (Ollama)';
        elements.modelSelect.appendChild(ollamaGroup);
    }

    // Clear existing options in the group
    ollamaGroup.innerHTML = '';

    // Add models from API
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = `ollama-${model}`;
        option.textContent = `Ollama ${model}`;
        ollamaGroup.appendChild(option);
    });
}

async function correctText(text, model = 'qwen', pipeline = 'qwen_protonx') {
    const response = await fetch(`${API_BASE_URL}/api/correct-paragraphs`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text, model, pipeline })
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

// ================================================
// UI Update Functions
// ================================================

function displayResults(data) {
    // Store results for later use
    resultsData = data.results;

    // Update output text
    elements.outputText.value = data.full_corrected;
    updateWordCount(elements.outputCount, data.full_corrected);

    // Clear and populate changes table
    elements.changesBody.innerHTML = '';

    let changesCount = 0;

    data.results.forEach((result, index) => {
        if (result.has_changes) {
            changesCount++;
            const row = document.createElement('tr');
            row.dataset.index = index;

            // Truncate long text
            const maxLen = 80;
            const originalDisplay = result.original.length > maxLen
                ? result.original.substring(0, maxLen) + '...'
                : result.original;
            const correctedDisplay = result.corrected.length > maxLen
                ? result.corrected.substring(0, maxLen) + '...'
                : result.corrected;

            row.innerHTML = `
                <td>${result.index + 1}</td>
                <td>${escapeHtml(originalDisplay)}</td>
                <td>${escapeHtml(correctedDisplay)}</td>
            `;

            row.addEventListener('click', () => showExplanation(index));

            elements.changesBody.appendChild(row);
        }
    });

    // Update changes count
    elements.changesCount.textContent = changesCount;

    // Show/hide empty state
    if (changesCount === 0) {
        elements.emptyState.classList.remove('hidden');
    } else {
        elements.emptyState.classList.add('hidden');
    }

    // Enable copy button
    elements.btnCopy.disabled = false;
}

function showExplanation(index) {
    // Remove previous selection
    document.querySelectorAll('#changes-body tr').forEach(row => {
        row.classList.remove('selected');
    });

    // Add selection to clicked row
    const clickedRow = document.querySelector(`#changes-body tr[data-index="${index}"]`);
    if (clickedRow) {
        clickedRow.classList.add('selected');
    }

    const result = resultsData[index];
    if (!result) return;

    let display = '';

    if (result.explanation) {
        display += `📝 GIẢI THÍCH:\n${result.explanation}\n\n`;
    }

    if (result.note) {
        display += `🔄 GHI CHÚ THAY ĐỔI:\n${result.note}`;
    }

    if (!display) {
        display = 'Không có giải thích cho thay đổi này.';
    }

    elements.explanation.textContent = display;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function clearAll() {
    elements.inputText.value = '';
    elements.outputText.value = '';
    elements.changesBody.innerHTML = '';
    elements.changesCount.textContent = '0';
    elements.emptyState.classList.remove('hidden');
    elements.explanation.textContent = 'Click vào một dòng trong bảng "CÁC THAY ĐỔI" để xem giải thích...';
    resultsData = [];

    updateWordCount(elements.inputCount, '');
    updateWordCount(elements.outputCount, '');

    elements.btnCopy.disabled = true;

    addLog('🗑️ Đã xóa tất cả nội dung', 'info');
}

// ================================================
// Event Handlers
// ================================================

async function handleProcess() {
    const text = elements.inputText.value.trim();

    if (!text) {
        alert('Vui lòng nhập văn bản cần sửa!');
        return;
    }

    // Get selected model and pipeline
    const selectedModel = elements.modelSelect.value;
    const selectedPipeline = elements.pipelineSelect.value;
    const modelNames = {
        'qwen-qwen2.5-7b': 'Qwen 2.5-7B',
        'qwen-qwen3-8b': 'Qwen 3-8B',
        'bartpho': 'BartPho',
        'vistral': 'Vistral 7B',
        'ollama-qwen2.5:7b': 'Ollama Qwen 2.5:7B',
        'ollama-qwen2.5:14b': 'Ollama Qwen 2.5:14B',
        'ollama-llama3.2': 'Ollama Llama 3.2',
        'ollama-gemma2': 'Ollama Gemma 2'
    };
    const pipelineNames = {
        'qwen_protonx': 'Qwen + ProtonX',
        'qwen_only': 'Qwen only',
        'protonx_only': 'ProtonX only',
        'bartpho_protonx': 'BartPho + ProtonX',
        'ollama_protonx': 'Ollama + ProtonX',
        'ollama_only': 'Ollama only'
    };
    const modelName = modelNames[selectedModel] || selectedModel;
    const pipelineName = pipelineNames[selectedPipeline] || selectedPipeline;

    setButtonsEnabled(false);
    setStatus('processing', 'Đang xử lý...');
    showLoading(true, 'Đang gửi yêu cầu đến API...');

    addLog(`📊 Bắt đầu xử lý với ${modelName} | Pipeline: ${pipelineName}`, 'info');

    try {
        const paragraphCount = text.split('\n').filter(p => p.trim()).length;
        showLoading(true, `Đang xử lý ${paragraphCount} đoạn văn với ${modelName}...`);

        const data = await correctText(text, selectedModel, selectedPipeline);

        if (data.success) {
            displayResults(data);
            setStatus('ready', 'Hoàn thành');
            addLog(`✅ Hoàn thành! Model: ${data.model_used}, Pipeline: ${data.pipeline_used}, ${data.total_paragraphs} đoạn văn`, 'success');
        } else {
            throw new Error(data.error || 'Unknown error');
        }

    } catch (error) {
        setStatus('error', 'Lỗi xử lý');
        addLog(`❌ Lỗi: ${error.message}`, 'error');
        alert(`Lỗi xử lý: ${error.message}\n\nHãy đảm bảo API đang chạy tại ${API_BASE_URL}`);
    } finally {
        setButtonsEnabled(true);
        showLoading(false);
    }
}

async function handlePaste() {
    try {
        const text = await navigator.clipboard.readText();
        elements.inputText.value = text;
        updateWordCount(elements.inputCount, text);
        addLog('📋 Đã dán văn bản từ clipboard', 'info');
    } catch (error) {
        addLog('❌ Không thể đọc clipboard', 'error');
        alert('Không thể đọc clipboard. Vui lòng dán thủ công (Ctrl+V).');
    }
}

async function handleCopy() {
    const text = elements.outputText.value;
    if (!text) {
        alert('Không có nội dung để copy!');
        return;
    }

    try {
        await navigator.clipboard.writeText(text);
        addLog('📄 Đã copy kết quả vào clipboard', 'success');

        // Visual feedback
        const originalText = elements.btnCopy.innerHTML;
        elements.btnCopy.innerHTML = '<span class="icon">✅</span> Đã copy!';
        setTimeout(() => {
            elements.btnCopy.innerHTML = originalText;
        }, 2000);
    } catch (error) {
        addLog('❌ Không thể copy vào clipboard', 'error');
    }
}

// Upload DOCX file
async function handleUpload() {
    elements.fileInput.click();
}

async function handleFileSelected(event) {
    const file = event.target.files[0];
    if (!file) return;

    if (!file.name.endsWith('.docx')) {
        alert('Chỉ hỗ trợ file .docx!');
        return;
    }

    showLoading(true, 'Đang tải file...');
    addLog(`📂 Đang tải file: ${file.name}`, 'info');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/api/upload-docx`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            elements.inputText.value = data.text;
            updateWordCount(elements.inputCount, data.text);
            addLog(`✅ Đã tải file: ${data.filename} (${data.paragraph_count} đoạn)`, 'success');
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        addLog(`❌ Lỗi tải file: ${error.message}`, 'error');
        alert(`Lỗi tải file: ${error.message}`);
    } finally {
        showLoading(false);
        // Reset file input
        elements.fileInput.value = '';
    }
}

// Download DOCX file
async function handleDownload() {
    const text = elements.outputText.value.trim();

    if (!text) {
        alert('Không có nội dung để tải!');
        return;
    }

    showLoading(true, 'Đang tạo file DOCX...');
    addLog('💾 Đang tạo file DOCX...', 'info');

    try {
        const response = await fetch(`${API_BASE_URL}/api/download-docx`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                filename: 'van_ban_da_sua.docx'
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Lỗi tải file');
        }

        // Download the file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'van_ban_da_sua.docx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        addLog('✅ Đã tải file van_ban_da_sua.docx', 'success');
    } catch (error) {
        addLog(`❌ Lỗi tải file: ${error.message}`, 'error');
        alert(`Lỗi tải file: ${error.message}`);
    } finally {
        showLoading(false);
    }
}

// Upload and correct DOCX with comments
async function handleCorrectDocx() {
    // Create a temporary file input
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.docx';

    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.docx')) {
            alert('Chỉ hỗ trợ file .docx!');
            return;
        }

        const selectedModel = elements.modelSelect.value;
        const modelNames = {
            'bartpho': 'BartPho',
            'qwen': 'Qwen',
            'vistral': 'Vistral'
        };

        showLoading(true, `Đang xử lý file ${file.name} với ${modelNames[selectedModel] || selectedModel}...`);
        addLog(`📁 Đang tải và xử lý file: ${file.name}`, 'info');
        addLog(`🤖 Model: ${modelNames[selectedModel] || selectedModel}`, 'info');

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('model', selectedModel);

            const response = await fetch(`${API_BASE_URL}/api/correct-docx`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Lỗi xử lý file');
            }

            // Download the corrected file
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = file.name.replace('.docx', '_corrected.docx');
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            addLog(`✅ Đã tải file: ${file.name.replace('.docx', '_corrected.docx')}`, 'success');
            addLog('📝 File có bao gồm phần tổng kết các thay đổi ở cuối', 'info');
        } catch (error) {
            addLog(`❌ Lỗi: ${error.message}`, 'error');
            alert(`Lỗi xử lý file: ${error.message}`);
        } finally {
            showLoading(false);
        }
    };

    input.click();
}

// ================================================
// Event Listeners
// ================================================

elements.btnProcess.addEventListener('click', handleProcess);
elements.btnPaste.addEventListener('click', handlePaste);
elements.btnCopy.addEventListener('click', handleCopy);
elements.btnClear.addEventListener('click', clearAll);
elements.btnClearLog.addEventListener('click', clearLog);
elements.btnUpload.addEventListener('click', handleUpload);
elements.btnDownload.addEventListener('click', handleDownload);
elements.btnCorrectDocx.addEventListener('click', handleCorrectDocx);
elements.fileInput.addEventListener('change', handleFileSelected);

// Word count updates
elements.inputText.addEventListener('input', () => {
    updateWordCount(elements.inputCount, elements.inputText.value);
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl+Enter to process
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        handleProcess();
    }
});

// ================================================
// Initialization
// ================================================

document.addEventListener('DOMContentLoaded', () => {
    addLog('🚀 Ứng dụng đã sẵn sàng', 'info');
    addLog('💡 Nhấn Ctrl+Enter để sửa lỗi nhanh', 'info');

    // Disable copy button initially
    elements.btnCopy.disabled = true;

    // Check API health
    checkHealth();
});
