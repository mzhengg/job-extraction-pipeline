# build image
build:
	docker build . \
		--tag scraper:latest

# run the image (build the container)
# IMPORTANT: these are dummy keys, replace them with your own before executing
run:
	docker run \
		-p 9000:8080 \
		--name scraper \
		-e AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE \
		-e AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY \
		-e AWS_DEFAULT_REGION=us-west-2 \
		scraper:latest

# test lambda function (input in JSON format)
test:
	curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"0": ["data analyst", "boston", "1"], "1": ["data scientist", "new york", "1"]}'

# destroy container and image
destroy:
	docker kill scraper
	docker rm scraper
	docker image rm scraper:latest

# build lambda deployment package
package:
	mkdir -p bin/

	# get chromedriver
	curl -SL https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip > chromedriver.zip
	unzip chromedriver.zip -d bin/

	# get headless-chrome
	curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-37/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
	unzip headless-chromium.zip -d bin/

	# clean up
	rm headless-chromium.zip chromedriver.zip

	# install python dependencies
	mkdir -p lib/
	python3 -m pip install -r requirements.txt -t lib/.

	# make zip package
	mkdir build

	cp -r src build/.
	cp -r bin build/.
	cp -r lib build/.

	cd build; zip -9qr build.zip .
	cp build/build.zip .
	
	rm -rf build