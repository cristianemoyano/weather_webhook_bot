new_release:
	git checkout master
	git pull origin master
	echo "git tag -a v1.4 -m 'my version 1.4'"
	echo "git push origin v1.4"

deploy:
	git checkout master
	git pull origin master
	git push heroku master

test_suite:
	python test_suite.py test

run:
	python server.py