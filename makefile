update_db:
	flask db migrate && flask db upgrade
new_db:
	rm -rf migrations
	flask db init && flask db migrate && flask db upgrade

