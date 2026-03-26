const displayEl = document.getElementById("display");
const keysEl = document.getElementById("keys");

const operators = new Set(["+", "-", "*", "/"]);
let expression = "0";
let justCalculated = false;

function safeEval(input) {
  if (!/^[\d+\-*/. ]+$/.test(input)) return null;

  try {
    const value = Function(`"use strict"; return (${input});`)();
    if (!Number.isFinite(value)) return null;
    return Number(value.toFixed(10)).toString();
  } catch {
    return null;
  }
}

function updateDisplay() {
  displayEl.textContent = expression;
}

function appendNumber(num) {
  if (justCalculated || expression === "0") {
    expression = num;
    justCalculated = false;
  } else {
    expression += num;
  }
  updateDisplay();
}

function appendDot() {
  if (justCalculated) {
    expression = "0.";
    justCalculated = false;
    updateDisplay();
    return;
  }

  const currentChunk = expression.split(/[+\-*/]/).pop() ?? "";
  if (!currentChunk.includes(".")) {
    expression += ".";
    updateDisplay();
  }
}

function appendOperator(op) {
  justCalculated = false;
  const last = expression.at(-1);
  if (operators.has(last)) {
    expression = expression.slice(0, -1) + op;
  } else {
    expression += op;
  }
  updateDisplay();
}

function calculate() {
  const result = safeEval(expression);
  if (result === null) {
    displayEl.textContent = "Err";
    setTimeout(() => {
      expression = "0";
      updateDisplay();
    }, 500);
    return;
  }

  expression = result;
  justCalculated = true;
  updateDisplay();
}

keysEl.addEventListener("click", (event) => {
  const button = event.target.closest("button");
  if (!button) return;

  const { value, action } = button.dataset;

  if (action === "equals") {
    calculate();
    return;
  }

  if (!value) return;
  if (/^\d$/.test(value)) return appendNumber(value);
  if (value === ".") return appendDot();
  appendOperator(value);
});

window.addEventListener("keydown", (event) => {
  const { key } = event;
  if (/^\d$/.test(key)) return appendNumber(key);
  if (key === ".") return appendDot();
  if (operators.has(key)) return appendOperator(key);
  if (key === "=" || key === "Enter") return calculate();
});

updateDisplay();
