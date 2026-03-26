const displayEl = document.getElementById("display");
const historyEl = document.getElementById("history");
const keysEl = document.getElementById("keys");

const operators = new Set(["+", "-", "*", "/"]);
let expression = "0";
let resultShown = false;

function toView(text) {
  return text.replace(/\*/g, "×").replace(/\//g, "÷").replace(/\./g, ",");
}

function updateDisplay() {
  displayEl.textContent = toView(expression);
}

function normalizeExpression(value) {
  if (value === "") return "0";
  if (value.startsWith(".")) return `0${value}`;
  return value;
}

function safeEval(input) {
  if (!/^[\d+\-*/.() ]+$/.test(input)) return null;

  try {
    const value = Function(`"use strict"; return (${input});`)();
    if (!Number.isFinite(value)) return null;
    return Number(value.toFixed(10)).toString();
  } catch {
    return null;
  }
}

function appendNumber(num) {
  if (resultShown) {
    expression = num;
    resultShown = false;
    updateDisplay();
    return;
  }

  if (expression === "0") {
    expression = num;
  } else {
    expression += num;
  }

  updateDisplay();
}

function appendDot() {
  if (resultShown) {
    expression = "0.";
    resultShown = false;
    updateDisplay();
    return;
  }

  const lastPart = expression.split(/[+\-*/]/).pop();
  if (!lastPart.includes(".")) expression += ".";
  updateDisplay();
}

function appendOperator(op) {
  resultShown = false;
  const lastChar = expression.at(-1);

  if (operators.has(lastChar)) {
    expression = `${expression.slice(0, -1)}${op}`;
  } else {
    expression += op;
  }

  expression = normalizeExpression(expression);
  updateDisplay();
}

function clearAll() {
  expression = "0";
  resultShown = false;
  historyEl.textContent = "";
  updateDisplay();
}

function deleteLast() {
  if (resultShown) {
    clearAll();
    return;
  }

  expression = expression.slice(0, -1);
  expression = normalizeExpression(expression);
  updateDisplay();
}

function toggleSign() {
  if (expression === "0") return;

  const parts = expression.split(/([+\-*/])/);
  const last = parts[parts.length - 1];

  if (!last || operators.has(last)) return;

  if (last.startsWith("-")) {
    parts[parts.length - 1] = last.slice(1);
  } else {
    parts[parts.length - 1] = `-${last}`;
  }

  expression = parts.join("");
  updateDisplay();
}

function toPercent() {
  const value = safeEval(expression);
  if (value === null) return;
  expression = (Number(value) / 100).toString();
  resultShown = true;
  historyEl.textContent = `${toView(value)}%`;
  updateDisplay();
}

function calculate() {
  const value = safeEval(expression);
  if (value === null) {
    displayEl.textContent = "Hata";
    setTimeout(updateDisplay, 800);
    return;
  }

  historyEl.textContent = `${toView(expression)} =`;
  expression = value;
  resultShown = true;
  updateDisplay();
}

keysEl.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;

  const { value, action } = button.dataset;

  if (value) {
    if (/^\d$/.test(value)) appendNumber(value);
    else if (value === ".") appendDot();
    else appendOperator(value);
    return;
  }

  switch (action) {
    case "clear":
      clearAll();
      break;
    case "delete":
      deleteLast();
      break;
    case "toggle-sign":
      toggleSign();
      break;
    case "percent":
      toPercent();
      break;
    case "equals":
      calculate();
      break;
    default:
      break;
  }
});

window.addEventListener("keydown", (event) => {
  const key = event.key;

  if (/^\d$/.test(key)) return appendNumber(key);
  if (key === ".") return appendDot();
  if (operators.has(key)) return appendOperator(key);
  if (key === "Enter" || key === "=") return calculate();
  if (key === "Backspace") return deleteLast();
  if (key.toLowerCase() === "c") return clearAll();
  if (key === "%") return toPercent();
});

updateDisplay();
