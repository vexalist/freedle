// freedle.js - All logic for static front-end-only Freedle

// --- Utility Functions ---
function generatePollId() {
    return Math.random().toString(36).substr(2, 8);
}
function getPollIdFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}
function getPollKey(id) {
    return 'poll_' + id;
}
function savePoll(poll) {
    localStorage.setItem(getPollKey(poll.id), JSON.stringify(poll));
}
function loadPoll(id) {
    const data = localStorage.getItem(getPollKey(id));
    return data ? JSON.parse(data) : null;
}

// --- Poll Creation (index.html) ---
if (document.getElementById('create-form')) {
    // Calendar logic (reuse your existing JS or keep simple for now)
    const maxSelections = 10;
    const selectedDates = new Set();
    const messageDiv = document.getElementById('calendar-message');
    const doneBtn = document.getElementById('done-btn');
    const monthLabel = document.getElementById('calendar-month-label');
    const calendarBody = document.getElementById('calendar-body');
    const prevBtn = document.getElementById('prev-month');
    const nextBtn = document.getElementById('next-month');
    const form = document.getElementById('create-form');
    const eventTitleInput = document.getElementById('event-title');
    const pollLinkSection = document.getElementById('poll-link-section');
    const pollLinkInput = document.getElementById('poll-link');
    const copyLinkBtn = document.getElementById('copy-link-btn');

    // Date boundaries
    const today = new Date();
    today.setHours(0,0,0,0);
    const startYear = today.getFullYear();
    const startMonth = today.getMonth();
    const endDate = new Date(today);
    endDate.setMonth(endDate.getMonth() + 6);
    endDate.setDate(0); // Last day of the 6th month
    const endYear = endDate.getFullYear();
    const endMonth = endDate.getMonth();

    // Build months array from today to 6 months ahead
    const months = [];
    let y = startYear, m = startMonth;
    while (y < endYear || (y === endYear && m <= endMonth)) {
        months.push({
            name: new Date(y, m).toLocaleString('default', { month: 'long' }),
            year: y,
            month: m
        });
        m++;
        if (m > 11) { m = 0; y++; }
    }
    let currentMonthIdx = 0; // Start at current month

    function pad(n) { return n < 10 ? '0' + n : n; }

    function renderCalendar() {
        const { name, year, month } = months[currentMonthIdx];
        monthLabel.textContent = `${name} ${year}`;
        prevBtn.disabled = currentMonthIdx === 0;
        nextBtn.disabled = currentMonthIdx === months.length - 1;
        const firstDay = new Date(year, month, 1);
        let startDay = firstDay.getDay();
        startDay = startDay === 0 ? 6 : startDay - 1; // Make Monday=0
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        let html = '';
        let day = 1;
        for (let row = 0; row < 6; row++) {
            html += '<tr>';
            for (let col = 0; col < 7; col++) {
                if (row === 0 && col < startDay) {
                    html += '<td></td>';
                } else if (day > daysInMonth) {
                    html += '<td></td>';
                } else {
                    const dateObj = new Date(year, month, day);
                    dateObj.setHours(0,0,0,0);
                    const dateStr = `${year}-${pad(month + 1)}-${pad(day)}`;
                    let cellClass = '';
                    let disabled = false;
                    if (dateObj < today) {
                        cellClass = 'disabled';
                        disabled = true;
                    }
                    if (selectedDates.has(dateStr)) cellClass += ' selected';
                    html += `<td data-date="${dateStr}" class="${cellClass.trim()}"${disabled ? ' tabindex="-1"' : ''}>${day}</td>`;
                    day++;
                }
            }
            html += '</tr>';
            if (day > daysInMonth) break;
        }
        calendarBody.innerHTML = html;
        document.querySelectorAll('.calendar-table td[data-date]').forEach(cell => {
            if (cell.classList.contains('disabled')) return;
            cell.addEventListener('click', function() {
                const date = this.getAttribute('data-date');
                if (this.classList.contains('selected')) {
                    this.classList.remove('selected');
                    selectedDates.delete(date);
                    messageDiv.textContent = '';
                } else {
                    if (selectedDates.size >= maxSelections) {
                        messageDiv.textContent = `You can select up to ${maxSelections} dates.`;
                        return;
                    }
                    this.classList.add('selected');
                    selectedDates.add(date);
                    messageDiv.textContent = '';
                }
                doneBtn.disabled = selectedDates.size === 0;
            });
        });
    }
    prevBtn.addEventListener('click', () => {
        if (currentMonthIdx > 0) {
            currentMonthIdx--;
            renderCalendar();
        }
    });
    nextBtn.addEventListener('click', () => {
        if (currentMonthIdx < months.length - 1) {
            currentMonthIdx++;
            renderCalendar();
        }
    });
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        const title = eventTitleInput.value.trim();
        if (!title || selectedDates.size === 0) {
            messageDiv.textContent = 'Please enter an event name and select at least one date.';
            return;
        }
        // Create poll
        const pollId = generatePollId();
        const poll = {
            id: pollId,
            title: title,
            dates: Array.from(selectedDates),
            responses: []
        };
        savePoll(poll);
        // Show poll link
        const pollUrl = `${window.location.origin}/poll.html?id=${pollId}`;
        pollLinkInput.value = pollUrl;
        pollLinkSection.style.display = '';
        copyLinkBtn.onclick = function() {
            pollLinkInput.select();
            document.execCommand('copy');
            this.textContent = 'copied!';
            setTimeout(() => { this.textContent = 'copy'; }, 1200);
        };
    });
    renderCalendar();
}

