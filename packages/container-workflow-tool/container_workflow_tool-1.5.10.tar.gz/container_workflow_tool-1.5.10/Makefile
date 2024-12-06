.PHONY: test-in-container build-generator push-generator build

TEST_IMAGE=cwt-tests
GENERATOR_IMAGE=quay.io/rhscl/cwt-generator
UNAME=$(shell uname)
ifeq ($(UNAME),Darwin)
	PODMAN := /opt/podman/bin/podman
else
	PODMAN := /usr/bin/podman
endif

.PHONY: tests
tests:
	cd tests && PYTHONPATH=$(CURDIR) python3 -m pytest --color=yes --verbose --showlocals .

build:
	$(PODMAN) build --tag $(TEST_IMAGE) -f Dockerfile.tests .

test-in-container:
	$(PODMAN) run --rm -it $(TEST_IMAGE)

build-generator:
	$(PODMAN) build --tag ${GENERATOR_IMAGE} -f Dockerfile.generator .

push-generator: build-generator
	$(PODMAN) push ${GENERATOR_IMAGE}
