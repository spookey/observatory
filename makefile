DEBUG		:=	1
ENVIRON		:=	development
FLASK		:=	application.py

_HOST		:=	::1
_PORT		:=	5000

CMD_GIT		:=	git
CMD_VENV	:=	virtualenv
DIR_VENV	:=	venv
VER_PY		:=	3.7
CMD_PIP		:=	$(DIR_VENV)/bin/pip$(VER_PY)
CMD_PY		:=	$(DIR_VENV)/bin/python$(VER_PY)
CMD_FLASK	:=	$(DIR_VENV)/bin/flask
CMD_ISORT	:=	$(DIR_VENV)/bin/isort
CMD_PTPY	:=	$(DIR_VENV)/bin/ptpython
CMD_PUDB	:=	$(DIR_VENV)/bin/pudb3
CMD_PYLINT	:=	$(DIR_VENV)/bin/pylint
CMD_PYREV	:=	$(DIR_VENV)/bin/pyreverse
CMD_PYTEST	:=	$(DIR_VENV)/bin/pytest

DIR_OBVTY	:=	observatory
DIR_STUFF	:=	stuff
DIR_TESTS	:=	tests

DIR_STATIC	:=	$(DIR_OBVTY)/static

DIR_NODEM	:=	node_modules
CMD_NPM		:=	npm

OUT_CODE	:=	$(DIR_STATIC)/script.js
OUT_VIEW	:=	$(DIR_STATIC)/style.css


.PHONY: help
help:
	@echo "observatory makefile"
	@echo "--------------------"
	@echo
	@echo "venv             install virtualenv"
	@echo "requirements     install requirements into venv"
	@echo
	@echo "static           build files for static directory"
	@echo
	@echo "lint             run pylint"
	@echo "plot             run pyreverse"
	@echo "sort             run isort"
	@echo "test             run pytest"
	@echo "tcov, tcovh      run test coverage (html)"
	@echo
	@echo "clean            show files to clean"
	@echo "cleanup          clean files unknown to git"
	@echo
	@echo "run              run application"
	@echo "shell            launch a shell"
	@echo "routes           show flask routes"
	@echo
	@echo "db-init          create migration folder (only needed once)"
	@echo "db-mig           create new db revision"
	@echo "db-up            apply db revision upwards"
	@echo "db-down          apply db revision downwards"
	@echo
	@echo "cli-adduser      add a new user"
	@echo "cli-setpass      set password of user"
	@echo "cli-setstate-..  toggle active/blocked of user"
	@echo


###
# plumbing

$(DIR_VENV):
	$(CMD_VENV) -p "python$(VER_PY)" "$(DIR_VENV)"

.PHONY: requirements requirements-dev requirements-debug
requirements: $(CMD_FLASK)
requirements-dev: $(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST)
requirements-debug: $(CMD_PTPY) $(CMD_PUDB)

