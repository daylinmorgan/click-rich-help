lint:
  pre-commit run --all

test:
  py.test tests
  mypy click_rich_help

screenshot:
  python scripts/make_screenshots.py
