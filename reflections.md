# Reflections

## 1. Which issues were easiest to fix, and which were hardest?

The Flake8 ones were the easiest: things like the unused `math` import, `== None` and the missing newline at the end of the file. Each of them took a few seconds to fix and didn't change how the program behaves.

The Bandit ones were the hardest, especially `eval()` and the hardcoded secret key. I couldn't just delete `eval`. I had to change `compute_seasonal_rate` to take a number instead of a string. The secret key also needed somewhere else to come from, so I moved it into an environment variable.

## 2. Did the tools give any false positives or miss any real problems?

Partly, yes. Pylint said `base_price` was unused, but it was actually used inside the `eval` string. The tools can't see inside strings. Bandit flagged `random` for the booking reference, which isn't really a security risk for a 4-digit number, but switching to `secrets` was easy, so I did it anyway.

They also missed some real problems. The program printed the admin token to the screen, and `main()` never checked whether the booking worked. I only noticed these by running the program and reading the output.

## 3. How would you use these tools in a real workflow?

I'd run Flake8 and Pylint in the editor or as a pre-commit hook so problems get caught early. On GitHub, a CI workflow could run all three tools on every push. It would fail the build if the Pylint score drops below 9.5 or if Bandit finds anything medium or high severity.

## 4. What improved after the fixes?

Pylint went from 5.32 to 10.00, and both Bandit and Flake8 now report no issues. The code is safer, with no `eval`, no shell commands and no exposed secret. It's also easier to read, with proper names, docstrings and simpler logic. The program still works the same way, and it now shows the booking result too.
