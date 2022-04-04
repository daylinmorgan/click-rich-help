lint:
  pre-commit run --all

test:
  py.test tests
  mypy click_rich_help
