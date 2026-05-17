const STORAGE_KEY = 'soe-rosa-romita-state-v1';

const seedState = {
  currentUserId: null,
  users: [
    { id: 'u-rep-7a', name: 'Ana Clara Representante', email: 'representante@rosaromita.edu.br', password: '123456', role: 'representante', classes: ['7A'], studentIds: [] },
    { id: 'u-resp-joao', name: 'Mariana Santos', email: 'responsavel@rosaromita.edu.br', password: '123456', role: 'responsavel', classes: [], studentIds: ['a-joao', 'a-luiza'] },
    { id: 'u-prof-mat', name: 'Prof. Ricardo Almeida', email: 'professor@rosaromita.edu.br', password: '123456', role: 'professor', classes: ['7A', '8B'], subjects: ['Matemática'] },
    { id: 'u-coord', name: 'Coordenação SOE', email: 'coordenacao@rosaromita.edu.br', password: '123456', role: 'coordenador', classes: ['7A', '8B', '9C'], studentIds: [] }
  ],
  students: [
    { id: 'a-joao', name: 'João Santos', className: '7A', guardianName: 'Mariana Santos', guardianEmail: 'responsavel@rosaromita.edu.br', guardianPhone: '11988887777' },
    { id: 'a-luiza', name: 'Luiza Santos', className: '8B', guardianName: 'Mariana Santos', guardianEmail: 'responsavel@rosaromita.edu.br', guardianPhone: '11988887777' },
    { id: 'a-pedro', name: 'Pedro Lima', className: '7A', guardianName: 'Carlos Lima', guardianEmail: 'carlos.lima@email.com', guardianPhone: '11977776666' },
    { id: 'a-bia', name: 'Beatriz Souza', className: '7A', guardianName: 'Renata Souza', guardianEmail: 'renata.souza@email.com', guardianPhone: '11966665555' }
  ],
  routines: [
    { id: 'r-1', date: today(), className: '7A', createdBy: 'u-rep-7a', lessonContent: 'Ciências: ecossistemas. História: Brasil Colônia.', homework: 'Responder exercícios 1 a 5 no caderno.', dailyReading: 'Leitura coletiva do conto A Cartomante.', attendance: { 'a-joao': 'Presente', 'a-pedro': 'Ausente', 'a-bia': 'Presente' } }
  ],
  documents: [
    { id: 'd-1', studentId: 'a-pedro', date: today(), type: 'Justificativa de falta', note: 'Consulta odontológica agendada previamente.', fileName: 'justificativa-pedro.pdf', uploadedBy: 'Carlos Lima', uploadedAt: new Date().toISOString() }
  ],
  deliveries: [
    { id: 'e-1', studentId: 'a-joao', title: 'Lista de frações', status: 'Entregue', date: today(), teacherId: 'u-prof-mat' }
  ]
};

let state = loadState();
let currentView = 'dashboard';

const roleLabels = {
  representante: 'Aluno representante',
  responsavel: 'Responsável do aluno',
  professor: 'Professor',
  coordenador: 'Coordenador SOE'
};

const roleAccess = {
  representante: ['dashboard', 'rotina', 'privacidade'],
  responsavel: ['dashboard', 'responsavel', 'privacidade'],
  professor: ['dashboard', 'professor', 'privacidade'],
  coordenador: ['dashboard', 'rotina', 'responsavel', 'professor', 'coordenacao', 'importacao', 'privacidade']
};

const qs = selector => document.querySelector(selector);
const qsa = selector => [...document.querySelectorAll(selector)];

function today() {
  return new Date().toISOString().slice(0, 10);
}