$(CMD_FLASK): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"
$(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-dev.txt"
$(CMD_PTPY) $(CMD_PUDB): $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-debug.txt"
	@echo
	@echo "import pudb; pudb.set_trace()"
	@echo


###
# assets

$(DIR_NODEM):
	$(CMD_NPM) install

.PHONY: static
static: $(OUT_CODE) $(OUT_VIEW)
$(OUT_CODE): $(DIR_NODEM)
	$(CMD_NPM) run distCode
$(OUT_VIEW): $(DIR_NODEM)
	$(CMD_NPM) run distView


###
# service

define PYLINT_MESSAGE_TEMPLATE
{C} {path}:{line}:{column} - {msg}
  ↪  {category} {module}.{obj} ({symbol} {msg_id})
endef
export PYLINT_MESSAGE_TEMPLATE

define _lint
	$(CMD_PYLINT) \
		--disable "C0111" \
		--disable "R0801" \
		--msg-template="$$PYLINT_MESSAGE_TEMPLATE" \
		--output-format="colorized" \
			$(1)
endef

.PHONY: lint lintt lints
lint: $(CMD_PYLINT)
	$(call _lint,"$(DIR_OBVTY)")
lintt: $(CMD_PYLINT)
	$(call _lint,"$(DIR_TESTS)")
lints: $(CMD_PYLINT)
	$(call _lint,"$(DIR_STUFF)")


define _reverse
	$(CMD_PYREV) \
		--all-ancestors \
		--filter-mode="ALL" \
		--module-names="yes" \
		--output png \
		--project="$(1)$(2)" \
			$(1)
endef

.PHONY: plot plott plots
plot: $(CMD_PYREV)
	$(call _reverse,$(DIR_OBVTY))
plott: $(CMD_PYREV)
	$(call _reverse,$(DIR_TESTS),_$(DIR_OBVTY))
plots: $(CMD_PYREV)
	$(call _reverse,$(DIR_STUFF),_$(DIR_OBVTY))


define _sort
	$(CMD_ISORT) -cs -fss -m=5 -y -rc $(1)
endef

.PHONY: sort sortt sorts
sort: $(CMD_ISORT)
	$(call _sort,"$(DIR_OBVTY)")
sortt: $(CMD_ISORT)
	$(call _sort,"$(DIR_TESTS)")
sorts: $(CMD_ISORT)
	$(call _sort,"$(DIR_STUFF)")


define _test
	$(CMD_PYTEST) -vv $(1) "$(DIR_TESTS)"
endef
define _tcov
	$(call _test,$(1) --cov="$(DIR_OBVTY)")
endef

HTMLCOV		:=	htmlcov

.PHONY: test tcov tcovh tcovh-open
test: $(CMD_PYTEST)
	$(call _test,--durations=5)
tcov: $(CMD_PYTEST)
	$(call _tcov,)
tcovh: $(CMD_PYTEST)
	$(call _tcov,--cov-report="html:$(HTMLCOV)")

tcovh-open: tcovh
	$(CMD_PY) -m webbrowser -t "$(HTMLCOV)/index.html"


###
# cleanup

define _gitclean
	$(CMD_GIT) clean \
		-e "*.py" \
		-e "*.sqlite" \
		-e ".env" \
		-e "secret.key" \
		-e "$(DIR_VENV)/" \
		$(1)
endef

.PHONY: clean cleanup
clean:
	$(call _gitclean,-ndx)
cleanup:
	$(call _gitclean,-fdx)


###
# flask

define _flask
	FLASK_DEBUG="$(DEBUG)" \
	FLASK_ENV="$(ENVIRON)" \
	FLASK_APP="$(FLASK)" \
	LOG_LVL="debug" \
	$(CMD_FLASK) $(1)
endef

.PHONY: run shell routes
run: $(CMD_FLASK) static
	$(call _flask,run --host "$(_HOST)" --port "$(_PORT)")
shell: $(CMD_FLASK)
	$(call _flask,shell)
routes: $(CMD_FLASK)
	$(call _flask,routes)


###
# database

.PHONY: db-init db-mig db-up db-down
db-init: $(CMD_FLASK)
	$(call _flask,db init)
db-mig: $(CMD_FLASK)
	$(call _flask,db migrate)
db-up: $(CMD_FLASK)
	$(call _flask,db upgrade)
db-down: $(CMD_FLASK)
	$(call _flask,db downgrade)


###
# cli

.PHONY: cli-adduser cli-setpass cli-setstate-active cli-setstate-blocked
cli-adduser: $(CMD_FLASK)
	$(call _flask,cli adduser)
cli-setpass: $(CMD_FLASK)
	$(call _flask,cli setpass)
cli-setstate-active: $(CMD_FLASK)
	$(call _flask,cli setstate --active)
cli-setstate-blocked: $(CMD_FLASK)
	$(call _flask,cli setstate --blocked)


###
# continuous integration

.PHONY: travis
travis: $(CMD_PYTEST)
	$(call _tcov,--durations=10)


CMD_MKTMP	:=	mktemp
CMD_MAKE	:=	make
CMD_RM		:=	rm

.PHONY: travis-phony
travis-phony:
	tmpdir=$$($(CMD_MKTMP) -d -t "$(DIR_OBVTY).phony") && \
	echo "=> $$tmpdir" && \
	$(CMD_GIT) clone . "$$tmpdir" && \
	$(CMD_MAKE) -C "$$tmpdir" travis && \
	echo "<= $$tmpdir" && \
	$(CMD_RM) -rf "$$tmpdir"
