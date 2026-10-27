# Issues Found — hotel_booking_system.py

Line numbers refer to the original file. Reports: `*_report_before.txt` (original) and `*_report.txt` (after fixes).

Baseline: Pylint **5.32/10**, Bandit **6 issues** (2 High, 1 Medium, 3 Low), Flake8 **7 issues**.
Final: Pylint **10.00/10**, Bandit **0 issues**, Flake8 **0 issues**.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (Bandit B605, High) | Security | 58 | `os.system("echo ... " + filename)` passes the filename to a shell, so a crafted filename could run any command. | Removed the shell call and printed the message with `print()`. |
| Weak MD5 hash (Bandit B324, High) | Security | 47 | MD5 is broken and should not be used to hash guest IDs. | Switched to `hashlib.sha256`. |
| Use of `eval` (Bandit B307 Medium, Pylint W0123) | Security | 42 | `eval(rate_expr)` runs any Python code passed in as the rate string. | The function now takes a numeric `multiplier` and returns `base_price * multiplier`, checking that the multiplier is positive. |
| Hardcoded secret, printed to console (Bandit B105) | Security | 62, 70 | The admin token is in the source code and printed in plain text. | Read it from the `HOTEL_SECRET_KEY` environment variable; print only whether it is set, never the value. |
| Insecure random booking reference (Bandit B311) | Security | 51 | `random.randint` is predictable and not suitable for reference/ID tokens. | Used `secrets.randbelow(9000) + 1000`. |
| Try/except/pass with bare except (Bandit B110, Pylint W0702, Flake8 E722) | Bug | 26–27 | Every error is silently ignored; cancelling a room that doesn't exist looks like it worked. | Check `room_num in ROOM_INVENTORY` and return `True`/`False`. |
| Mutable default argument (Pylint W0102) | Bug | 15 | `booking_log=[]` is shared across all calls, so logs leak between bookings. | Default is `None`; a new list is created inside the function. |
| File opened without `with` or encoding (Pylint R1732, W1514) | Bug | 55–57 | The file is not closed if `write` fails, and the encoding depends on the platform. | `with open(filename, "w", encoding="utf-8")`. |
| Booking result ignored in `main` | Bug (logic, no tool flags it) | 63 | The return value of the booking and the booking log are never shown. | `main` prints the booking result and the log entries. |
| Comparison to `None` with `==` (Flake8 E711, Pylint C0121) | Style | 32 | `== None` should be `is None`. | Replaced with `is None`. |
| Unused import / variables (Flake8 F401, F841; Pylint W0611, W0612) | Style | 6, 31, 41 | `math`, `cleaning_deposit` and `base_price` (only used inside `eval`) are unused. | Removed them; `base_price` is now used directly. |
| Line too long / no final newline (Flake8 E501, W292; Pylint C0304) | Style | 19, 73 | Line is 80 characters; file has no trailing newline. | Shortened the line and added a final newline. |
| Non-snake_case function name (Pylint C0103) | Convention | 15 | `bookRoom` breaks PEP 8 naming. | Renamed to `book_room`; global renamed to `ROOM_INVENTORY`. |
| Missing docstrings (Pylint C0116) | Convention | 15–61 | No function has a docstring. | Added docstrings to every function. |
| `%` formatting, redundant if/else (Pylint C0209, R1703, R1705) | Convention | 19, 34–37 | Old-style formatting; `if/else` returning True/False. | Used an f-string; `return not ROOM_INVENTORY[room_num]["is_booked"]`. |
| `main()` runs on import | Convention | 73 | Importing the module runs the whole demo. | Wrapped in `if __name__ == "__main__":`. |
