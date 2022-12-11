# build image
docker-build:
	docker build . \
		--tag scraper:latest

# build the container from image
docker-run:
	docker run \
		-p 9000:8080 \
		--name scraper \
		-e AWS_ACCESS_KEY_ID=AKIAUTIELVA45LLIQPAH \
		-e AWS_SECRET_ACCESS_KEY=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 \
		-e AWS_DEFAULT_REGION=us-west-2 \
		scraper:latest

# test the container
docker-test:
	# test code with inputs
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"0": ["data analyst", "boston", "1"], "1": ["data scientist", "new york", "1"]}'

# clean up
docker-clean:
	docker kill scraper
	docker rm scraper
	docker image rm scraper:latest

# gets chromedriver and python dependencies
fetch-dependencies:
	mkdir -p bin/

	# get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# get headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# clean
	rm headless-chromium.zip chromedriver.zip

	mkdir -p lib/

	# install python dependencies
	python3 -m pip install -r requirements.txt -t lib/.

# builds zip file to be uploaded to AWS Lambda (run fetch-dependencies first!)
build-lambda-package:
	mkdir build
	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.
	cd build; zip -9qr build.zip .
	cp build/build.zip .
	rm -rf build