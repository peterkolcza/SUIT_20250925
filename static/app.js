const GRID_SIZE = 9;
const gridElement = document.getElementById("sudoku-grid");
const form = document.getElementById("sudoku-form");
const output = document.getElementById("output");
const checkUnique = document.getElementById("check-unique");
const clearButton = document.getElementById("clear");
const exampleButton = document.getElementById("load-example");

const EXAMPLE_BOARD = [
  [5, 3, 0, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
];

function createCell(row, col) {
  const wrapper = document.createElement("div");
  wrapper.classList.add("cell");
  if ((col + 1) % 3 === 0 && col !== GRID_SIZE - 1) {
    wrapper.classList.add("subgrid-right");
  }
  if ((row + 1) % 3 === 0 && row !== GRID_SIZE - 1) {
    wrapper.classList.add("subgrid-bottom");
  }

  const input = document.createElement("input");
  input.type = "text";
  input.inputMode = "numeric";
  input.maxLength = 1;
  input.dataset.row = row;
  input.dataset.col = col;

  input.addEventListener("input", () => {
    input.value = input.value.replace(/[^0-9]/g, "");
    if (input.value.length > 1) {
      input.value = input.value.slice(-1);
    }
  });

  input.addEventListener("keydown", (event) => {
    const allowed = [
      "Backspace",
      "Delete",
      "Tab",
      "ArrowUp",
      "ArrowDown",
      "ArrowLeft",
      "ArrowRight",
    ];
    if (allowed.includes(event.key)) {
      return;
    }
    if (!/[0-9]/.test(event.key)) {
      event.preventDefault();
    }
  });

  wrapper.appendChild(input);
  return wrapper;
}

function buildGrid() {
  for (let row = 0; row < GRID_SIZE; row += 1) {
    for (let col = 0; col < GRID_SIZE; col += 1) {
      gridElement.appendChild(createCell(row, col));
    }
  }
}

function setBoard(board) {
  const cells = gridElement.querySelectorAll("input");
  cells.forEach((cell) => {
    const row = Number(cell.dataset.row);
    const col = Number(cell.dataset.col);
    const value = board[row][col];
    cell.value = value === 0 ? "" : String(value);
  });
}

function clearBoard() {
  const cells = gridElement.querySelectorAll("input");
  cells.forEach((cell) => {
    cell.value = "";
  });
  output.textContent = "";
  output.classList.remove("error");
}

function collectBoard() {
  const board = [];
  for (let row = 0; row < GRID_SIZE; row += 1) {
    const rowValues = [];
    for (let col = 0; col < GRID_SIZE; col += 1) {
      const selector = `input[data-row="${row}"][data-col="${col}"]`;
      const input = gridElement.querySelector(selector);
      const value = input.value.trim();
      if (value === "") {
        rowValues.push(0);
      } else {
        const num = Number(value);
        if (Number.isNaN(num) || num < 0 || num > 9) {
          throw new Error("Values must be digits between 0 and 9");
        }
        rowValues.push(num);
      }
    }
    board.push(rowValues);
  }
  return board;
}

function boardToString(board) {
  const horizontal = "+-------+-------+-------+";
  const rows = [];
  for (let r = 0; r < GRID_SIZE; r += 1) {
    if (r % 3 === 0) {
      rows.push(horizontal);
    }
    const chunks = [];
    for (let c = 0; c < GRID_SIZE; c += 3) {
      const slice = board[r].slice(c, c + 3).map((v) => (v === 0 ? "." : v));
      chunks.push(slice.join(" "));
    }
    rows.push(`| ${chunks.join(" | ")} |`);
  }
  rows.push(horizontal);
  return rows.join("\n");
}

async function submitBoard(event) {
  event.preventDefault();
  let board;
  try {
    board = collectBoard();
  } catch (error) {
    output.textContent = error.message;
    output.classList.add("error");
    return;
  }

  output.textContent = "Solving...";
  output.classList.remove("error");

  try {
    const response = await fetch("/api/solve", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        board,
        check_uniqueness: checkUnique.checked,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Unknown error");
    }
    setBoard(payload.solution);
    let message = boardToString(payload.solution);
    if (payload.unique !== undefined) {
      message += `\n\nSolution is ${payload.unique ? "unique" : "not unique"}.`;
    }
    output.textContent = message;
  } catch (error) {
    output.textContent = error.message;
    output.classList.add("error");
  }
}

buildGrid();
setBoard(EXAMPLE_BOARD);

form.addEventListener("submit", submitBoard);
clearButton.addEventListener("click", () => {
  clearBoard();
});
exampleButton.addEventListener("click", () => {
  setBoard(EXAMPLE_BOARD);
  output.textContent = "Loaded example puzzle.";
  output.classList.remove("error");
});