function loadState() {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (!stored) return structuredClone(seedState);
  try {
    return { ...structuredClone(seedState), ...JSON.parse(stored) };
  } catch {
    return structuredClone(seedState);
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function currentUser() {
  return state.users.find(user => user.id === state.currentUserId) || null;
}

function showToast(message) {
  const toast = qs('#toast');
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3200);
}

function normalizePhone(phone = '') {
  return phone.replace(/\D/g, '');
}

function formatDate(dateText) {
  if (!dateText) return '-';
  return new Date(`${dateText}T12:00:00`).toLocaleDateString('pt-BR');
}

function canAccess(view) {
  const user = currentUser();
  return user && roleAccess[user.role].includes(view);
}

function scopedStudents() {
  const user = currentUser();
  if (!user) return [];
  if (user.role === 'coordenador') return state.students;
  if (user.role === 'representante' || user.role === 'professor') {
    return state.students.filter(student => user.classes.includes(student.className));
  }
  if (user.role === 'responsavel') {
    return state.students.filter(student => user.studentIds.includes(student.id));
  }
  return [];
}

function scopedRoutines() {
  const user = currentUser();
  if (!user) return [];
  if (user.role === 'coordenador') return state.routines;
  if (user.role === 'representante' || user.role === 'professor') return state.routines.filter(routine => user.classes.includes(routine.className));
  const classes = scopedStudents().map(student => student.className);
  return state.routines.filter(routine => classes.includes(routine.className));
}

function scopedDocuments() {
  const user = currentUser();
  if (!user) return [];
  if (user.role === 'coordenador') return state.documents;
  const ids = scopedStudents().map(student => student.id);
  return state.documents.filter(document => ids.includes(document.studentId));
}

function init() {
  qs('#routineDate').value = today();
  qs('#deliveryDate').value = today();
  qs('#absenceDate').value = today();
  renderDemoUsers();
  bindEvents();
  renderSession();
}

function bindEvents() {
  qs('#toggleMenu').addEventListener('click', () => qs('#sidebar').classList.toggle('open'));
  qs('#logoutButton').addEventListener('click', logout);
  qs('#loginForm').addEventListener('submit', login);
  qs('#routineForm').addEventListener('submit', saveRoutine);
  qs('#documentForm').addEventListener('submit', saveDocument);
  qs('#deliveryForm').addEventListener('submit', saveDelivery);
  qs('#studentForm').addEventListener('submit', saveStudent);
  qs('#userForm').addEventListener('submit', saveUser);
  qs('#csvForm').addEventListener('submit', importCsvFile);
  qs('#sheetsForm').addEventListener('submit', importFromSheets);

  qsa('.menu__item').forEach(button => {
    button.addEventListener('click', () => switchView(button.dataset.view));
  });
  qs('#routineClass').addEventListener('change', renderAttendanceList);
}

function renderDemoUsers() {
  qs('#demoUsers').innerHTML = seedState.users.map(user => `
    <button class="demo-user" type="button" data-email="${user.email}">
      <strong>${roleLabels[user.role]}</strong><br>${user.email} · senha 123456
    </button>
  `).join('');
  qsa('.demo-user').forEach(button => button.addEventListener('click', () => {
    qs('#email').value = button.dataset.email;
    qs('#password').value = '123456';
  }));
}

function login(event) {
  event.preventDefault();
  const email = qs('#email').value.trim().toLowerCase();
  const password = qs('#password').value;
  const user = state.users.find(item => item.email.toLowerCase() === email && item.password === password);
  if (!user) {
    showToast('E-mail ou senha inválidos.');
    return;
  }
  state.currentUserId = user.id;
  saveState();
  currentView = 'dashboard';
  renderSession();
  showToast(`Bem-vindo(a), ${user.name}!`);
}

function logout() {
  state.currentUserId = null;
  saveState();
  renderSession();
  showToast('Sessão encerrada com segurança.');
}

function renderSession() {
  const user = currentUser();
  qs('#loginPanel').classList.toggle('hidden', Boolean(user));
  qs('#workspace').classList.toggle('hidden', !user);
  qs('#logoutButton').classList.toggle('hidden', !user);
  qs('#sessionName').textContent = user ? user.name : 'Visitante';
  qs('#sessionRole').textContent = user ? roleLabels[user.role] : 'Faça login';

  qsa('.menu__item').forEach(button => {
    const allowed = user && canAccess(button.dataset.view);
    button.classList.toggle('locked', user && !allowed);
    button.classList.toggle('active', user && button.dataset.view === currentView);
  });

  if (user) {
    if (!canAccess(currentView)) currentView = 'dashboard';
    switchView(currentView, true);
    renderAll();
  }
}

function switchView(view, silent = false) {
  if (!canAccess(view)) {
    if (!silent) showToast('Você não tem permissão para acessar esta área.');
    return;
  }
  currentView = view;
  qsa('.view').forEach(element => element.classList.toggle('active', element.id === `view-${view}`));
  qsa('.menu__item').forEach(button => button.classList.toggle('active', button.dataset.view === view));
  const activeButton = qs(`.menu__item[data-view="${view}"]`);
  qs('#pageTitle').textContent = activeButton ? activeButton.textContent : 'SOE Rosa Romita';
  qs('#sidebar').classList.remove('open');
  renderAll();
}

function renderAll() {
  renderAccessNotice();
  renderMetrics();
  renderTimeline();
  renderRoutineControls();
  renderChildrenArea();
  renderTeacherArea();
  renderCoordinatorArea();
  renderImportPreview();
}

function renderAccessNotice() {
  const user = currentUser();
  const descriptions = {
    representante: `Acesso restrito à(s) turma(s): ${user.classes.join(', ')}.`,
    responsavel: 'Acesso restrito às informações dos filhos associados ao cadastro.',
    professor: `Acesso às turmas em que leciona: ${user.classes.join(', ')}.`,
    coordenador: 'Acesso completo aos dados, cadastros, permissões e documentos do sistema.'
  };
  qs('#accessNotice').innerHTML = `<strong>${roleLabels[user.role]}</strong> · ${descriptions[user.role]}`;
}

function renderMetrics() {
  const students = scopedStudents();
  const routines = scopedRoutines();
  const docs = scopedDocuments();
  const absences = routines.flatMap(routine => Object.entries(routine.attendance || {})).filter(([, status]) => status === 'Ausente').length;
  qs('#metricCards').innerHTML = [
    ['Alunos visíveis', students.length],
    ['Registros de rotina', routines.length],
    ['Faltas registradas', absences],
    ['Documentos anexados', docs.length]
  ].map(([label, value]) => `<article class="metric"><span>${label}</span><strong>${value}</strong></article>`).join('');
}

function renderTimeline() {
  const items = [
    ...scopedRoutines().map(routine => ({ date: routine.date, title: `Rotina ${routine.className}`, text: routine.homework })),
    ...scopedDocuments().map(document => ({ date: document.date, title: document.type, text: `${studentName(document.studentId)} · ${document.fileName || 'sem arquivo'}` }))
  ].sort((a, b) => b.date.localeCompare(a.date)).slice(0, 6);
  qs('#activityTimeline').innerHTML = items.length ? items.map(item => `
    <div class="timeline__item"><strong>${formatDate(item.date)} · ${item.title}</strong><br><span>${item.text}</span></div>
  `).join('') : '<p class="hint">Nenhuma atividade recente para o seu perfil.</p>';
}

function renderRoutineControls() {
  const user = currentUser();
  const classSelect = qs('#routineClass');
  const classes = user.role === 'coordenador' ? [...new Set(state.students.map(s => s.className))] : user.classes || [];
  classSelect.innerHTML = classes.map(className => `<option value="${className}">${className}</option>`).join('');
  qs('#classScopePill').textContent = user.role === 'coordenador' ? 'Todas as turmas' : `Turma: ${classes.join(', ')}`;
  renderAttendanceList();
}

function renderAttendanceList() {
  const selectedClass = qs('#routineClass').value;
  const students = state.students.filter(student => student.className === selectedClass);
  qs('#attendanceList').innerHTML = `<strong>Controle de frequência</strong>${students.map(student => `
    <div class="attendance-row">
      <span>${student.name}</span>
      <div class="segmented">
        <label><input type="radio" name="att-${student.id}" value="Presente" checked> Presente</label>
        <label><input type="radio" name="att-${student.id}" value="Ausente"> Ausente</label>
      </div>
    </div>
  `).join('') || '<p class="hint">Nenhum aluno cadastrado nesta turma.</p>'}`;
}

function saveRoutine(event) {
  event.preventDefault();
  const user = currentUser();
  if (!['representante', 'coordenador'].includes(user.role)) return showToast('Apenas representante ou coordenação podem salvar rotina.');
  const className = qs('#routineClass').value;
  const attendance = {};
  state.students.filter(student => student.className === className).forEach(student => {
    attendance[student.id] = qs(`input[name="att-${student.id}"]:checked`)?.value || 'Presente';
  });
  state.routines.unshift({
    id: crypto.randomUUID(),
    date: qs('#routineDate').value,
    className,
    createdBy: user.id,
    lessonContent: qs('#lessonContent').value,
    homework: qs('#homework').value,
    dailyReading: qs('#dailyReading').value,
    attendance
  });
  event.target.reset();
  qs('#routineDate').value = today();
  saveState();
  renderAll();
  showToast('Rotina, frequência, tarefas e leitura salvas.');
}

function renderChildrenArea() {
  const children = scopedStudents();
  qs('#childrenData').innerHTML = children.length ? children.map(student => {
    const studentRoutines = state.routines.filter(routine => routine.className === student.className);
    const frequency = studentRoutines.map(routine => `${formatDate(routine.date)}: ${routine.attendance?.[student.id] || 'Sem lançamento'}`).join('<br>');
    const deliveries = state.deliveries.filter(delivery => delivery.studentId === student.id).map(delivery => `${delivery.title}: ${delivery.status}`).join('<br>') || 'Sem entregas lançadas.';
    return `<div class="child-card"><div><strong>${student.name}</strong><br><span>${student.className}</span><p>${frequency || 'Sem frequência.'}</p><p><strong>Entregas:</strong><br>${deliveries}</p></div></div>`;
  }).join('') : '<p class="hint">Nenhum filho associado a este usuário.</p>';
  qs('#documentStudent').innerHTML = children.map(student => `<option value="${student.id}">${student.name} · ${student.className}</option>`).join('');
}

function saveDocument(event) {
  event.preventDefault();
  const file = qs('#documentFile').files[0];
  state.documents.unshift({
    id: crypto.randomUUID(),
    studentId: qs('#documentStudent').value,
    date: qs('#absenceDate').value,
    type: qs('#documentType').value,
    note: qs('#documentNote').value,
    fileName: file ? file.name : 'Documento físico ou não anexado',
    uploadedBy: currentUser().name,
    uploadedAt: new Date().toISOString()
  });
  event.target.reset();
  qs('#absenceDate').value = today();
  saveState();
  renderAll();
  showToast('Documento anexado com visibilidade restrita.');
}

function renderTeacherArea() {
  const students = scopedStudents();
  qs('#deliveryStudent').innerHTML = students.map(student => `<option value="${student.id}">${student.name} · ${student.className}</option>`).join('');
  qs('#teacherRoutines').innerHTML = scopedRoutines().map(routine => `
    <div class="record"><div><strong>${formatDate(routine.date)} · ${routine.className}</strong><br>${routine.lessonContent}<br><span class="hint">Tarefa: ${routine.homework}</span></div></div>
  `).join('') || '<p class="hint">Sem registros de representantes nas suas turmas.</p>';

  const rows = scopedDocuments().map(document => {
    const student = state.students.find(item => item.id === document.studentId);
    const phone = normalizePhone(student?.guardianPhone);
    return `<tr>
      <td>${student?.name || '-'}</td>
      <td>${formatDate(document.date)}</td>
      <td><span class="badge badge--danger">${document.type}</span><br>${document.note || ''}</td>
      <td>${document.fileName || '-'}</td>
      <td>${student?.guardianName || '-'}<br>${student?.guardianPhone || '-'}</td>
      <td><a class="button button--small button--whatsapp" href="https://wa.me/55${phone}" target="_blank" rel="noopener">WhatsApp</a><a class="button button--small button--phone" href="tel:+55${phone}">Ligar</a></td>
    </tr>`;
  }).join('');
  qs('#teacherDocumentsTable').innerHTML = `<thead><tr><th>Aluno</th><th>Falta</th><th>Documento</th><th>Arquivo</th><th>Responsável</th><th>Ações</th></tr></thead><tbody>${rows || '<tr><td colspan="6">Sem documentos visíveis.</td></tr>'}</tbody>`;
}

function saveDelivery(event) {
  event.preventDefault();
  state.deliveries.unshift({
    id: crypto.randomUUID(),
    studentId: qs('#deliveryStudent').value,
    title: qs('#deliveryTitle').value,
    status: qs('#deliveryStatus').value,
    date: qs('#deliveryDate').value,
    teacherId: currentUser().id
  });
  event.target.reset();
  qs('#deliveryDate').value = today();
  saveState();
  renderAll();
  showToast('Entrega de atividade lançada para o aluno.');
}

function renderCoordinatorArea() {
  const rows = state.documents.map(document => {
    const student = state.students.find(item => item.id === document.studentId);
    return `<tr><td>${student?.name || '-'}</td><td>${student?.className || '-'}</td><td>${formatDate(document.date)}</td><td>${document.type}</td><td>${document.fileName || '-'}</td><td>${document.uploadedBy}</td></tr>`;
  }).join('');
  qs('#adminAbsencesTable').innerHTML = `<thead><tr><th>Aluno</th><th>Turma</th><th>Dia exato</th><th>Tipo</th><th>Arquivo</th><th>Enviado por</th></tr></thead><tbody>${rows || '<tr><td colspan="6">Sem faltas justificadas.</td></tr>'}</tbody>`;
}

function saveStudent(event) {
  event.preventDefault();
  const email = qs('#guardianEmail').value.trim().toLowerCase();
  const student = {
    id: crypto.randomUUID(),
    name: qs('#studentName').value,
    className: qs('#studentClass').value.trim().toUpperCase(),
    guardianName: qs('#guardianName').value,
    guardianEmail: email,
    guardianPhone: qs('#guardianPhone').value
  };
  state.students.push(student);
  const guardian = state.users.find(user => user.email.toLowerCase() === email && user.role === 'responsavel');
  if (guardian && !guardian.studentIds.includes(student.id)) guardian.studentIds.push(student.id);
  event.target.reset();
  saveState();
  renderAll();
  showToast('Aluno cadastrado e vínculo do responsável atualizado.');
}

function saveUser(event) {
  event.preventDefault();
  const role = qs('#userRole').value;
  const scope = qs('#userScope').value.split(',').map(item => item.trim()).filter(Boolean);
  const email = qs('#userEmail').value.trim().toLowerCase();
  const existing = state.users.find(user => user.email.toLowerCase() === email);
  const payload = {
    name: qs('#userName').value,
    email,
    password: qs('#userPassword').value,
    role,
    classes: ['representante', 'professor', 'coordenador'].includes(role) ? scope.map(item => item.toUpperCase()) : [],
    studentIds: role === 'responsavel' ? scope : []
  };
  if (existing) Object.assign(existing, payload);
  else state.users.push({ id: crypto.randomUUID(), ...payload });
  event.target.reset();
  saveState();
  renderAll();
  showToast('Usuário e permissões atualizados.');
}

async function importCsvFile(event) {
  event.preventDefault();
  const file = qs('#csvFile').files[0];
  if (!file) return;
  const text = await file.text();
  processCsv(text);
  event.target.reset();
}

async function importFromSheets(event) {
  event.preventDefault();
  const url = qs('#sheetsUrl').value.trim();
  if (!url) return showToast('Informe uma URL pública da planilha.');
  try {
    const response = await fetch(url);
    const text = await response.text();
    processCsv(text);
  } catch (error) {
    showToast(`Não foi possível ler a planilha: ${error.message}`);
  }
}

function processCsv(text) {
  const lines = text.trim().split(/\r?\n/).filter(Boolean);
  if (lines.length < 2) return showToast('CSV sem dados para importar.');
  const headers = splitCsvLine(lines.shift()).map(header => header.trim().toLowerCase());
  lines.forEach(line => {
    const values = splitCsvLine(line);
    const row = Object.fromEntries(headers.map((header, index) => [header, values[index]?.trim() || '']));
    if (row.nome && row.turma && row.responsavel) {
      const student = {
        id: crypto.randomUUID(),
        name: row.nome,
        className: row.turma.toUpperCase(),
        guardianName: row.responsavel,
        guardianEmail: row.email,
        guardianPhone: row.telefone
      };
      state.students.push(student);
    }
    if (row.tipo && row.email) {
      state.users.push({
        id: crypto.randomUUID(),
        name: row.nome || row.email,
        email: row.email.toLowerCase(),
        password: row.senha || '123456',
        role: row.tipo,
        classes: ['representante', 'professor', 'coordenador'].includes(row.tipo) ? (row.escopo || row.turma || '').split(',').map(item => item.trim().toUpperCase()).filter(Boolean) : [],
        studentIds: []
      });
    }
  });
  saveState();
  renderAll();
  showToast('Planilha processada e cadastros criados automaticamente.');
}

function splitCsvLine(line) {
  const values = [];
  let current = '';
  let quoted = false;
  for (const char of line) {
    if (char === '"') quoted = !quoted;
    else if (char === ',' && !quoted) {
      values.push(current);
      current = '';
    } else current += char;
  }
  values.push(current);
  return values;
}

function renderImportPreview() {
  const rows = state.students.map(student => `<tr><td>${student.name}</td><td>${student.className}</td><td>${student.guardianName}</td><td>${student.guardianEmail}</td><td>${student.guardianPhone}</td></tr>`).join('');
  qs('#importPreviewTable').innerHTML = `<thead><tr><th>Aluno</th><th>Turma</th><th>Responsável</th><th>E-mail</th><th>Telefone</th></tr></thead><tbody>${rows}</tbody>`;
}

function studentName(studentId) {
  return state.students.find(student => student.id === studentId)?.name || 'Aluno não encontrado';
}

init();
