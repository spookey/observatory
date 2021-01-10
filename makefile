DEBUG		:=	1
ENVIRON		:=	development
FLASK		:=	application.py

_HOST		:=	::1
_PORT		:=	5000

CMD_GIT		:=	git
CMD_MAKE	:=	make
CMD_VENV	:=	virtualenv
DIR_VENV	:=	venv
VER_PY		:=	3.8
CMD_PIP		:=	$(DIR_VENV)/bin/pip$(VER_PY)
CMD_PY		:=	$(DIR_VENV)/bin/python$(VER_PY)
CMD_FLASK	:=	$(DIR_VENV)/bin/flask
CMD_BLACK	:=	$(DIR_VENV)/bin/black
CMD_ISORT	:=	$(DIR_VENV)/bin/isort
CMD_BPY		:=	$(DIR_VENV)/bin/bpython
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
	@echo "black            run black"
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
	$(CMD_PIP) install -U pip

.PHONY: requirements
requirements: $(CMD_FLASK)
.PHONY: requirements-dev
requirements-dev: $(CMD_BLACK) $(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST)
.PHONY: requirements-debug
requirements-debug: $(CMD_BPY) $(CMD_PUDB)

$(CMD_FLASK): | $(DIR_VENV)
	$(CMD_PIP) install -r "requirements.txt"
$(CMD_BLACK) $(CMD_ISORT) $(CMD_PYLINT) $(CMD_PYREV) $(CMD_PYTEST): | $(DIR_VENV)
	$(CMD_PIP) install -r "requirements-dev.txt"
$(CMD_BPY) $(CMD_PUDB): | $(DIR_VENV)
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
$(OUT_CODE): | $(DIR_NODEM)
	$(CMD_NPM) run distCode
$(OUT_VIEW): | $(DIR_NODEM)
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

.PHONY: lint
lint: $(CMD_PYLINT)
	$(call _lint,"$(DIR_OBVTY)" "$(FLASK)")
.PHONY: lintt
lintt: $(CMD_PYLINT)
	$(call _lint,"$(DIR_TESTS)")
.PHONY: lints
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

.PHONY: plot
plot: $(CMD_PYREV)
	$(call _reverse,$(DIR_OBVTY))
.PHONY: plott
plott: $(CMD_PYREV)
	$(call _reverse,$(DIR_TESTS),_$(DIR_OBVTY))
.PHONY: plots
plots: $(CMD_PYREV)
	$(call _reverse,$(DIR_STUFF),_$(DIR_OBVTY))


define _sort
	$(CMD_ISORT) \
		--combine-star \
		--force-sort-within-sections \
		--py "$(subst .,,$(VER_PY))" \
		--line-width="79" \
		--multi-line "VERTICAL_HANGING_INDENT" \
		--trailing-comma \
		--force-grid-wrap 0 \
		--use-parentheses \
		--ensure-newline-before-comments \
			$(1)
endef

.PHONY: sort
sort: $(CMD_ISORT)
	$(call _sort,"$(DIR_OBVTY)" "$(FLASK)")
.PHONY: sortt
sortt: $(CMD_ISORT)
	$(call _sort,"$(DIR_TESTS)")
.PHONY: sorts
sorts: $(CMD_ISORT)
	$(call _sort,"$(DIR_STUFF)")


define _black
	$(CMD_BLACK) \
		--skip-string-normalization \
		--target-version "py$(subst .,,$(VER_PY))" \
		--line-length 79 \
			$(1)
endef

.PHONY: black
black: $(CMD_BLACK)
	$(call _black,"$(DIR_OBVTY)" "$(FLASK)")
.PHONY: blackt
blackt: $(CMD_BLACK)
	$(call _black,"$(DIR_TESTS)")
.PHONY: blacks
blacks: $(CMD_BLACK)
	$(call _black,"$(DIR_STUFF)")


define _test
	$(CMD_PYTEST) -vv $(1) "$(DIR_TESTS)"
endef
define _tcov
	$(call _test,$(1) --cov="$(DIR_OBVTY)")
endef

HTMLCOV		:=	htmlcov

.PHONY: test
test: $(CMD_PYTEST)
	$(call _test,--durations=5)
.PHONY:tcov
tcov: $(CMD_PYTEST)
	$(call _tcov,)
.PHONY:tcovh
tcovh: $(CMD_PYTEST)
	$(call _tcov,--cov-report="html:$(HTMLCOV)")

.PHONY:tcovh-open
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

.PHONY: clean
clean:
	$(call _gitclean,-ndx)
.PHONY: cleanup
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

.PHONY: run
run: $(CMD_FLASK) static
	$(call _flask,run --host "$(_HOST)" --port "$(_PORT)")
.PHONY: shell
shell: $(CMD_FLASK) $(CMD_BPY)
	$(call _flask,shell)
.PHONY: routes
routes: $(CMD_FLASK)
	$(call _flask,routes)


###
# database

.PHONY: db-init
db-init: $(CMD_FLASK)
	$(call _flask,db init)
.PHONY: db-mig
db-mig: $(CMD_FLASK)
	$(call _flask,db migrate)
.PHONY: db-up
db-up: $(CMD_FLASK)
	$(call _flask,db upgrade)
.PHONY: db-down
db-down: $(CMD_FLASK)
	$(call _flask,db downgrade)


###
# cli

.PHONY: cli-adduser
cli-adduser: $(CMD_FLASK)
	$(call _flask,cli adduser)
.PHONY: cli-setpass
cli-setpass: $(CMD_FLASK)
	$(call _flask,cli setpass)
.PHONY: cli-setstate-active
cli-setstate-active: $(CMD_FLASK)
	$(call _flask,cli setstate --active)
.PHONY: cli-setstate-blocked
cli-setstate-blocked: $(CMD_FLASK)
	$(call _flask,cli setstate --blocked)
.PHONY: cli-sensorclear
cli-sensorclear: $(CMD_FLASK)
	$(call _flask,cli sensorclear)
.PHONY: cli-sensorcurve
cli-sensorcurve: $(CMD_FLASK)
	$(call _flask,cli sensorcurve)

###
# continuous integration

.PHONY: ci
ci: $(CMD_PYTEST) static
	$(call _tcov,--durations=10)


CMD_MKTMP	:=	mktemp
CMD_RM		:=	rm

.PHONY: ci-phony
ci-phony:
	tmpdir=$$($(CMD_MKTMP) -d -t "$(DIR_OBVTY).phony") && \
	echo "=> $$tmpdir" && \
	$(CMD_GIT) clone . "$$tmpdir" && \
	$(CMD_MAKE) -C "$$tmpdir" ci && \
	echo "<= $$tmpdir" && \
	$(CMD_RM) -rf "$$tmpdir"
