let subjectCount = 0;

const DIFFICULTIES = [
  { value: 1, label: 'Easy',   color: '#4ade80' },
  { value: 2, label: 'Medium', color: '#f5a623' },
  { value: 3, label: 'Hard',   color: '#f87171' },
];

function addSubject(name = '', diff = 2, topics = '') {
  subjectCount++;
  const list = document.getElementById('subjectList');
  const div = document.createElement('div');
  div.className = 'subject-row';
  div.id = `subject-${subjectCount}`;

  div.innerHTML = `
    <div class="subject-row-inner">
      <div class="subject-num">${subjectCount}</div>
      <div class="subject-fields">
        <input
          type="text"
          name="subject_name[]"
          placeholder="Subject name (e.g. Mathematics)"
          value="${name}"
          required
          class="subject-name-input"
        />
        <div class="diff-group">
          ${DIFFICULTIES.map(d => `
            <label class="diff-btn ${d.value === diff ? 'diff-active' : ''}" style="--dc:${d.color}">
              <input type="radio" name="subject_difficulty[]" value="${d.value}" ${d.value === diff ? 'checked' : ''} onchange="setDiff(this)"/>
              ${d.label}
            </label>
          `).join('')}
        </div>
        <input
          type="text"
          name="subject_topics[]"
          placeholder="Topics / chapters (optional, comma-separated)"
          value="${topics}"
          class="subject-topics-input"
        />
      </div>
      <button type="button" class="btn-remove-subject" onclick="removeSubject(${subjectCount})" title="Remove">✕</button>
    </div>
  `;

  list.appendChild(div);
  div.querySelector('.subject-name-input').focus();
}

function removeSubject(id) {
  const el = document.getElementById(`subject-${id}`);
  if (el) {
    el.style.opacity = '0';
    el.style.transform = 'translateX(-10px)';
    setTimeout(() => el.remove(), 200);
  }
}

function setDiff(radio) {
  const group = radio.closest('.diff-group');
  group.querySelectorAll('.diff-btn').forEach(btn => btn.classList.remove('diff-active'));
  radio.closest('.diff-btn').classList.add('diff-active');
}

function updateHours(val) {
  document.getElementById('hoursVal').textContent = `${val} hrs`;
}

function updateDaysPreview() {
  const examInput = document.getElementById('exam_date');
  const preview   = document.getElementById('daysPreview');
  if (!examInput.value) return;

  const exam  = new Date(examInput.value);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const diff  = Math.ceil((exam - today) / (1000 * 60 * 60 * 24));

  if (diff <= 0) {
    preview.textContent = '⚠ Exam date must be in the future';
    preview.className = 'days-preview preview-warn';
    return;
  }

  const urgency = diff <= 7 ? 'preview-danger' : diff <= 14 ? 'preview-warn' : 'preview-ok';
  preview.className = `days-preview ${urgency}`;
  preview.innerHTML = `
    <strong>${diff} days</strong> until your exam
    &nbsp;·&nbsp; ${diff * parseFloat(document.getElementById('daily_hours').value)} total study hours available
  `;
}

document.addEventListener('DOMContentLoaded', () => {
  addSubject();
  addSubject('', 2, '');

  document.getElementById('exam_date').addEventListener('change', updateDaysPreview);
  document.getElementById('daily_hours').addEventListener('input', updateDaysPreview);

  document.getElementById('planForm').addEventListener('submit', function () {
    const subjects = document.querySelectorAll('input[name="subject_name[]"]');
    let hasSubject = false;
    subjects.forEach(s => { if (s.value.trim()) hasSubject = true; });

    if (!hasSubject) {
      alert('Please add at least one subject.');
      return false;
    }

    document.getElementById('btnText').style.display   = 'none';
    document.getElementById('btnLoader').style.display = 'inline';
    document.getElementById('submitBtn').disabled      = true;
  });
});