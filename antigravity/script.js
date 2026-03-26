const calculator = {
    displayValue: '0',
    firstOperand: null,
    waitingForSecondOperand: false,
    operator: null,
};

function inputDigit(digit) {
    const { displayValue, waitingForSecondOperand } = calculator;

    if (waitingForSecondOperand === true) {
        calculator.displayValue = digit;
        calculator.waitingForSecondOperand = false;
    } else {
        calculator.displayValue = displayValue === '0' ? digit : displayValue + digit;
    }
}

function inputDecimal(dot) {
    if (calculator.waitingForSecondOperand === true) {
        calculator.displayValue = "0.";
        calculator.waitingForSecondOperand = false;
        return;
    }

    if (!calculator.displayValue.includes(dot)) {
        calculator.displayValue += dot;
    }
}

function handleOperator(nextOperator) {
    const { firstOperand, displayValue, operator } = calculator;
    const inputValue = parseFloat(displayValue);

    if (operator && calculator.waitingForSecondOperand) {
        calculator.operator = nextOperator;
        return;
    }

    if (firstOperand == null && !isNaN(inputValue)) {
        calculator.firstOperand = inputValue;
    } else if (operator) {
        const result = calculate(firstOperand, inputValue, operator);
        calculator.displayValue = `${parseFloat(result.toFixed(7))}`;
        calculator.firstOperand = result;
    }

    calculator.waitingForSecondOperand = true;
    calculator.operator = nextOperator;
}

function calculate(firstOperand, secondOperand, operator) {
    if (operator === '+') {
        return firstOperand + secondOperand;
    } else if (operator === '-') {
        return firstOperand - secondOperand;
    } else if (operator === '×') {
        return firstOperand * secondOperand;
    } else if (operator === '÷') {
        return firstOperand / secondOperand;
    }

    return secondOperand;
}

function updateDisplay() {
    const display = document.querySelector('#display');
    if (calculator.displayValue.length > 11) {
        display.innerText = calculator.displayValue.substring(0, 11);
    } else {
        display.innerText = calculator.displayValue;
    }
}

updateDisplay();

const keys = document.querySelector('.buttons');
keys.addEventListener('click', (event) => {
    const { target } = event;
    const value = target.innerText;

    if (!target.matches('button')) {
        return;
    }

    if (['+', '-', '×', '÷'].includes(value)) {
        handleOperator(value);
        updateDisplay();
        return;
    }

    if (value === '.') {
        inputDecimal(value);
        updateDisplay();
        return;
    }

    if (value === '=') {
        if (calculator.operator && !calculator.waitingForSecondOperand) {
            const result = calculate(calculator.firstOperand, parseFloat(calculator.displayValue), calculator.operator);
            calculator.displayValue = `${parseFloat(result.toFixed(7))}`;
            calculator.firstOperand = null;
            calculator.operator = null;
            calculator.waitingForSecondOperand = true;
            updateDisplay();
        }
        return;
    }

    // Number keys
    inputDigit(value);
    updateDisplay();
});
