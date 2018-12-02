new_release:
	git checkout master
	git pull origin master
	echo "git tag -a v1.4 -m 'my version 1.4'"
	echo "git push origin v1.4"

deploy:
	git checkout master
	git pull origin master
	git push heroku master

run:
	python3 server.py

setup:
	pip3 install -r requirements.txt

clean_local_branches:
	git branch | grep -v "master" | xargs git branch -D

test:
	python3 test_suite.py test

logs:
	heroku logs --tail

upgrade:
	pip3 install --upgrade --force-reinstall -r requirements.txt