// --- Poll Response (poll.html) ---
if (document.getElementById('response-form')) {
    const pollId = getPollIdFromUrl();
    const poll = loadPoll(pollId);
    const pollTitle = document.getElementById('poll-title');
    const dateOptionsDiv = document.getElementById('date-options');
    const responseForm = document.getElementById('response-form');
    const responseMessage = document.getElementById('response-message');
    const resultsLinkSection = document.getElementById('results-link-section');
    const resultsLinkInput = document.getElementById('results-link');
    const copyResultsBtn = document.getElementById('copy-results-btn');
    if (!poll) {
        pollTitle.textContent = 'Poll not found.';
        responseForm.style.display = 'none';
    } else {
        pollTitle.textContent = poll.title;
        // Render date options
        dateOptionsDiv.innerHTML = '';
        poll.dates.forEach((date, idx) => {
            const id = `date-${idx}`;
            const row = document.createElement('div');
            row.className = 'date-option-row';
            row.innerHTML = `<input type="checkbox" id="${id}" name="dates" value="${date}"><label for="${id}">${formatDateOption(date)}</label>`;
            dateOptionsDiv.appendChild(row);
        });
        responseForm.onsubmit = function(e) {
            e.preventDefault();
            const name = document.getElementById('name').value.trim();
            const selectedDates = Array.from(document.querySelectorAll('input[name="dates"]:checked')).map(cb => cb.value);
            if (!name) {
                responseMessage.textContent = 'Name is required.';
                return;
            }
            if (selectedDates.length === 0) {
                responseMessage.textContent = 'Please select at least one date.';
                return;
            }
            if (poll.responses.some(r => r.name === name)) {
                responseMessage.textContent = 'Someone has already submitted with that name.';
                return;
            }
            poll.responses.push({ name, selectedDates });
            savePoll(poll);
            responseMessage.textContent = '';
            // Show results link
            const resultsUrl = `${window.location.origin}/results.html?id=${pollId}`;
            resultsLinkInput.value = resultsUrl;
            resultsLinkSection.style.display = '';
            copyResultsBtn.onclick = function() {
                resultsLinkInput.select();
                document.execCommand('copy');
                this.textContent = 'copied!';
                setTimeout(() => { this.textContent = 'copy'; }, 1200);
            };
        };
    }
}

// --- Results Page (results.html) ---
if (document.getElementById('results-grid')) {
    const pollId = getPollIdFromUrl();
    const poll = loadPoll(pollId);
    const resultsTitle = document.getElementById('results-title');
    const resultsGrid = document.getElementById('results-grid');
    const resultsUrlInput = document.getElementById('results-url');
    const copyResultsUrlBtn = document.getElementById('copy-results-url-btn');
    if (!poll) {
        resultsTitle.textContent = 'Poll not found.';
        resultsGrid.innerHTML = '';
    } else {
        resultsTitle.textContent = poll.title;
        resultsUrlInput.value = window.location.href;
        copyResultsUrlBtn.onclick = function() {
            resultsUrlInput.select();
            document.execCommand('copy');
            this.textContent = 'copied!';
            setTimeout(() => { this.textContent = 'copy'; }, 1200);
        };
        // Build results grid
        const participants = poll.responses.map(r => r.name);
        const dateLabels = poll.dates.map(formatDateOption);
        let html = '<table style="width: 100%; border-collapse: separate; border-spacing: 0 8px; margin-bottom: 32px;">';
        html += '<thead><tr><th style="text-align: left; font-size: 1.1rem; font-weight: 700; color: #fff;"></th>';
        participants.forEach(participant => {
            html += `<th style="padding: 0 8px; height: 60px; vertical-align: bottom;"><div style="writing-mode: vertical-rl; transform: rotate(180deg); font-size: 1.1rem; font-weight: 700; color: #fff; letter-spacing: 1px;">${participant}</div></th>`;
        });
        html += '</tr></thead><tbody>';
        poll.dates.forEach((date, dateIdx) => {
            html += `<tr><td style="font-size: 1.1rem; font-weight: 600; color: #ffd97b; padding-right: 12px;">${dateLabels[dateIdx]}</td>`;
            participants.forEach((participant, partIdx) => {
                const r = poll.responses[partIdx];
                const selected = r.selectedDates.includes(date);
                html += `<td style="text-align: center;">${selected ? '<span style=\'color: #ffd97b; font-size: 2rem;\'>&#10003;</span>' : '<span style=\'color: #8d8d8d; font-size: 2rem;\'>&#10007;</span>'}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody></table>';
        resultsGrid.innerHTML = html;
    }
}

// --- Helper: Format date option ---
function formatDateOption(dateStr) {
    try {
        const dt = new Date(dateStr);
        return dt.toLocaleDateString(undefined, { weekday: 'short', day: 'numeric', month: 'short' });
    } catch {
        return dateStr;
    }
} 