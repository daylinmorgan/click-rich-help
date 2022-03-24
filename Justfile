lint:
  pre-commit run --all

test:
  mypy click_rich_help
  py.test tests
