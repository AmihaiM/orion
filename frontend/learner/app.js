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
  } catch {
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

  nextBtn.style.display = "none";
  nextBtn.disabled = true;

  recordBtn.style.display = "inline-block";
  recordBtn.disabled = false;
}

function speakCurrentSentence() {
  const sentence = currentMission.sentences[currentIndex];
  const utterance = new SpeechSynthesisUtterance(sentence.english_text);
  utterance.lang = "en-US";
  speechSynthesis.speak(utterance);
}

function recordCurrentSentence() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    showFeedback({
      message: "הדפדפן לא תומך בזיהוי דיבור. נסה Chrome.",
      accuracy_score: 0,
      spoken_text: "",
      passed: false,
      next_action: "RETRY_SENTENCE",
    });
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recordBtn.textContent = "מקשיב...";
  recordBtn.disabled = true;
  nextBtn.style.display = "none";

  recognition.onresult = async (event) => {
    const spoken = event.results[0][0].transcript;
    const sentence = currentMission.sentences[currentIndex];

    try {
      const result = await api("/attempts", {
        method: "POST",
        body: JSON.stringify({
          student_id: DEMO_STUDENT_ID,
          mission_id: currentMission.mission.id,
          sentence_id: sentence.id,
          session_id: currentSession.id,
          stage: "practice",
          spoken_text: spoken,
          accuracy_score: 0,
          passed: false,
          recording_duration_ms: 0,
          silence_ms: 0,
          words_per_minute: 0,
          fluency_status: "",
        }),
      });

      results.push({
        sentence_id: sentence.id,
        spoken,
        score: result.accuracy_score,
        passed: result.passed,
        next_action: result.next_action,
      });

      showFeedback(result);

      if (result.next_action === "NEXT_SENTENCE") {
        nextBtn.style.display = "inline-block";
        nextBtn.disabled = false;
        recordBtn.style.display = "none";
      } else if (result.next_action === "RETRY_SENTENCE") {
        nextBtn.style.display = "none";
        nextBtn.disabled = true;
        recordBtn.style.display = "inline-block";
      } else {
        nextBtn.style.display = "inline-block";
        nextBtn.disabled = false;
      }
    } catch (err) {
      showFeedback({
        message: `API error: ${err.message}`,
        accuracy_score: 0,
        spoken_text: spoken,
        passed: false,
        next_action: "RETRY_SENTENCE",
      });
    }
  };

  recognition.onerror = (event) => {
    showFeedback({
      message: `Speech error: ${event.error}`,
      accuracy_score: 0,
      spoken_text: "",
      passed: false,
      next_action: "RETRY_SENTENCE",
    });
  };

  recognition.onend = () => {
    recordBtn.textContent = "🎤 הקלט";
    recordBtn.disabled = false;
  };

  recognition.start();
}

function showFeedback(result) {
  const score = result.accuracy_score || 0;
  const cls = score >= 85 ? "score-ok" : score >= 60 ? "score-warn" : "score-bad";

  feedback.innerHTML = `
    <p><strong>${result.message || ""}</strong></p>
    <p>Score: <span class="${cls}">${score}%</span></p>
    <p>Status: <strong>${result.passed ? "Passed" : "Try again"}</strong></p>
    <p>Action: <strong>${result.next_action || ""}</strong></p>
    <p dir="ltr">You said: ${result.spoken_text || "—"}</p>
  `;

  feedback.classList.remove("hidden");
}

async function nextSentence() {
  const nextStep = await api(`/learning-sessions/${currentSession.id}/next`);

  if (nextStep.next_action === "MISSION_COMPLETED") {
    completeMission();
    return;
  }

  if (!nextStep.sentence) {
    completeMission();
    return;
  }

  const nextIndex = currentMission.sentences.findIndex(
    (s) => s.id === nextStep.sentence.id
  );

  if (nextIndex >= 0) {
    currentIndex = nextIndex;
  }

  renderSentence();
}

function completeMission() {
  practicePanel.classList.add("hidden");
  completePanel.classList.remove("hidden");

  const avg = results.length
    ? Math.round(results.reduce((sum, r) => sum + r.score, 0) / results.length)
    : 0;

  summary.innerHTML = `
    <p>Average score: <strong>${avg}%</strong></p>
    <p>Session ID: ${currentSession.id}</p>
  `;
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