const API_BASE = "http://127.0.0.1:8000";
const DEMO_STUDENT_ID = "ae0e2e7c-a72d-4b6b-9406-433a345759d1";

let currentMission = null;
let currentSession = null;
let currentIndex = 0;
let results = [];

const apiStatus = document.getElementById("apiStatus");
const loadMissionsBtn = document.getElementById("loadMissionsBtn");
const missionsList = document.getElementById("missionsList");
const missionPanel = document.getElementById("missionPanel");
const practicePanel = document.getElementById("practicePanel");
const completePanel = document.getElementById("completePanel");
const missionMeta = document.getElementById("missionMeta");
const missionTitle = document.getElementById("missionTitle");
const progressText = document.getElementById("progressText");
const hebrewText = document.getElementById("hebrewText");
const englishText = document.getElementById("englishText");
const speakBtn = document.getElementById("speakBtn");
const recordBtn = document.getElementById("recordBtn");
const nextBtn = document.getElementById("nextBtn");
const feedback = document.getElementById("feedback");
const summary = document.getElementById("summary");
const restartBtn = document.getElementById("restartBtn");

async function api(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(data));
  return data;
}

async function checkApi() {
  try {
    const health = await api("/health");
    apiStatus.textContent = `API: ${health.api}, Supabase: ${health.supabase}`;
  } catch (err) {
    apiStatus.textContent = "API: failed";
  }
}

async function loadMissions() {
  missionsList.innerHTML = "טוען...";
  const data = await api("/missions");
  if (!data.missions.length) {
    missionsList.innerHTML = "לא נמצאו Missions.";
    return;
  }

  missionsList.innerHTML = "";
  data.missions.forEach((mission) => {
    const row = document.createElement("div");
    row.className = "mission-item";
    row.innerHTML = `
      <div>
        <strong>${mission.title}</strong>
        <div class="muted">${mission.level || ""} · ${mission.unit || ""}</div>
      </div>
      <button class="primary">Start</button>
    `;
    row.querySelector("button").onclick = () => startMission(mission.id);
    missionsList.appendChild(row);
  });
}

async function startMission(missionId) {
  const detail = await api(`/missions/${missionId}`);
  currentMission = detail;
  currentIndex = 0;
  results = [];

  currentSession = await api("/learning-sessions", {
    method: "POST",
    body: JSON.stringify({
      student_id: DEMO_STUDENT_ID,
      mission_id: missionId,
      assignment_id: null,
    }),
  });

  missionPanel.classList.add("hidden");
  completePanel.classList.add("hidden");
  practicePanel.classList.remove("hidden");
  renderSentence();
}

function renderSentence() {
  const sentence = currentMission.sentences[currentIndex];
  missionMeta.textContent = `Session: ${currentSession.id}`;
  missionTitle.textContent = currentMission.mission.title;
  progressText.textContent = `${currentIndex + 1} / ${currentMission.sentences.length}`;
  hebrewText.textContent = sentence.hebrew_text || "";
  englishText.textContent = sentence.english_text;
  feedback.classList.add("hidden");
  feedback.innerHTML = "";
  nextBtn.disabled = true;
}

function speakCurrentSentence() {
  const sentence = currentMission.sentences[currentIndex];
  const utterance = new SpeechSynthesisUtterance(sentence.english_text);
  utterance.lang = "en-US";
  speechSynthesis.speak(utterance);
}

function normalize(text) {
  return text.toLowerCase().replace(/[^a-z0-9\s]/g, "").replace(/\s+/g, " ").trim();
}

function calculateAccuracy(expected, spoken) {
  const expectedWords = normalize(expected).split(" ").filter(Boolean);
  const spokenWords = normalize(spoken).split(" ").filter(Boolean);
  if (!expectedWords.length) return 0;
  let hits = 0;
  expectedWords.forEach((word) => {
    if (spokenWords.includes(word)) hits += 1;
  });
  return Math.round((hits / expectedWords.length) * 100);
}

function recordCurrentSentence() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    showFeedback("הדפדפן לא תומך בזיהוי דיבור. נסה Chrome.", 0, "");
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recordBtn.textContent = "מקשיב...";
  recordBtn.disabled = true;

  recognition.onresult = (event) => {
    const spoken = event.results[0][0].transcript;
    const sentence = currentMission.sentences[currentIndex];
    const score = calculateAccuracy(sentence.english_text, spoken);
    results.push({ sentence_id: sentence.id, spoken, score });
    showFeedback(score >= 85 ? "Great! Sentence passed." : "Good try. Let's improve it.", score, spoken);
    nextBtn.disabled = false;
  };

  recognition.onerror = (event) => {
    showFeedback(`Speech error: ${event.error}`, 0, "");
    nextBtn.disabled = false;
  };

  recognition.onend = () => {
    recordBtn.textContent = "🎤 הקלט";
    recordBtn.disabled = false;
  };

  recognition.start();
}

function showFeedback(message, score, spoken) {
  const cls = score >= 85 ? "score-ok" : score >= 60 ? "score-warn" : "score-bad";
  feedback.innerHTML = `
    <p><strong>${message}</strong></p>
    <p>Score: <span class="${cls}">${score}%</span></p>
    <p dir="ltr">You said: ${spoken || "—"}</p>
  `;
  feedback.classList.remove("hidden");
}

function nextSentence() {
  if (currentIndex < currentMission.sentences.length - 1) {
    currentIndex += 1;
    renderSentence();
  } else {
    completeMission();
  }
}

function completeMission() {
  practicePanel.classList.add("hidden");
  completePanel.classList.remove("hidden");
  const avg = results.length ? Math.round(results.reduce((sum, r) => sum + r.score, 0) / results.length) : 0;
  summary.innerHTML = `<p>Average score: <strong>${avg}%</strong></p><p>Session ID: ${currentSession.id}</p>`;
}

function restart() {
  currentMission = null;
  currentSession = null;
  currentIndex = 0;
  results = [];
  completePanel.classList.add("hidden");
  missionPanel.classList.remove("hidden");
}

loadMissionsBtn.onclick = loadMissions;
speakBtn.onclick = speakCurrentSentence;
recordBtn.onclick = recordCurrentSentence;
nextBtn.onclick = nextSentence;
restartBtn.onclick = restart;

checkApi();
