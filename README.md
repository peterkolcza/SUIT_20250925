# Sudoku Solver

Deterministic Sudoku solver featuring a Python CLI and a lightweight Flask web interface. The solver uses backtracking with forward checking and a minimum remaining value (MRV) heuristic to solve standard 9×9 puzzles quickly and reliably.

## Features

- Pure functional core: parsing, validation, solving, and uniqueness checking.
- Command line interface with file/stdin input, optional uniqueness verification, and benchmarking.
- Flask web demo with responsive UI, live validation, and uniqueness toggle.
- Sample puzzles (easy → evil) with verified solutions.
- Thorough pytest suite and `pyflakes` lint target for confidence.

## Quick Start (macOS)

```bash
make setup
make test
make web  # launches the Flask development server on http://localhost:5000
```

The `setup` target creates a `.venv` virtual environment, installs Flask + pytest, and registers the project in editable mode.

### CLI Usage

Solve a puzzle from a file:

```bash
python -m sudoku.solve --file puzzles/easy.txt --format grid
```

Read a puzzle from stdin and check uniqueness:

```bash
cat puzzles/medium.txt | python -m sudoku.solve --stdin --check-unique --format plain
```

Benchmark the solver (5 iterations by default):

```bash
python -m sudoku.solve --bench puzzles/hard.txt --iterations 10
```

### Web Demo

After running `make web`, open `http://localhost:5000` in your browser. Enter digits (leave blanks empty or 0), toggle uniqueness checking if desired, and press **Solve**. The example button loads a ready-made puzzle for quick exploration.

### Testing and Linting

```bash
make lint
make test
```

Both commands run inside the virtual environment created by `make setup`.

### Benchmarking

```bash
make bench
```

Runs `python -m sudoku.solve --bench puzzles/hard.txt` to capture average solve times.

## Git használati útmutató

### Repozitórium klónozása nulláról

1. Válaszd ki azt a mappát, ahová a projekt kerülni fog.
2. Futtasd az alábbi parancsot (a `<url>` helyére írd be a GitHub repó HTTPS vagy SSH URL-jét):

   ```bash
   git clone <url>
   cd SUIT_20250925
   ```

   Az első sor letölti a teljes repót, a második pedig belép a frissen létrehozott könyvtárba.

### Frissítés a GitHub-on történt változások után

Ha már klónoztad a repót és szeretnéd a legfrissebb `main` állapotot, lépj a projekt mappájába, majd futtasd:

```bash
git pull origin main
```

Ez letölti és beolvasztja a távoli `main` ágon történt változtatásokat a helyi példányodba. Ha helyi módosításaid vannak, érdemes előbb commitolni vagy stash-elni őket, hogy elkerüld az ütközéseket.

### Másik branch letöltése és tesztelése

Amennyiben nem a `main`, hanem egy konkrét feature vagy fix branch állapotát szeretnéd kipróbálni:

```bash
git fetch origin
git checkout <branch-név>
```

Az első parancs letölti a távoli branch-ek aktuális állapotát, a második pedig átvált a megadott `<branch-név>` branchre. Ha még nincs helyi példánya a branch-nek, a `git checkout` létrehozza azt a távoli (`origin/<branch-név>`) alapján.

## API

`POST /api/solve`

Request body:

```json
{
  "board": [[5,3,0,0,7,0,0,0,0], [... 8 more rows ...]],
  "check_uniqueness": true
}
```

Response on success:

```json
{
  "solution": [[5,3,4,6,7,8,9,1,2], [...]],
  "unique": true
}
```

Errors return `{"error": "message"}` with a 4xx/422 status code.

## Sample Puzzles & Solutions

| Difficulty | Puzzle Source              | Solution (rows concatenated) |
|------------|----------------------------|-------------------------------|
| Easy       | `puzzles/easy.txt`         | `534678912672195348198342567859761423426853791713924856961537284287419635345286179` |
| Medium     | `puzzles/medium.txt`       | `435269781682571493197834562826195347374682915951743628519326874248957136763418259` |
| Hard       | `puzzles/hard.txt`         | `483921657967345821251876493548132976729564138136798245372689514814253769695417382` |
| Evil       | `puzzles/evil.txt`         | `123456987597428163864715326176934852358261749249587619912873645634159278785642931` |

All puzzles are solvable within a fraction of a second on a modern laptop.

## Project Layout

```
.
├── README.md
├── pyproject.toml
├── Makefile
├── sudoku/
│   ├── __init__.py
│   ├── core.py
│   ├── cli.py
│   ├── web.py
│   └── utils.py
├── static/
│   ├── styles.css
│   └── app.js
├── templates/
│   └── index.html
├── puzzles/
│   ├── easy.txt
│   ├── medium.txt
│   ├── hard.txt
│   └── evil.txt
└── tests/
    ├── test_core.py
    ├── test_parser.py
    └── test_api.py
```

## License

MIT License (see repository usage guidelines).

