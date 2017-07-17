default: publish

publish:
	rm -fr build
	docker build -t dropbox-api-tool .
	mkdir -p build
	docker save -o "build/dropbox-api-tool-$(shell date +%Y_%m_%d_%H%M%S)" dropbox-api-tool
	rsync -r --progress build poseidon:/root/dropbox-org-exporter
