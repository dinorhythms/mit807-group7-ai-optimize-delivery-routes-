// Global state
let nodeNames = [];

// DOM Elements
const sourceSelect = document.getElementById('source');
const destSelect = document.getElementById('destination');
const bfsBtn = document.getElementById('bfs-btn');
const dfsBtn = document.getElementById('dfs-btn');
const astarBtn = document.getElementById('astar-btn');
const loadingEl = document.getElementById('loading');
const resultsEl = document.getElementById('results');
const errorEl = document.getElementById('error');
const statusEl = document.getElementById('status');
const initialMsg = document.getElementById('initial-message');

// Slider elements
const trafficSlider = document.getElementById('traffic');
const peakSlider = document.getElementById('peak');
const weatherSlider = document.getElementById('weather');
const rerouteSlider = document.getElementById('reroute');

// Slider value displays
const trafficValue = document.getElementById('traffic-value');
const peakValue = document.getElementById('peak-value');
const weatherValue = document.getElementById('weather-value');
const rerouteValue = document.getElementById('reroute-value');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initializeApp();
  setupEventListeners();
});

async function initializeApp() {
  try {
    const response = await fetch('/api/nodes');
    const data = await response.json();
    nodeNames = data.nodes;
    populateSelects();
  } catch (error) {
    console.error('Failed to load nodes:', error);
    showError('Failed to load location data. Please refresh the page.');
  }
}

function populateSelects() {
  // Clear existing options (except currently selected)
  const selectedSource = sourceSelect.value || 'Select Source';
  const selectedDest = destSelect.value || 'Ajah';

  sourceSelect.innerHTML = '';
  destSelect.innerHTML = '';

  nodeNames.forEach((node) => {
    const sourceOption = document.createElement('option');
    sourceOption.value = node;
    sourceOption.textContent = node;
    sourceSelect.appendChild(sourceOption);

    const destOption = document.createElement('option');
    destOption.value = node;
    destOption.textContent = node;
    destSelect.appendChild(destOption);
  });

  // Set selected values
  if (nodeNames.includes(selectedSource)) {
    sourceSelect.value = selectedSource;
  } else if (nodeNames.length > 0) {
    sourceSelect.value = nodeNames[0];
  }

  if (nodeNames.includes(selectedDest)) {
    destSelect.value = selectedDest;
  } else if (nodeNames.length > 1) {
    destSelect.value = nodeNames[1];
  }
}

function setupEventListeners() {
  bfsBtn.addEventListener('click', () => runAlgorithm('bfs'));
  dfsBtn.addEventListener('click', () => runAlgorithm('dfs'));
  astarBtn.addEventListener('click', () => runAlgorithm('astar'));

  trafficSlider.addEventListener('input', (e) => {
    trafficValue.textContent = parseFloat(e.target.value).toFixed(2);
  });

  peakSlider.addEventListener('input', (e) => {
    peakValue.textContent = parseFloat(e.target.value).toFixed(2);
  });

  weatherSlider.addEventListener('input', (e) => {
    weatherValue.textContent = parseFloat(e.target.value).toFixed(2);
  });

  rerouteSlider.addEventListener('input', (e) => {
    rerouteValue.textContent = parseFloat(e.target.value).toFixed(2);
  });
}

async function runAlgorithm(algorithm) {
  const source = sourceSelect.value;
  const destination = destSelect.value;

  if (!source || !destination) {
    showError('Please select both source and destination.');
    return;
  }

  if (source === destination) {
    showError('Source and destination cannot be the same.');
    return;
  }

  // Show loading state
  showLoading(true);
  clearResults();
  setStatus('Running...');

  try {
    let endpoint = '';
    let payload = {
      source: source,
      destination: destination,
    };

    if (algorithm === 'bfs') {
      endpoint = '/api/run-bfs';
    } else if (algorithm === 'dfs') {
      endpoint = '/api/run-dfs';
    } else if (algorithm === 'astar') {
      endpoint = '/api/run-astar';
      payload.traffic_level = parseFloat(trafficSlider.value);
      payload.peak_factor = parseFloat(peakSlider.value);
      payload.weather_factor = parseFloat(weatherSlider.value);
      payload.reroute_factor = parseFloat(rerouteSlider.value);
    }

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Algorithm execution failed');
    }

    const result = await response.json();
    displayResults(result);
    setStatus('Complete', 'success');
  } catch (error) {
    console.error('Error running algorithm:', error);
    showError(error.message || 'An error occurred. Please try again.');
    setStatus('Error', 'error');
  } finally {
    showLoading(false);
  }
}

function displayResults(result) {
  // Hide initial message
  initialMsg.style.display = 'none';

  // Show results container
  resultsEl.classList.remove('hidden');

  // Set algorithm title
  document.getElementById('result-title').textContent = result.title;

  // Format and display traversal order
  const traversalText =
    result.traversal_order && result.traversal_order.length > 0
      ? result.traversal_order.join(' → ')
      : 'No traversal result';
  document.getElementById('traversal').textContent = traversalText;

  // Format and display path
  const pathText =
    result.path && result.path.length > 0
      ? result.path.join(' → ')
      : 'No path found';
  document.getElementById('path').textContent = pathText;

  // Format and display metrics
  let metricsText = '';
  if (result.total_cost !== null && result.total_cost !== undefined) {
    metricsText = `${result.cost_label}: ${result.total_cost}`;
  } else {
    metricsText = 'No cost information available';
  }
  document.getElementById('metrics').textContent = metricsText;

  // Display scenario parameters if available (A* only)
  const scenarioEl = document.getElementById('scenario');
  if (result.scenario) {
    scenarioEl.classList.remove('hidden');
    const scenarioContent = document.getElementById('scenario-content');
    let scenarioText = '';
    for (const [key, value] of Object.entries(result.scenario)) {
      const formattedKey = key
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (c) => c.toUpperCase());
      scenarioText += `${formattedKey}: ${(value * 100).toFixed(1)}%\n`;
    }
    scenarioContent.textContent = scenarioText;
  } else {
    scenarioEl.classList.add('hidden');
  }
}

function clearResults() {
  document.getElementById('result-title').textContent = 'Result';
  document.getElementById('traversal').textContent = '—';
  document.getElementById('path').textContent = '—';
  document.getElementById('metrics').textContent = '—';
}

function showLoading(show) {
  if (show) {
    loadingEl.classList.remove('hidden');
  } else {
    loadingEl.classList.add('hidden');
  }
}

function showError(message) {
  errorEl.textContent = message;
  errorEl.classList.remove('hidden');
  resultsEl.classList.add('hidden');

  // Auto-hide error after 5 seconds
  setTimeout(() => {
    errorEl.classList.add('hidden');
  }, 5000);
}

function setStatus(text, type = 'default') {
  statusEl.textContent = text;
  statusEl.classList.remove('success', 'error');
  if (type === 'success') {
    statusEl.classList.add('success');
  } else if (type === 'error') {
    statusEl.classList.add('error');
  }
}
